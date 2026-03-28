from dataclasses import dataclass
from uuid import UUID

from weaviate.agents.classes import Persona, PersonaInteraction
from weaviate.agents.personalization import PersonalizationAgent
from weaviate.classes.config import DataType
from weaviate.util import generate_uuid5

from collection_config import COURSES_COLLECTION
from personalization_profiles import PERSONA_PROFILES, PersonaProfile
from project_config import connect_weaviate_client, load_environment_config


@dataclass
class PersonalizedCourse:
    title: str
    department: str
    level: str
    language: str
    ects: int | None
    original_rank: int | None
    personalized_rank: int | None


@dataclass
class PersonalizationResult:
    profile_name: str
    rationale: str
    courses: list[PersonalizedCourse]


class UniversityPersonalizationExtension:
    def __init__(self) -> None:
        config = load_environment_config()
        self.client = connect_weaviate_client(config)
        self.agent = self._create_or_connect_agent()

    def close(self) -> None:
        self.client.close()

    def _create_or_connect_agent(self):
        if PersonalizationAgent.exists(self.client, COURSES_COLLECTION):
            return PersonalizationAgent.connect(
                client=self.client,
                reference_collection=COURSES_COLLECTION,
                vector_name="default",
            )

        return PersonalizationAgent.create(
            client=self.client,
            reference_collection=COURSES_COLLECTION,
            vector_name="default",
            user_properties={
                "preferred_departments": DataType.TEXT_ARRAY,
                "preferred_skills": DataType.TEXT_ARRAY,
                "preferred_language": DataType.TEXT,
                "preferred_level": DataType.TEXT,
            },
        )

    def _course_code_to_uuid_map(self) -> dict[str, UUID]:
        collection = self.client.collections.get(COURSES_COLLECTION)
        response = collection.query.fetch_objects(limit=500)
        mapping: dict[str, UUID] = {}

        for obj in response.objects:
            properties = obj.properties or {}
            course_code = properties.get("course_code")
            if course_code:
                mapping[course_code] = obj.uuid

        return mapping

    def _upsert_persona(self, profile: PersonaProfile) -> UUID:
        persona_id = generate_uuid5(f"persona:{profile.profile_id}")
        persona = Persona(persona_id=persona_id, properties=profile.to_properties())

        try:
            if self.agent.has_persona(persona_id):
                self.agent.update_persona(persona)
            else:
                self.agent.add_persona(persona)
        except Exception:
            self.agent.add_persona(persona)

        return persona_id

    def _sync_interactions(self, profile: PersonaProfile, persona_id: UUID) -> None:
        code_to_uuid = self._course_code_to_uuid_map()
        interactions: list[PersonaInteraction] = []

        for code, weight in profile.liked_courses.items():
            item_id = code_to_uuid.get(code)
            if item_id:
                interactions.append(
                    PersonaInteraction(
                        persona_id=persona_id,
                        item_id=item_id,
                        weight=weight,
                        replace_previous_interaction=True,
                    )
                )

        for code, weight in profile.disliked_courses.items():
            item_id = code_to_uuid.get(code)
            if item_id:
                interactions.append(
                    PersonaInteraction(
                        persona_id=persona_id,
                        item_id=item_id,
                        weight=weight,
                        replace_previous_interaction=True,
                    )
                )

        if interactions:
            self.agent.add_interactions(interactions)

    def recommend(
        self,
        profile_id: str,
        limit: int = 5,
        instruction: str | None = None,
        use_agent_ranking: bool = True,
    ) -> PersonalizationResult:
        if profile_id not in PERSONA_PROFILES:
            raise ValueError(f"Unknown profile_id: {profile_id}")

        profile = PERSONA_PROFILES[profile_id]
        persona_id = self._upsert_persona(profile)
        self._sync_interactions(profile, persona_id)

        response = self.agent.get_objects(
            persona_id=persona_id,
            limit=limit,
            recent_interactions_count=100,
            exclude_interacted_items=True,
            decay_rate=0.1,
            use_agent_ranking=use_agent_ranking,
            explain_results=True,
            instruction=instruction,
        )

        ranked_courses: list[PersonalizedCourse] = []
        for obj in response.objects:
            props = obj.properties or {}
            ranked_courses.append(
                PersonalizedCourse(
                    title=props.get("title", "N/A"),
                    department=props.get("department", "N/A"),
                    level=props.get("level", "N/A"),
                    language=props.get("language", "N/A"),
                    ects=props.get("ects"),
                    original_rank=getattr(obj, "original_rank", None),
                    personalized_rank=getattr(obj, "personalized_rank", None),
                )
            )

        rationale = getattr(response, "ranking_rationale", "") or "No rationale returned."

        return PersonalizationResult(
            profile_name=profile.display_name,
            rationale=rationale,
            courses=ranked_courses,
        )


def format_personalization_result(result: PersonalizationResult) -> str:
    lines: list[str] = []
    lines.append(f"Profile: {result.profile_name}")
    lines.append("")
    lines.append("Recommendations:")

    if not result.courses:
        lines.append("- No recommendations found.")
    else:
        for idx, course in enumerate(result.courses, start=1):
            lines.append(
                f"{idx}. {course.title} | {course.department} | {course.level} | "
                f"{course.language} | ECTS: {course.ects}"
            )
            lines.append(
                f"   original_rank={course.original_rank}, personalized_rank={course.personalized_rank}"
            )

    lines.append("")
    lines.append("Rationale:")
    lines.append(result.rationale)

    return "\n".join(lines)
