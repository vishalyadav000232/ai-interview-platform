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
# Compiled patterns (module-level — compiled once)
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

# Month names + abbreviations
_MONTH = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
)

_DATE_RANGE = re.compile(
    rf"({_MONTH}\.?\s*\d{{4}}|\d{{4}})\s*(?:–|-|to)\s*({_MONTH}\.?\s*\d{{4}}|\d{{4}}|Present|Current|Till\s+Date)",
    re.IGNORECASE,
)

# Section header detection — broad set
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

_SECTION_PATTERN = re.compile(
    r"^(?:" + "|".join(re.escape(h) for h in _ALL_SECTION_HEADERS) + r")\s*[:\-]?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Heading-like lines: ALL CAPS, Title Case short, or ends with colon
_HEADING_LINE = re.compile(
    r"^(?:[A-Z][A-Z\s&/]{3,}|[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\s*:?\s*$"
)

# Grade patterns
_GRADE_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"CGPA[:\s]+([0-9]+(?:\.[0-9]+)?(?:\s*/\s*[0-9]+(?:\.[0-9]+)?)?)",
        r"GPA[:\s]+([0-9]+(?:\.[0-9]+)?(?:\s*/\s*[0-9]+(?:\.[0-9]+)?)?)",
        r"SGPA[:\s]+([0-9]+(?:\.[0-9]+)?)",
        r"Percentage[:\s]+([0-9]+(?:\.[0-9]+)?%?)",
        r"([0-9]+(?:\.[0-9]+)?)\s*/\s*10\b",       # e.g. 8.5/10
        r"([0-9]+(?:\.[0-9]+)?)\s*/\s*4\.0\b",     # e.g. 3.8/4.0
        r"([0-9]{2,3}(?:\.[0-9]+)?)\s*%",          # e.g. 85%
    ]
]

KNOWN_SKILLS: set[str] = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c", "c#",
    "go", "golang", "rust", "kotlin", "swift", "r", "scala", "php",
    "ruby", "perl", "bash", "shell", "powershell", "dart", "lua", "matlab",
    # Web frameworks
    "fastapi", "django", "flask", "express", "express.js", "nest.js", "nestjs",
    "spring", "spring boot", "rails", "laravel", "gin", "fiber",
    # Frontend
    "react", "react.js", "reactjs", "next.js", "nextjs", "vue", "vue.js",
    "angular", "svelte", "nuxt", "nuxt.js", "redux", "zustand", "mobx",
    "html", "css", "sass", "scss", "tailwind", "tailwindcss",
    "bootstrap", "material ui", "chakra ui", "shadcn", "framer motion",
    # Databases
    "postgresql", "postgres", "mysql", "mariadb", "mongodb", "redis",
    "sqlite", "elasticsearch", "cassandra", "dynamodb", "firestore",
    "neo4j", "influxdb", "mssql", "sql server",
    # ORM / migrations
    "sqlalchemy", "alembic", "prisma", "sequelize", "typeorm", "mongoose",
    "hibernate", "gorm",
    # Cloud
    "aws", "gcp", "google cloud", "azure", "vercel", "netlify", "heroku",
    "cloudflare", "digitalocean", "railway", "render",
    # DevOps / infra
    "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
    "github actions", "gitlab ci", "ci/cd", "nginx", "apache",
    # Tools
    "git", "github", "gitlab", "bitbucket", "linux", "unix",
    "postman", "swagger", "jira", "figma",
    # Auth / protocols
    "jwt", "oauth", "oauth2", "rest", "restful", "graphql", "grpc",
    "websockets", "socket.io", "celery", "rabbitmq", "kafka",
    # ML / Data
    "machine learning", "deep learning", "pandas", "numpy", "scikit-learn",
    "tensorflow", "keras", "pytorch", "opencv", "huggingface", "langchain",
    "llm", "rag", "matplotlib", "seaborn", "scipy",
    # Mobile
    "react native", "flutter", "android", "ios", "expo",
    # Testing
    "pytest", "jest", "unittest", "selenium", "cypress", "playwright",
}


