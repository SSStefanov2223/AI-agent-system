from personalization_agent import (
    UniversityPersonalizationExtension,
    format_personalization_result,
)
from personalization_profiles import PERSONA_OPTION_LABELS


def run_personalization_demo() -> None:
    extension = UniversityPersonalizationExtension()

    try:
        print("=== Personalization Agent Demo ===")
        for profile_id, label in PERSONA_OPTION_LABELS.items():
            print(f"\n--- Profile: {label} ---")
            result = extension.recommend(
                profile_id=profile_id,
                limit=3,
                instruction="Prioritize practical, career-relevant courses.",
                use_agent_ranking=True,
            )
            print(format_personalization_result(result))
        print("\n=== Personalization demo complete ===")
    finally:
        extension.close()


if __name__ == "__main__":
    run_personalization_demo()
