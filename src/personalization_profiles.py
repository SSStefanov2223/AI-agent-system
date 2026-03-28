from dataclasses import dataclass


@dataclass(frozen=True)
class PersonaProfile:
    profile_id: str
    display_name: str
    preferred_departments: list[str]
    preferred_skills: list[str]
    preferred_language: str
    preferred_level: str
    liked_courses: dict[str, float]
    disliked_courses: dict[str, float]

    def to_properties(self) -> dict:
        return {
            "preferred_departments": self.preferred_departments,
            "preferred_skills": self.preferred_skills,
            "preferred_language": self.preferred_language,
            "preferred_level": self.preferred_level,
        }


PERSONA_PROFILES: dict[str, PersonaProfile] = {
    "ai_career": PersonaProfile(
        profile_id="ai_career",
        display_name="AI Career Starter",
        preferred_departments=["Computer Science", "Data Science"],
        preferred_skills=["python", "machine learning", "nlp", "deep learning"],
        preferred_language="English",
        preferred_level="Bachelor",
        liked_courses={"CS301": 0.95, "CS410": 0.85, "DS402": 0.7},
        disliked_courses={"SE415": -0.4},
    ),
    "backend_scale": PersonaProfile(
        profile_id="backend_scale",
        display_name="Backend & Scale Engineer",
        preferred_departments=["Computer Science", "Software Engineering"],
        preferred_skills=["distributed systems", "microservices", "architecture"],
        preferred_language="English",
        preferred_level="Bachelor",
        liked_courses={"CS350": 0.95, "SE330": 0.9, "CS210": 0.65},
        disliked_courses={"DS220": -0.3},
    ),
    "data_analyst_bg": PersonaProfile(
        profile_id="data_analyst_bg",
        display_name="Data Analyst (BG)",
        preferred_departments=["Data Science", "Information Systems"],
        preferred_skills=["analytics", "sql", "data mining", "evaluation"],
        preferred_language="Bulgarian",
        preferred_level="Bachelor",
        liked_courses={"DS220": 0.95, "IS340": 0.85, "IS305": 0.5},
        disliked_courses={"CS410": -0.4},
    ),
}


PERSONA_OPTION_LABELS = {
    profile_id: profile.display_name for profile_id, profile in PERSONA_PROFILES.items()
}