# ---------------------------------------------------------------------------
# Degree keywords for education detection
# ---------------------------------------------------------------------------

_DEGREE_KEYWORDS = re.compile(
    r"\b(B\.?Tech|B\.?E|B\.?Sc|B\.?Com|B\.?A|BCA|BBA|MBA|M\.?Tech|M\.?Sc|"
    r"M\.?E|MCA|Ph\.?D|Bachelor|Master|Doctorate|Diploma|12th|10th|HSC|SSC|CBSE|ICSE)\b",
    re.IGNORECASE,
)

_INSTITUTION_KEYWORDS = re.compile(
    r"\b(University|Institute|College|School|Academy|IIT|NIT|BITS|LIT|VIT|SRM|IIIT)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Main Parser
# ---------------------------------------------------------------------------

class RegexResumeParser:
    """
    Regex-based resume parser targeting 90%+ field coverage across
    common resume formats (single-column, multi-column, ATS-plain, decorated).
    """

    async def parse(self, text: str) -> dict[str, Any]:
        cleaned = self._clean_text(text)
        sections = self._split_sections(cleaned)

        parsed: dict[str, Any] = {
            "profile": self._parse_profile(cleaned, sections),
            "skills": self._parse_skills(cleaned, sections),
            "educations": self._parse_educations(cleaned, sections),
            "experiences": self._parse_experiences(sections),
            "projects": self._parse_projects(sections),
        }

        logger.info(
            "Regex resume parsing completed",
            extra={
                "skills_count": len(parsed["skills"]),
                "educations_count": len(parsed["educations"]),
                "experiences_count": len(parsed["experiences"]),
                "projects_count": len(parsed["projects"]),
            },
        )

        return parsed

    # -----------------------------------------------------------------------
    # Text cleaning
    # -----------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.replace("\u200b", "").replace("\u00a0", " ")
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    # -----------------------------------------------------------------------
    # Section splitter  ← the foundation of accuracy
    # -----------------------------------------------------------------------

    def _split_sections(self, text: str) -> dict[str, str]:
        """
        Splits resume into named sections by detecting header lines.
        Handles: ALL CAPS headers, Title Case headers, headers with colons,
        headers detected via known section-name list.
        Returns a dict of lowercase_section_name -> section_body_text.
        """
        lines = text.splitlines()
        sections: dict[str, str] = {}
        current_header: str = "__preamble__"
        buffer: list[str] = []

        for line in lines:
            stripped = line.strip()
            header = self._detect_section_header(stripped)

            if header:
                # save current buffer
                if buffer:
                    body = "\n".join(buffer).strip()
                    if body:
                        sections.setdefault(current_header, "")
                        sections[current_header] += ("\n" + body) if sections[current_header] else body
                current_header = header
                buffer = []
            else:
                buffer.append(line)

        # flush last buffer
        if buffer:
            body = "\n".join(buffer).strip()
            if body:
                sections.setdefault(current_header, "")
                sections[current_header] += ("\n" + body) if sections[current_header] else body

        return sections

    def _detect_section_header(self, line: str) -> str | None:
        """Return canonical lowercase section name if line is a header, else None."""
        if not line or len(line) > 60:
            return None

        # strip trailing colons / dashes
        clean = line.rstrip(":- \t")

        lower = clean.lower()

        # Direct match against known headers
        for header in _ALL_SECTION_HEADERS:
            if lower == header:
                return header

        # ALL CAPS match (at least 4 chars, no digits)
        if re.match(r"^[A-Z][A-Z\s&/\-]{3,}$", clean) and not re.search(r"\d", clean):
            candidate = clean.lower().strip()
            # fuzzy: if any known header is a substring
            for header in _ALL_SECTION_HEADERS:
                if header in candidate or candidate in header:
                    return header
            # Still treat as a header if ALL-CAPS section-like
            if len(clean.split()) <= 4:
                return candidate

        return None

    def _get_section(self, sections: dict[str, str], *names: str) -> str | None:
        """Return the first matching section body, checking aliases."""
        for name in names:
            if name in sections:
                return sections[name]
            # fuzzy: key starts with or contains the name
            for key, val in sections.items():
                if name in key and val:
                    return val
        return None

    # -----------------------------------------------------------------------
    # Profile
    # -----------------------------------------------------------------------

    def _parse_profile(self, full_text: str, sections: dict[str, str]) -> dict[str, Any]:
        name = self._extract_name(full_text, sections)
        email = self._extract_email(full_text)
        phone = self._extract_phone(full_text)
        linkedin = self._extract_linkedin(full_text)
        github = self._extract_github(full_text)
        portfolio = self._extract_portfolio(full_text, linkedin, github)
        summary = self._extract_summary(sections)

        return {
            "full_name": name,
            "email": email,
            "phone": phone,
            "linkedin_url": linkedin,
            "github_url": github,
            "portfolio_url": portfolio,
            "professional_summary": summary,
        }

    def _extract_email(self, text: str) -> str | None:
        m = _EMAIL.search(text)
        return m.group().strip().lower() if m else None

    def _extract_phone(self, text: str) -> str | None:
        m = _PHONE.search(text)
        if not m:
            return None
        raw = re.sub(r"[^\d+]", "", m.group())
        # skip if it looks like a year run
        if re.fullmatch(r"(?:19|20)\d{2}", raw):
            return None
        return raw if len(raw) >= 7 else None

    def _extract_linkedin(self, text: str) -> str | None:
        m = _LINKEDIN.search(text)
        return _normalize_url(m.group()) if m else None

    def _extract_github(self, text: str) -> str | None:
        m = _GITHUB.search(text)
        if not m:
            return None
        url = _normalize_url(m.group())
        # exclude github.com/user/repo style if it looks like a full repo URL in a project
        # Keep only github.com/<username> (one path segment) for the profile field
        path_parts = [p for p in url.replace("https://github.com/", "").split("/") if p]
        if len(path_parts) == 1:
            return url
        # Still return — caller can decide
        return url

    def _extract_portfolio(self, text: str, linkedin: str | None, github: str | None) -> str | None:
        for m in _PORTFOLIO.finditer(text):
            url = m.group()
            if "linkedin.com" in url or "github.com" in url:
                continue
            return _normalize_url(url)
        return None

    def _extract_name(self, text: str, sections: dict[str, str]) -> str | None:
        """
        Strategy (in order):
        1. Preamble lines before any section header — first 2-4 word line of alphabetic words
        2. Lines at the very top of the doc
        """
        BLOCKED = {
            "resume", "curriculum vitae", "cv", "email", "phone", "mobile",
            "skills", "education", "experience", "projects", "summary",
            "objective", "profile", "contact", "address", "linkedin", "github",
        }

        preamble = sections.get("__preamble__", "")
        candidate_text = preamble if preamble else text

        lines = _non_empty_lines(candidate_text)

        for line in lines[:10]:
            # Remove URLs, emails, phones
            line_clean = _EMAIL.sub("", line)
            line_clean = _PHONE.sub("", line_clean)
            line_clean = _LINKEDIN.sub("", line_clean)
            line_clean = _GITHUB.sub("", line_clean)
            line_clean = re.sub(r"https?://\S+", "", line_clean)
            line_clean = re.sub(r"[^A-Za-z\s'\-]", "", line_clean).strip()

            if not line_clean:
                continue

            if line_clean.lower() in BLOCKED:
                continue

            # skip if it contains a blocked word
            if any(w in line_clean.lower().split() for w in BLOCKED):
                continue

            words = line_clean.split()
            if 2 <= len(words) <= 5:
                # all words should be capitalized-like (name tokens)
                if all(re.match(r"^[A-Za-z'\-]+$", w) for w in words):
                    return line_clean.title()

        return None

    def _extract_summary(self, sections: dict[str, str]) -> str | None:
        body = self._get_section(
            sections,
            "summary", "objective", "career objective",
            "profile", "about me", "professional summary",
        )
        if not body:
            return None
        lines = _non_empty_lines(body)
        text = " ".join(lines)
        return _limit(text, 1000)

    # -----------------------------------------------------------------------
    # Skills
    # -----------------------------------------------------------------------

    def _parse_skills(self, full_text: str, sections: dict[str, str]) -> list[str]:
        """
        Extract skills from: (a) dedicated skills section, (b) full text scan.
        Returns deduplicated sorted list.
        """
        skills_text = self._get_section(
            sections,
            "skills", "technical skills", "core competencies", "technologies",
        ) or ""

        search_text = (skills_text + "\n" + full_text).lower()
        found: set[str] = set()

        for skill in KNOWN_SKILLS:
            pattern = re.compile(r"(?<![a-z])" + re.escape(skill) + r"(?![a-z])", re.IGNORECASE)
            if pattern.search(search_text):
                found.add(skill.title())

        # Also parse skills section for unlisted comma/pipe/newline-separated tokens
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

    def _parse_educations(self, full_text: str, sections: dict[str, str]) -> list[dict[str, Any]]:
        edu_text = self._get_section(
            sections,
            "education", "academic background", "academic qualification",
        )

        if not edu_text:
            # Try to detect education anywhere in the text
            edu_text = self._find_education_block(full_text)

        if not edu_text:
            return []

        return self._parse_education_block(edu_text)

    def _find_education_block(self, text: str) -> str | None:
        """Find education-looking block by degree keywords."""
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
        """
        Handles formats:
        - "B.Tech · LIT Lucknow · 2022 – 2026"
        - "B.Tech in Computer Science\nLIT Lucknow\n2022 - 2026\nCGPA: 8.5"
        - "Bachelor of Technology (CSE), LIT Lucknow, 2022-2026"
        """
        results: list[dict[str, Any]] = []
        lines = _non_empty_lines(text)

        i = 0
        while i < len(lines):
            line = lines[i]

            # Detect degree line
            if _DEGREE_KEYWORDS.search(line) or _INSTITUTION_KEYWORDS.search(line):
                block_lines = [line]
                # Grab next few lines as part of this entry
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
        combined = " · ".join(block) if len(block) == 1 else "\n".join(block)

        # Try · delimiter first
        if "·" in combined:
            parts = [_clean_line(p) for p in combined.split("·") if _clean_line(p)]
        elif "," in combined and len(combined.split(",")) >= 2:
            parts = [_clean_line(p) for p in combined.split(",") if _clean_line(p)]
        else:
            parts = block

        degree = institution = field = None

        for part in parts:
            if not part:
                continue
            if _DEGREE_KEYWORDS.search(part) and not degree:
                degree = _YEAR_PATTERN_sub(part)  # remove year from degree
                # Extract field_of_study from parens: "B.Tech (Computer Science)"
                field_match = re.search(r"\(([^)]+)\)", part)
                if field_match:
                    field = _clean_line(field_match.group(1))
                    degree = re.sub(r"\([^)]+\)", "", degree).strip()
            elif _INSTITUTION_KEYWORDS.search(part) and not institution:
                institution = _YEAR_PATTERN_sub(part)
            elif not institution and not _YEAR.search(part) and len(part.split()) >= 2:
                institution = part

        years = _YEAR.findall(combined)
        start_year = int(years[0]) if years else None
        end_year = int(years[-1]) if len(years) >= 2 else None
        if start_year and end_year and start_year == end_year:
            end_year = None

        grade = self._extract_grade("\n".join(block))

        return {
            "degree": _limit(degree),
            "institution": _limit(institution),
            "field_of_study": _limit(field),
            "start_year": start_year,
            "end_year": end_year,
            "grade": grade,
        }

    def _parse_education_fallback(self, text: str) -> list[dict[str, Any]]:
        """Last-resort: return whatever we can extract as a single entry."""
        years = _YEAR.findall(text)
        return [{
            "degree": None,
            "institution": None,
            "field_of_study": None,
            "start_year": int(years[0]) if years else None,
            "end_year": int(years[-1]) if len(years) >= 2 else None,
            "grade": self._extract_grade(text),
        }]

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
            "experience", "work experience", "professional experience",
            "employment", "internship", "internships",
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

        # Fallback: return raw if we got nothing
        if not experiences:
            experiences = [{
                "company_name": None,
                "job_title": None,
                "location": None,
                "start_date": None,
                "end_date": None,
                "description": _limit(exp_text, 2000),
            }]

        return experiences

    def _split_experience_blocks(self, lines: list[str]) -> list[list[str]]:
        """
        Each experience starts with a line containing a company/title that
        doesn't start with a bullet and has a date range nearby.
        """
        blocks: list[list[str]] = []
        current: list[str] = []

        for line in lines:
            is_heading = (
                not _BULLET.match(line)
                and (_DATE_RANGE.search(line) or _YEAR.search(line))
                and len(line.split()) <= 12
            )

            if is_heading and current:
                blocks.append(current)
                current = [line]
            elif is_heading and not current:
                current = [line]
            else:
                if current:
                    current.append(line)

        if current:
            blocks.append(current)

        # Fallback: treat whole text as one block
        return blocks if blocks else [lines]

    def _parse_experience_block(self, block: list[str]) -> dict[str, Any] | None:
        if not block:
            return None

        heading = block[0]
        rest = block[1:]

        company, title, location = self._parse_experience_heading(heading, rest)
        start_date, end_date = self._extract_date_range("\n".join(block))
        description_lines = [
            _BULLET.sub("", l).strip()
            for l in rest
            if _BULLET.match(l) or (len(l.split()) > 5 and not _DATE_RANGE.search(l))
        ]
        description = " ".join(description_lines).strip()

        return {
            "company_name": _limit(company),
            "job_title": _limit(title),
            "location": _limit(location),
            "start_date": start_date,
            "end_date": end_date,
            "description": _limit(description, 2000) or None,
        }

    def _parse_experience_heading(
        self, heading: str, rest: list[str]
    ) -> tuple[str | None, str | None, str | None]:
        """
        Handles:
        - "Software Engineer · Acme Corp · Jan 2024 – Present · Remote"
        - "Acme Corp | Software Engineer | 2023 - 2024"
        - "Software Engineer Intern\nAcme Corp\nJan 2024 – Present"
        """
        # Remove date portions
        heading_clean = _DATE_RANGE.sub("", heading)
        heading_clean = _YEAR.sub("", heading_clean)
        heading_clean = re.sub(r"\s+", " ", heading_clean).strip(" |·-,")

        company = title = location = None

        for sep in ["·", "|", " - ", " – "]:
            if sep in heading_clean:
                parts = [_clean_line(p) for p in heading_clean.split(sep) if _clean_line(p)]
                if len(parts) >= 2:
                    # Heuristic: title usually has "engineer/developer/intern/analyst"
                    title_keywords = re.compile(
                        r"\b(engineer|developer|intern|analyst|designer|manager|"
                        r"lead|architect|consultant|associate|officer|executive|"
                        r"scientist|researcher|coordinator)\b",
                        re.IGNORECASE,
                    )
                    for idx, part in enumerate(parts):
                        if title_keywords.search(part) and not title:
                            title = part
                        elif idx != parts.index(title if title else parts[0]) and not company:
                            company = part
                    if not title and parts:
                        title = parts[0]
                    if not company and len(parts) >= 2:
                        company = parts[1]
                    if len(parts) >= 3 and not location:
                        remaining = [p for p in parts if p not in (title, company)]
                        if remaining:
                            location = remaining[0]
                    return company, title, location

        # No separator — heading might just be company or title
        # Check first line of rest for the other part
        if heading_clean:
            title = heading_clean
            if rest:
                next_line = _clean_line(rest[0])
                if next_line and not _BULLET.match(next_line) and not _DATE_RANGE.search(next_line or ""):
                    company = next_line

        return company, title, location

    def _extract_date_range(self, text: str) -> tuple[str | None, str | None]:
        m = _DATE_RANGE.search(text)
        if m:
            return _clean_line(m.group(1)), _clean_line(m.group(2))

        # Fallback: two bare years
        years = _YEAR.findall(text)
        if len(years) >= 2:
            return years[0], years[-1]
        if len(years) == 1:
            return years[0], None

        return None, None

    # -----------------------------------------------------------------------
    # Projects
    # -----------------------------------------------------------------------

    def _parse_projects(self, sections: dict[str, str]) -> list[dict[str, Any]]:
        projects_text = self._get_section(
            sections,
            "projects", "project", "academic projects",
            "personal projects", "key projects",
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
        PROJECT_HEADING_HINTS = [
            "personal project", "client project", "academic project",
            "freelance project", "major project", "minor project",
            "open source",
        ]

        blocks: list[list[str]] = []
        current: list[str] = []

        for line in lines:
            if self._is_project_heading(line, PROJECT_HEADING_HINTS):
                if current:
                    blocks.append(current)
                current = [line]
            elif current:
                current.append(line)

        if current:
            blocks.append(current)

        return blocks

    def _is_project_heading(self, line: str, hints: list[str]) -> bool:
        clean = _clean_line(line)
        if not clean:
            return False

        lower = clean.lower()

        # Never treat bullet lines as headings
        if _BULLET.match(clean):
            return False

        # Explicit hint match
        if any(h in lower for h in hints):
            return True

        # "ProjectName · Type · Year" pattern
        if "·" in clean and _YEAR.search(clean):
            return True

        # "ProjectName | Tech | Year" pattern
        if "|" in clean and _YEAR.search(clean):
            return True

        # Bold-like: ALL CAPS short line (≤6 words, no bullet)
        if re.match(r"^[A-Z][A-Z\s\-]{4,}$", clean) and len(clean.split()) <= 6:
            return True

        # Title-case short line followed by year on same line
        if _YEAR.search(clean) and re.match(r"^[A-Z][a-z]", clean) and len(clean.split()) <= 8:
            return True

        return False

    def _parse_project_block(self, block: list[str]) -> dict[str, Any] | None:
        if not block:
            return None

        heading = _clean_line(block[0])
        if not heading:
            return None

        # Extract name from heading
        heading_no_year = _YEAR.sub("", heading).strip(" ·|-,")
        parts = [_clean_line(p) for p in re.split(r"[·|]", heading_no_year) if _clean_line(p)]
        project_name = parts[0] if parts else heading_no_year

        body_lines = block[1:]

        technologies: str | None = None
        project_url: str | None = None
        description_lines: list[str] = []

        for idx, line in enumerate(body_lines):
            clean = _clean_line(line)
            if not clean:
                continue

            # URL detection
            url_match = _GITHUB.search(clean) or _PORTFOLIO.search(clean)
            if url_match and not project_url:
                project_url = _normalize_url(url_match.group())

            # First non-bullet line that looks like a tech stack
            if idx == 0 and self._looks_like_tech_stack(clean):
                technologies = clean
                continue

            # Description lines
            if _BULLET.match(clean):
                description_lines.append(_BULLET.sub("", clean).strip())
            else:
                description_lines.append(clean)

        description = _clean_line(" ".join(description_lines))

        return {
            "project_name": _limit(project_name),
            "technologies": _limit(technologies, 500),
            "project_url": _limit(project_url, 500),
            "description": _limit(description, 2000),
        }

    def _looks_like_tech_stack(self, line: str) -> bool:
        lower = line.lower()
        skill_hits = sum(1 for skill in KNOWN_SKILLS if skill in lower)
        has_separator = any(sep in line for sep in ["·", "|", ","])
        return skill_hits >= 2 or (skill_hits >= 1 and has_separator)


# ---------------------------------------------------------------------------
# Util
# ---------------------------------------------------------------------------

def _YEAR_PATTERN_sub(text: str) -> str:
    """Remove year occurrences from a string."""
    return _YEAR.sub("", text).strip(" ·-–,")