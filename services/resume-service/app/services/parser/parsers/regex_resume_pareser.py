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
        r"(https?://)?(www\.)?github\.com/[A-Za-z0-9_-]+/?",
        re.IGNORECASE,
    )

    KNOWN_SKILLS = {
        "python", "java", "javascript", "typescript", "c++", "c",
        "fastapi", "django", "flask", "react", "next.js", "node.js",
        "postgresql", "mysql", "mongodb", "redis",
        "docker", "kubernetes", "aws", "git", "github",
        "html", "css", "tailwind", "sql",
        "machine learning", "deep learning", "pandas", "numpy",
    }

    BLOCKED_NAME_WORDS = {
        "resume",
        "curriculum vitae",
        "cv",
        "email",
        "phone",
        "mobile",
        "skills",
        "education",
        "experience",
        "projects",
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

    async def parse(self, text: str) -> dict[str, Any]:
        logger.info(
            "Starting regex resume parsing",
            extra={
                "text_length": len(text) if text else 0,
            },
        )

        cleaned_text = self._clean_text(text)

        parsed_data = {
            "full_name": self._extract_full_name(cleaned_text),
            "email": self._extract_email(cleaned_text),
            "phone": self._extract_phone(cleaned_text),
            "linkedin_url": self._extract_linkedin(cleaned_text),
            "github_url": self._extract_github(cleaned_text),
            "skills": self._extract_skills(cleaned_text),
            "education": self._extract_section(
                cleaned_text,
                ["education", "academic"],
            ),
            "experience": self._extract_section(
                cleaned_text,
                ["experience", "work experience", "employment"],
            ),
            "projects": self._extract_section(
                cleaned_text,
                ["projects", "project"],
            ),
        }

        logger.info(
            "Regex resume parsing completed",
            extra={
                "has_full_name": bool(parsed_data["full_name"]),
                "has_email": bool(parsed_data["email"]),
                "has_phone": bool(parsed_data["phone"]),
                "has_linkedin": bool(parsed_data["linkedin_url"]),
                "has_github": bool(parsed_data["github_url"]),
                "skills_count": len(parsed_data["skills"]),
                "has_education": bool(parsed_data["education"]),
                "has_experience": bool(parsed_data["experience"]),
                "has_projects": bool(parsed_data["projects"]),
            },
        )

        return parsed_data

    def _clean_text(self, text: str) -> str:
        if not text:
            logger.warning("Empty text received for resume parsing")
            return ""

        cleaned_text = re.sub(r"\r\n|\r", "\n", text)
        cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
        cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

        return cleaned_text.strip()

    def _extract_email(self, text: str) -> str | None:
        match = self.EMAIL_PATTERN.search(text)

        if not match:
            logger.debug("Email not found in resume text")
            return None

        return match.group().strip().lower()

    def _extract_phone(self, text: str) -> str | None:
        match = self.PHONE_PATTERN.search(text)

        if not match:
            logger.debug("Phone number not found in resume text")
            return None

        phone = match.group().strip()

        return re.sub(r"[^\d+]", "", phone)

    def _extract_linkedin(self, text: str) -> str | None:
        match = self.LINKEDIN_PATTERN.search(text)

        if not match:
            logger.debug("LinkedIn URL not found in resume text")
            return None

        return self._normalize_url(match.group())

    def _extract_github(self, text: str) -> str | None:
        match = self.GITHUB_PATTERN.search(text)

        if not match:
            logger.debug("GitHub URL not found in resume text")
            return None

        return self._normalize_url(match.group())

    def _normalize_url(self, url: str) -> str:
        normalized_url = url.strip()

        if not normalized_url.startswith(("http://", "https://")):
            return f"https://{normalized_url}"

        return normalized_url

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

        logger.debug("Full name not found in resume text")
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

        logger.debug(
            "Section not found in resume text",
            extra={
                "section_names": section_names,
            },
        )

        return None