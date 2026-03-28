from pathlib import Path

REQUIRED_FILES = [
    "src/load_data.py",
    "src/query_agent.py",
    "src/query_agent_demo.py",
    "src/personalization_demo.py",
    "src/app.py",
    "src/project_config.py",
    "src/collection_config.py",
    "src/demo_queries.py",
    "src/personalization_profiles.py",
    "src/personalization_agent.py",
    "src/data/courses.json",
    "src/data/instructors.json",
]


def main() -> None:
    print("=== Demo Readiness Check ===")
    missing = []

    for file_path in REQUIRED_FILES:
        exists = Path(file_path).exists()
        status = "OK" if exists else "MISSING"
        print(f"[{status}] {file_path}")
        if not exists:
            missing.append(file_path)

    print("\nSuggested demo commands:")
    print("1) python src/load_data.py")
    print("2) python src/query_agent_demo.py")
    print("3) python src/personalization_demo.py")
    print("4) streamlit run src/app.py")

    if missing:
        print("\nResult: NOT READY")
        print("Missing files:")
        for item in missing:
            print(f"- {item}")
    else:
        print("\nResult: READY")


if __name__ == "__main__":
    main()
