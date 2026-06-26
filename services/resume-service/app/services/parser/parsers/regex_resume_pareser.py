import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_line(value: str | None) -> str | None:
    if not value:
        return None
    value = value.replace("\u200b", "").replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" |,-•–—\n\t") or None


def _limit(value: str | None, max_length: int = 255) -> str | None:
    value = _clean_line(value)
    return value[:max_length] if value else None


def _non_empty_lines(text: str) -> list[str]:
    return [c for line in text.splitlines() if (c := _clean_line(line))]


def _normalize_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    return url


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")

_PHONE = re.compile(
    r"(?<!\d)"
    r"(\+?\d{1,3}[\s\-.]?)?"
    r"(\(?\d{3,5}\)?[\s\-.]?)?"
    r"\d{4,5}[\s\-.]?\d{4,5}"
    r"(?!\d)"
)

_LINKEDIN = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_\-]+/?",
    re.IGNORECASE,
)

_GITHUB = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*/?",
    re.IGNORECASE,
)

_PORTFOLIO = re.compile(
    r"(?:https?://)[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)+(?:/[^\s]*)?",
    re.IGNORECASE,
)

_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")

_BULLET = re.compile(r"^[•\-\*\u2022\u25cf\u25e6\u2013]\s*")

_MONTH = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
)

_DATE_RANGE = re.compile(
    rf"({_MONTH}\.?\s*\d{{4}}|\d{{4}})\s*(?:–|-|to)\s*"
    rf"({_MONTH}\.?\s*\d{{4}}|\d{{4}}|Present|Current|Till\s+Date)",
    re.IGNORECASE,
)

_EMPLOYMENT_TYPE = re.compile(
    r"\b(Internship|Intern|Full[-\s]?time|Part[-\s]?time|Contract|Freelance|Trainee)\b",
    re.IGNORECASE,
)

_LOCATION_HINT = re.compile(
    r"\b(Remote|Hybrid|Onsite|Lucknow|Delhi|Noida|Gurgaon|Gurugram|Bangalore|"
    r"Bengaluru|Mumbai|Pune|Hyderabad|Chennai|Kolkata|India)\b",
    re.IGNORECASE,
)

_ALL_SECTION_HEADERS = [
    "education", "academic background", "academic qualification",
    "experience", "work experience", "professional experience", "employment",
    "internship", "internships",
    "projects", "project", "academic projects", "personal projects", "key projects",
    "skills", "technical skills", "core competencies", "technologies",
    "certifications", "certificates", "achievements", "awards",
    "summary", "objective", "career objective", "profile", "about me",
    "publications", "languages", "hobbies", "interests", "extra-curricular",
    "activities", "volunteer", "volunteering",
]

_GRADE_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"CGPA[:\s]+([0-9]+(?:\.[0-9]+)?(?:\s*/\s*[0-9]+(?:\.[0-9]+)?)?)",
        r"GPA[:\s]+([0-9]+(?:\.[0-9]+)?(?:\s*/\s*[0-9]+(?:\.[0-9]+)?)?)",
        r"SGPA[:\s]+([0-9]+(?:\.[0-9]+)?)",
        r"Percentage[:\s]+([0-9]+(?:\.[0-9]+)?%?)",
        r"([0-9]+(?:\.[0-9]+)?)\s*/\s*10\b",
        r"([0-9]+(?:\.[0-9]+)?)\s*/\s*4\.0\b",
        r"([0-9]{2,3}(?:\.[0-9]+)?)\s*%",
    ]
]

KNOWN_SKILLS: set[str] = {
    "python", "java", "javascript", "typescript", "c++", "c", "c#",
    "go", "golang", "rust", "kotlin", "swift", "r", "scala", "php",
    "ruby", "perl", "bash", "shell", "powershell", "dart",
    "fastapi", "django", "flask", "express", "spring boot",
    "react", "next.js", "vue", "angular", "html", "css", "tailwind",
    "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite",
    "sqlalchemy", "alembic", "docker", "kubernetes", "nginx",
    "git", "github", "linux", "postman", "swagger",
    "jwt", "oauth", "rest", "graphql", "websockets",
    "pytest", "jest", "selenium",
}

