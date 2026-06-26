import logging
import re
from typing import Any

from app.services.parser.interface.resume_parser import ResumeParserInterface


logger = logging.getLogger(__name__)


class RegexResumeParser(ResumeParserInterface):
    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    PHONE_PATTERN = re.compile(
        r"(?:\+?\d{1,3}[\s-]?)?"
        r"(?:\(?\d{3,5}\)?[\s-]?)?"
        r"\d{5}[\s-]?\d{5}"
    )

    LINKEDIN_PATTERN = re.compile(
        r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?",
        re.IGNORECASE,
    )

    GITHUB_PATTERN = re.compile(
        r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_./-]+/?",
        re.IGNORECASE,
    )

    YEAR_PATTERN = re.compile(r"\b(?:19|20)\d{2}\b")

    BULLET_PATTERN = re.compile(r"^[•\-\*]\s*")

    KNOWN_SKILLS = {
        "python", "java", "javascript", "typescript", "c++", "c",
        "fastapi", "django", "flask", "react", "next.js", "node.js",
        "postgresql", "mysql", "mongodb", "redis",
        "docker", "kubernetes", "aws", "git", "github",
        "html", "css", "tailwind", "sql",
        "machine learning", "deep learning", "pandas", "numpy",
        "sqlalchemy", "alembic", "jwt", "websockets", "redux",
    }

    SECTION_HEADERS = [
        "education",
        "academic",
        "experience",
        "work experience",
        "employment",
        "projects",
        "project",
        "skills",
        "technical skills",
        "certifications",
        "achievements",
    ]

    BLOCKED_NAME_WORDS = {
        "resume", "curriculum vitae", "cv", "email", "phone",
        "mobile", "skills", "education", "experience", "projects",
    }

    PROJECT_HEADER_HINTS = [
        "personal project",
        "client project",
        "academic project",
        "freelance project",
        "major project",
        "minor project",
    ]

    async def parse(self, text: str) -> dict[str, Any]:
        cleaned_text = self._clean_text(text)

        parsed_data = {
            "profile": {
                "full_name": self._extract_full_name(cleaned_text),
                "email": self._extract_email(cleaned_text),
                "phone": self._extract_phone(cleaned_text),
                "linkedin_url": self._extract_linkedin(cleaned_text),
                "github_url": self._extract_github(cleaned_text),
                "professional_summary": None,
            },
            "skills": self._extract_skills(cleaned_text),
            "educations": self._extract_educations(cleaned_text),
            "experiences": self._extract_experiences(cleaned_text),
            "projects": self._extract_projects(cleaned_text),
        }

        logger.info(
            "Regex resume parsing completed",
            extra={
                "skills_count": len(parsed_data["skills"]),
                "educations_count": len(parsed_data["educations"]),
                "experiences_count": len(parsed_data["experiences"]),
                "projects_count": len(parsed_data["projects"]),
            },
        )

        return parsed_data

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.replace("\u200b", "")
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def _clean_line(self, value: str | None) -> str | None:
        if not value:
            return None

        value = value.replace("\u200b", "")
        value = re.sub(r"\s+", " ", value)
        return value.strip(" |,-•\n\t")

    def _limit(self, value: str | None, max_length: int = 255) -> str | None:
        value = self._clean_line(value)

        if not value:
            return None

        return value[:max_length]

    def _extract_email(self, text: str) -> str | None:
        match = self.EMAIL_PATTERN.search(text)
        return match.group().strip().lower() if match else None

    def _extract_phone(self, text: str) -> str | None:
        match = self.PHONE_PATTERN.search(text)

        if not match:
            return None

        return re.sub(r"[^\d+]", "", match.group().strip())

    def _extract_linkedin(self, text: str) -> str | None:
        match = self.LINKEDIN_PATTERN.search(text)
        return self._normalize_url(match.group()) if match else None

    def _extract_github(self, text: str) -> str | None:
        match = self.GITHUB_PATTERN.search(text)
        return self._normalize_url(match.group()) if match else None

    def _normalize_url(self, url: str) -> str:
        url = url.strip()

        if not url.startswith(("http://", "https://")):
            return f"https://{url}"

        return url

    def _extract_full_name(self, text: str) -> str | None:
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines[:8]:
            clean_line = re.sub(r"[^A-Za-z\s]", "", line).strip()

            if not clean_line:
                continue

            if clean_line.lower() in self.BLOCKED_NAME_WORDS:
                continue

            words = clean_line.split()

            if 2 <= len(words) <= 4:
                return clean_line.title()

        return None

    def _extract_skills(self, text: str) -> list[str]:
        lower_text = text.lower()
        found_skills: set[str] = set()

        for skill in self.KNOWN_SKILLS:
            pattern = re.compile(
                r"\b" + re.escape(skill) + r"\b",
                re.IGNORECASE,
            )

            if pattern.search(lower_text):
                found_skills.add(skill.title())

        return sorted(found_skills)

    def _extract_educations(self, text: str) -> list[dict[str, Any]]:
        education_text = self._extract_section(
            text,
            ["education", "academic"],
        )

        if not education_text:
            return []

        lines = self._non_empty_lines(education_text)

        if not lines:
            return []

        first_line = lines[0]

        # Example:
        # Bachelor of Technology (B.Tech) · Dr. A.P.J Abdul Kalam Technical University2022 – 2026 · Lucknow, India
        parts = [
            self._clean_line(part)
            for part in first_line.split("·")
            if self._clean_line(part)
        ]

        degree = parts[0] if len(parts) >= 1 else None
        institution = parts[1] if len(parts) >= 2 else None

        if institution:
            institution = self.YEAR_PATTERN.split(institution)[0].strip()

        years = self.YEAR_PATTERN.findall(education_text)

        start_year = int(years[0]) if years else None
        end_year = int(years[-1]) if years else None

        return [
            {
                "degree": self._limit(degree),
                "institution": self._limit(institution),
                "field_of_study": None,
                "start_year": start_year,
                "end_year": end_year,
                "grade": self._extract_grade(education_text),
            }
        ]

    def _extract_grade(self, text: str) -> str | None:
        patterns = [
            r"\bCGPA[:\s]+([0-9.]+)",
            r"\bGPA[:\s]+([0-9.]+)",
            r"\bSGPA[:\s]+([0-9.]+)",
            r"\bPercentage[:\s]+([0-9.]+%?)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return self._limit(match.group(1), 50)

        return None

    def _extract_experiences(self, text: str) -> list[dict[str, Any]]:
        experience_text = self._extract_section(
            text,
            ["experience", "work experience", "employment"],
        )

        if not experience_text:
            return []

        return [
            {
                "company_name": None,
                "job_title": None,
                "location": None,
                "start_date": None,
                "end_date": None,
                "description": experience_text,
            }
        ]

    def _extract_projects(self, text: str) -> list[dict[str, Any]]:
        projects_text = self._extract_section(
            text,
            ["projects", "project"],
        )

        if not projects_text:
            return []

        lines = self._non_empty_lines(projects_text)

        if not lines:
            return []

        project_blocks = self._split_project_blocks(lines)

        projects: list[dict[str, Any]] = []

        for block in project_blocks:
            project = self._parse_project_block(block)

            if project:
                projects.append(project)

        return projects

    def _split_project_blocks(self, lines: list[str]) -> list[list[str]]:
        blocks: list[list[str]] = []
        current_block: list[str] = []

        for line in lines:
            if self._is_project_heading(line):
                if current_block:
                    blocks.append(current_block)

                current_block = [line]
                continue

            if current_block:
                current_block.append(line)

        if current_block:
            blocks.append(current_block)

        return blocks

    def _is_project_heading(self, line: str) -> bool:
        clean_line = self._clean_line(line)

        if not clean_line:
            return False

        lower_line = clean_line.lower()

        if self.BULLET_PATTERN.match(clean_line):
            return False

        if any(hint in lower_line for hint in self.PROJECT_HEADER_HINTS):
            return True

        # Example: Library Management System · Personal Project2025
        if "·" in clean_line and self.YEAR_PATTERN.search(clean_line):
            return True

        return False

    def _parse_project_block(self, block: list[str]) -> dict[str, Any] | None:
        if not block:
            return None

        heading = self._clean_line(block[0])

        if not heading:
            return None

        heading_parts = [
            self._clean_line(part)
            for part in heading.split("·")
            if self._clean_line(part)
        ]

        project_name = heading_parts[0] if heading_parts else heading

        body_lines = block[1:]

        technologies = None
        project_url = None
        description_lines: list[str] = []

        for index, line in enumerate(body_lines):
            clean_line = self._clean_line(line)

            if not clean_line:
                continue

            url_match = self.GITHUB_PATTERN.search(clean_line)

            if url_match and not project_url:
                project_url = self._normalize_url(url_match.group())

            if index == 0 and self._looks_like_tech_stack(clean_line):
                technologies = clean_line
                continue

            if self.BULLET_PATTERN.match(clean_line):
                description_lines.append(
                    self.BULLET_PATTERN.sub("", clean_line).strip()
                )
            else:
                description_lines.append(clean_line)

        description = " ".join(description_lines)
        description = self._clean_line(description)

        return {
            "project_name": self._limit(project_name),
            "technologies": self._limit(technologies, 500),
            "project_url": self._limit(project_url, 500),
            "description": description,
        }

    def _looks_like_tech_stack(self, line: str) -> bool:
        lower_line = line.lower()

        skill_hits = sum(
            1
            for skill in self.KNOWN_SKILLS
            if skill in lower_line
        )

        has_separator = "·" in line or "|" in line or "," in line

        return skill_hits >= 2 or has_separator

    def _non_empty_lines(self, text: str) -> list[str]:
        return [
            self._clean_line(line)
            for line in text.splitlines()
            if self._clean_line(line)
        ]

    def _extract_first_year(self, text: str) -> int | None:
        years = self.YEAR_PATTERN.findall(text)
        return int(years[0]) if years else None

    def _extract_last_year(self, text: str) -> int | None:
        years = self.YEAR_PATTERN.findall(text)
        return int(years[-1]) if years else None

    def _extract_section(
        self,
        text: str,
        section_names: list[str],
    ) -> str | None:
        section_pattern = "|".join(
            re.escape(section)
            for section in self.SECTION_HEADERS
        )

        for section_name in section_names:
            pattern = re.compile(
                rf"\b{re.escape(section_name)}\b\s*[:\-]?\s*"
                rf"(.*?)(?=\n\s*(?:{section_pattern})\b|$)",
                re.DOTALL | re.IGNORECASE,
            )

            match = pattern.search(text)

            if match:
                section_text = match.group(1).strip()
                return section_text if section_text else None

        return None