_DEGREE_KEYWORDS = re.compile(
    r"\b(B\.?Tech|B\.?E|B\.?Sc|B\.?Com|B\.?A|BCA|BBA|MBA|M\.?Tech|M\.?Sc|"
    r"M\.?E|MCA|Ph\.?D|Bachelor|Master|Doctorate|Diploma|12th|10th|HSC|SSC|CBSE|ICSE)\b",
    re.IGNORECASE,
)

_INSTITUTION_KEYWORDS = re.compile(
    r"\b(University|Institute|College|School|Academy|IIT|NIT|BITS|LIT|VIT|SRM|IIIT)\b",
    re.IGNORECASE,
)


class RegexResumeParser:
    async def parse(self, text: str) -> dict[str, Any]:
        cleaned = self._clean_text(text)
        sections = self._split_sections(cleaned)

        parsed = {
            "profile": self._parse_profile(cleaned, sections),
            "skills": self._parse_skills(cleaned, sections),
            "educations": self._parse_educations(cleaned, sections),
            "experiences": self._parse_experiences(sections),
            "projects": self._parse_projects(sections),
        }

        return parsed

    # -----------------------------------------------------------------------
    # Clean + Sections
    # -----------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.replace("\u200b", "").replace("\u00a0", " ")
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _split_sections(self, text: str) -> dict[str, str]:
        lines = text.splitlines()
        sections: dict[str, str] = {}

        current_header = "__preamble__"
        buffer: list[str] = []

        for line in lines:
            stripped = line.strip()
            header = self._detect_section_header(stripped)

            if header:
                if buffer:
                    body = "\n".join(buffer).strip()
                    if body:
                        sections[current_header] = (
                            sections.get(current_header, "") + "\n" + body
                        ).strip()

                current_header = header
                buffer = []
            else:
                buffer.append(line)

        if buffer:
            body = "\n".join(buffer).strip()
            if body:
                sections[current_header] = (
                    sections.get(current_header, "") + "\n" + body
                ).strip()

        return sections

    def _detect_section_header(self, line: str) -> str | None:
        if not line or len(line) > 60:
            return None

        clean = line.rstrip(":- \t")
        lower = clean.lower()

        for header in _ALL_SECTION_HEADERS:
            if lower == header:
                return header

        if re.match(r"^[A-Z][A-Z\s&/\-]{3,}$", clean) and not re.search(r"\d", clean):
            candidate = clean.lower().strip()
            for header in _ALL_SECTION_HEADERS:
                if header in candidate or candidate in header:
                    return header

        return None

    def _get_section(self, sections: dict[str, str], *names: str) -> str | None:
        for name in names:
            if name in sections:
                return sections[name]

            for key, val in sections.items():
                if name in key and val:
                    return val

        return None

    # -----------------------------------------------------------------------
    # Profile
    # -----------------------------------------------------------------------

    def _parse_profile(self, full_text: str, sections: dict[str, str]) -> dict[str, Any]:
        return {
            "full_name": self._extract_name(full_text, sections),
            "email": self._extract_email(full_text),
            "phone": self._extract_phone(full_text),
            "linkedin_url": self._extract_linkedin(full_text),
            "github_url": self._extract_github(full_text),
            "portfolio_url": self._extract_portfolio(full_text),
            "professional_summary": self._extract_summary(sections),
        }

    def _extract_email(self, text: str) -> str | None:
        m = _EMAIL.search(text)
        return m.group().strip().lower() if m else None

    def _extract_phone(self, text: str) -> str | None:
        m = _PHONE.search(text)
        if not m:
            return None

        raw = re.sub(r"[^\d+]", "", m.group())

        if re.fullmatch(r"(?:19|20)\d{2}", raw):
            return None

        return raw if len(raw) >= 7 else None

    def _extract_linkedin(self, text: str) -> str | None:
        m = _LINKEDIN.search(text)
        return _normalize_url(m.group()) if m else None

    def _extract_github(self, text: str) -> str | None:
        m = _GITHUB.search(text)
        return _normalize_url(m.group()) if m else None

    def _extract_portfolio(self, text: str) -> str | None:
        for m in _PORTFOLIO.finditer(text):
            url = m.group()
            if "linkedin.com" in url or "github.com" in url:
                continue
            return _normalize_url(url)

        return None

    def _extract_name(self, text: str, sections: dict[str, str]) -> str | None:
        blocked = {
            "resume", "curriculum vitae", "cv", "email", "phone", "mobile",
            "skills", "education", "experience", "projects", "summary",
            "objective", "profile", "contact", "address", "linkedin", "github",
        }

        preamble = sections.get("__preamble__", "")
        candidate_text = preamble if preamble else text
        lines = _non_empty_lines(candidate_text)

        for line in lines[:10]:
            line_clean = _EMAIL.sub("", line)
            line_clean = _PHONE.sub("", line_clean)
            line_clean = _LINKEDIN.sub("", line_clean)
            line_clean = _GITHUB.sub("", line_clean)
            line_clean = re.sub(r"https?://\S+", "", line_clean)
            line_clean = re.sub(r"[^A-Za-z\s'\-]", "", line_clean).strip()

            if not line_clean:
                continue

            if line_clean.lower() in blocked:
                continue

            if any(w in blocked for w in line_clean.lower().split()):
                continue

            words = line_clean.split()

            if 2 <= len(words) <= 5:
                return line_clean.title()

        return None

    def _extract_summary(self, sections: dict[str, str]) -> str | None:
        body = self._get_section(
            sections,
            "summary",
            "objective",
            "career objective",
            "profile",
            "about me",
            "professional summary",
        )

        if not body:
            return None

        return _limit(" ".join(_non_empty_lines(body)), 1000)

    # -----------------------------------------------------------------------
    # Skills
    # -----------------------------------------------------------------------

    def _parse_skills(self, full_text: str, sections: dict[str, str]) -> list[str]:
        skills_text = self._get_section(
            sections,
            "skills",
            "technical skills",
            "core competencies",
            "technologies",
        ) or ""

        search_text = (skills_text + "\n" + full_text).lower()
        found: set[str] = set()

        for skill in KNOWN_SKILLS:
            pattern = re.compile(
                r"(?<![a-z])" + re.escape(skill) + r"(?![a-z])",
                re.IGNORECASE,
            )
            if pattern.search(search_text):
                found.add(skill.title())

        if skills_text:
            for separator in [",", "|", "·", "•", "\n"]:
                parts = skills_text.split(separator)
                if len(parts) > 2:
                    for part in parts:
                        token = _clean_line(part)
                        if token and 2 <= len(token) <= 40:
                            found.add(token.title())
                    break

        return sorted(found)

    # -----------------------------------------------------------------------
    # Education
    # -----------------------------------------------------------------------

    def _parse_educations(
        self,
        full_text: str,
        sections: dict[str, str],
    ) -> list[dict[str, Any]]:
        edu_text = self._get_section(
            sections,
            "education",
            "academic background",
            "academic qualification",
        )

        if not edu_text:
            edu_text = self._find_education_block(full_text)

        if not edu_text:
            return []

        return self._parse_education_block(edu_text)

    def _find_education_block(self, text: str) -> str | None:
        lines = text.splitlines()
        blocks: list[str] = []
        inside = False

        for line in lines:
            if _DEGREE_KEYWORDS.search(line) or _INSTITUTION_KEYWORDS.search(line):
                inside = True

            if inside:
                blocks.append(line)
                if len(blocks) > 8:
                    break

        return "\n".join(blocks) if blocks else None

    def _parse_education_block(self, text: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        lines = _non_empty_lines(text)

        i = 0
        while i < len(lines):
            line = lines[i]

            if _DEGREE_KEYWORDS.search(line) or _INSTITUTION_KEYWORDS.search(line):
                block_lines = [line]

                for j in range(i + 1, min(i + 6, len(lines))):
                    next_line = lines[j]

                    if _DEGREE_KEYWORDS.search(next_line) and j != i + 1:
                        break

                    block_lines.append(next_line)
                    i = j

                edu = self._parse_single_education(block_lines)
                if edu:
                    results.append(edu)

            i += 1

        return results if results else self._parse_education_fallback(text)

    def _parse_single_education(self, block: list[str]) -> dict[str, Any] | None:
        combined = "\n".join(block)

        if "·" in combined:
            parts = [_clean_line(p) for p in combined.split("·") if _clean_line(p)]
        elif "," in combined and len(combined.split(",")) >= 2:
            parts = [_clean_line(p) for p in combined.split(",") if _clean_line(p)]
        else:
            parts = block

        degree = None
        institution = None
        field = None

        for part in parts:
            if not part:
                continue

            if _DEGREE_KEYWORDS.search(part) and not degree:
                degree = _YEAR.sub("", part).strip(" ·-–,")

                field_match = re.search(r"\(([^)]+)\)", part)
                if field_match:
                    field = _clean_line(field_match.group(1))
                    degree = re.sub(r"\([^)]+\)", "", degree).strip()

            elif _INSTITUTION_KEYWORDS.search(part) and not institution:
                institution = _YEAR.sub("", part).strip(" ·-–,")

            elif not institution and not _YEAR.search(part) and len(part.split()) >= 2:
                institution = part

        years = _YEAR.findall(combined)
        start_year = int(years[0]) if years else None
        end_year = int(years[-1]) if len(years) >= 2 else None

        if start_year and end_year and start_year == end_year:
            end_year = None

        return {
            "degree": _limit(degree),
            "institution": _limit(institution),
            "field_of_study": _limit(field),
            "start_year": start_year,
            "end_year": end_year,
            "grade": self._extract_grade(combined),
        }

    def _parse_education_fallback(self, text: str) -> list[dict[str, Any]]:
        years = _YEAR.findall(text)

        return [
            {
                "degree": None,
                "institution": None,
                "field_of_study": None,
                "start_year": int(years[0]) if years else None,
                "end_year": int(years[-1]) if len(years) >= 2 else None,
                "grade": self._extract_grade(text),
            }
        ]

    def _extract_grade(self, text: str) -> str | None:
        for pattern in _GRADE_PATTERNS:
            m = pattern.search(text)
            if m:
                return _limit(m.group(1), 50)

        return None

    # -----------------------------------------------------------------------
    # Experience
    # -----------------------------------------------------------------------

    def _parse_experiences(self, sections: dict[str, str]) -> list[dict[str, Any]]:
        exp_text = self._get_section(
            sections,
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "internship",
            "internships",
        )

        if not exp_text:
            return []

        lines = _non_empty_lines(exp_text)
        if not lines:
            return []

        blocks = self._split_experience_blocks(lines)

        experiences: list[dict[str, Any]] = []

        for block in blocks:
            exp = self._parse_experience_block(block)
            if exp:
                experiences.append(exp)

        if not experiences:
            return [
                {
                    "company_name": None,
                    "job_title": None,
                    "employment_type": None,
                    "location": None,
                    "start_date": None,
                    "end_date": None,
                    "is_current": False,
                    "description": _limit(exp_text, 2000),
                }
            ]

        return experiences

    def _split_experience_blocks(self, lines: list[str]) -> list[list[str]]:
        blocks: list[list[str]] = []
        current: list[str] = []

        for line in lines:
            is_heading = (
                not _BULLET.match(line)
                and (
                    _DATE_RANGE.search(line)
                    or _YEAR.search(line)
                    or _EMPLOYMENT_TYPE.search(line)
                )
                and len(line.split()) <= 16
            )

            if is_heading and current:
                blocks.append(current)
                current = [line]
            elif is_heading and not current:
                current = [line]
            else:
                if current:
                    current.append(line)
                else:
                    current = [line]

        if current:
            blocks.append(current)

        return blocks if blocks else [lines]

    def _parse_experience_block(self, block: list[str]) -> dict[str, Any] | None:
        if not block:
            return None

        heading = block[0]
        rest = block[1:]
        combined = "\n".join(block)

        company, title, location = self._parse_experience_heading(heading, rest)

        start_date, end_date = self._extract_date_range(combined)
        employment_type = self._extract_employment_type(combined)

        is_current = bool(
            end_date and end_date.lower() in {"present", "current", "till date"}
        )

        if not location:
            location = self._extract_location(combined)

        description_lines = []

        for line in rest:
            clean = _clean_line(line)
            if not clean:
                continue

            if _DATE_RANGE.search(clean):
                continue

            if clean == company or clean == title or clean == location:
                continue

            if _BULLET.match(clean):
                description_lines.append(_BULLET.sub("", clean).strip())
            elif len(clean.split()) > 5:
                description_lines.append(clean)

        description = " ".join(description_lines).strip()

        return {
            "company_name": _limit(company),
            "job_title": _limit(title),
            "employment_type": _limit(employment_type),
            "location": _limit(location),
            "start_date": self._normalize_resume_date(start_date),
            "end_date": None if is_current else self._normalize_resume_date(end_date),
            "is_current": is_current,
            "description": _limit(description, 2000) or None,
        }

    def _parse_experience_heading(
        self,
        heading: str,
        rest: list[str],
    ) -> tuple[str | None, str | None, str | None]:
        heading_clean = _DATE_RANGE.sub("", heading)
        heading_clean = _YEAR.sub("", heading_clean)
        heading_clean = _EMPLOYMENT_TYPE.sub("", heading_clean)
        heading_clean = re.sub(r"\s+", " ", heading_clean).strip(" |·-,")

        company = None
        title = None
        location = None

        title_keywords = re.compile(
            r"\b(engineer|developer|intern|analyst|designer|manager|"
            r"lead|architect|consultant|associate|officer|executive|"
            r"scientist|researcher|coordinator|trainee|backend|frontend|"
            r"fullstack|full-stack|software)\b",
            re.IGNORECASE,
        )

        for sep in ["·", "|", " - ", " – "]:
            if sep in heading_clean:
                parts = [_clean_line(p) for p in heading_clean.split(sep) if _clean_line(p)]

                for part in parts:
                    if not part:
                        continue

                    if title_keywords.search(part) and not title:
                        title = part
                    elif _LOCATION_HINT.search(part) and not location:
                        location = part
                    elif not company:
                        company = part

                return company, title, location

        if heading_clean:
            if title_keywords.search(heading_clean):
                title = heading_clean
            else:
                company = heading_clean

        for line in rest[:3]:
            clean = _clean_line(line)
            if not clean:
                continue

            if _DATE_RANGE.search(clean):
                continue

            if _LOCATION_HINT.search(clean) and not location:
                location = clean
                continue

            if title_keywords.search(clean) and not title:
                title = clean
                continue

            if not company and len(clean.split()) <= 6:
                company = clean

        return company, title, location

    def _extract_date_range(self, text: str) -> tuple[str | None, str | None]:
        m = _DATE_RANGE.search(text)

        if m:
            return _clean_line(m.group(1)), _clean_line(m.group(2))

        years = _YEAR.findall(text)

        if len(years) >= 2:
            return years[0], years[-1]

        if len(years) == 1:
            return years[0], None

        return None, None

    def _extract_employment_type(self, text: str) -> str | None:
        m = _EMPLOYMENT_TYPE.search(text)

        if not m:
            return None

        value = m.group(1).lower().replace(" ", "-")

        mapping = {
            "intern": "Internship",
            "internship": "Internship",
            "full-time": "Full-time",
            "part-time": "Part-time",
            "contract": "Contract",
            "freelance": "Freelance",
            "trainee": "Trainee",
        }

        return mapping.get(value, value.title())

    def _extract_location(self, text: str) -> str | None:
        m = _LOCATION_HINT.search(text)
        return m.group(1) if m else None

    def _normalize_resume_date(self, value: str | None) -> str | None:
        if not value:
            return None

        value = _clean_line(value)

        if not value:
            return None

        if value.lower() in {"present", "current", "till date"}:
            return None

        month_map = {
            "jan": "01", "january": "01",
            "feb": "02", "february": "02",
            "mar": "03", "march": "03",
            "apr": "04", "april": "04",
            "may": "05",
            "jun": "06", "june": "06",
            "jul": "07", "july": "07",
            "aug": "08", "august": "08",
            "sep": "09", "september": "09",
            "oct": "10", "october": "10",
            "nov": "11", "november": "11",
            "dec": "12", "december": "12",
        }

        if re.fullmatch(r"\d{4}", value):
            return value

        m = re.search(r"([A-Za-z]+)\.?\s+(\d{4})", value)

        if m:
            month = month_map.get(m.group(1).lower())
            year = m.group(2)

            if month:
                return f"{year}-{month}"

        return value

    # -----------------------------------------------------------------------
    # Projects
    # -----------------------------------------------------------------------

    def _parse_projects(self, sections: dict[str, str]) -> list[dict[str, Any]]:
        projects_text = self._get_section(
            sections,
            "projects",
            "project",
            "academic projects",
            "personal projects",
            "key projects",
        )

        if not projects_text:
            return []

        lines = _non_empty_lines(projects_text)
        if not lines:
            return []

        blocks = self._split_project_blocks(lines)

        projects: list[dict[str, Any]] = []

        for block in blocks:
            project = self._parse_project_block(block)
            if project:
                projects.append(project)

        return projects

    def _split_project_blocks(self, lines: list[str]) -> list[list[str]]:
        blocks: list[list[str]] = []
        current: list[str] = []

        for line in lines:
            if self._is_project_heading(line):
                if current:
                    blocks.append(current)
                current = [line]
            elif current:
                current.append(line)

        if current:
            blocks.append(current)

        return blocks

    def _is_project_heading(self, line: str) -> bool:
        clean = _clean_line(line)

        if not clean:
            return False

        if _BULLET.match(clean):
            return False

        lower = clean.lower()

        hints = [
            "personal project",
            "client project",
            "academic project",
            "freelance project",
            "major project",
            "minor project",
            "open source",
        ]

        if any(h in lower for h in hints):
            return True

        if "·" in clean and _YEAR.search(clean):
            return True

        if "|" in clean and _YEAR.search(clean):
            return True

        if re.match(r"^[A-Z][A-Z\s\-]{4,}$", clean) and len(clean.split()) <= 6:
            return True

        if _YEAR.search(clean) and re.match(r"^[A-Z][a-z]", clean) and len(clean.split()) <= 8:
            return True

        return False

    def _parse_project_block(self, block: list[str]) -> dict[str, Any] | None:
        if not block:
            return None

        heading = _clean_line(block[0])

        if not heading:
            return None

        heading_no_year = _YEAR.sub("", heading).strip(" ·|-,")
        parts = [_clean_line(p) for p in re.split(r"[·|]", heading_no_year) if _clean_line(p)]
        project_name = parts[0] if parts else heading_no_year

        technologies = None
        project_url = None
        description_lines: list[str] = []

        for idx, line in enumerate(block[1:]):
            clean = _clean_line(line)

            if not clean:
                continue

            url_match = _GITHUB.search(clean) or _PORTFOLIO.search(clean)

            if url_match and not project_url:
                project_url = _normalize_url(url_match.group())

            if idx == 0 and self._looks_like_tech_stack(clean):
                technologies = clean
                continue

            if _BULLET.match(clean):
                description_lines.append(_BULLET.sub("", clean).strip())
            else:
                description_lines.append(clean)

        return {
            "project_name": _limit(project_name),
            "technologies": _limit(technologies, 500),
            "project_url": _limit(project_url, 500),
            "description": _limit(" ".join(description_lines), 2000),
        }

    def _looks_like_tech_stack(self, line: str) -> bool:
        lower = line.lower()
        skill_hits = sum(1 for skill in KNOWN_SKILLS if skill in lower)
        has_separator = any(sep in line for sep in ["·", "|", ","])

        return skill_hits >= 2 or (skill_hits >= 1 and has_separator)