import json
from pathlib import Path

import weaviate
import weaviate.classes as wvc

from collection_config import (
    COURSES_COLLECTION,
    INSTRUCTORS_COLLECTION,
    courses_schema_properties,
    instructors_schema_properties,
)
from project_config import connect_weaviate_client, load_environment_config


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def recreate_if_needed(client: weaviate.WeaviateClient, collection_name: str, reset: bool) -> None:
    exists = client.collections.exists(collection_name)
    if exists and reset:
        client.collections.delete(collection_name)


def ensure_schema(client: weaviate.WeaviateClient, reset_collections: bool) -> None:
    recreate_if_needed(client, INSTRUCTORS_COLLECTION, reset_collections)
    recreate_if_needed(client, COURSES_COLLECTION, reset_collections)

    config = load_environment_config()
    if config.llm_provider == "gemini":
        vectorizer_config = wvc.config.Configure.Vectorizer.text2vec_google_aistudio()
        generative_config = wvc.config.Configure.Generative.google_gemini(
            model="gemini-2.0-flash"
        )
    else:
        vectorizer_config = wvc.config.Configure.Vectorizer.text2vec_openai()
        generative_config = wvc.config.Configure.Generative.openai(model="gpt-4o-mini")

    if not client.collections.exists(INSTRUCTORS_COLLECTION):
        client.collections.create(
            name=INSTRUCTORS_COLLECTION,
            vectorizer_config=vectorizer_config,
            generative_config=generative_config,
            properties=instructors_schema_properties(),
        )

    if not client.collections.exists(COURSES_COLLECTION):
        client.collections.create(
            name=COURSES_COLLECTION,
            vectorizer_config=vectorizer_config,
            generative_config=generative_config,
            properties=courses_schema_properties(),
        )


def import_instructors(client: weaviate.WeaviateClient) -> int:
    data = load_json(DATA_DIR / "instructors.json")
    collection = client.collections.get(INSTRUCTORS_COLLECTION)

    with collection.batch.dynamic() as batch:
        for row in data:
            batch.add_object(properties=row)

    if collection.batch.failed_objects:
        raise RuntimeError(
            f"Failed to import instructors: {len(collection.batch.failed_objects)} objects"
        )

    return len(data)


def import_courses(client: weaviate.WeaviateClient) -> int:
    data = load_json(DATA_DIR / "courses.json")
    collection = client.collections.get(COURSES_COLLECTION)

    with collection.batch.dynamic() as batch:
        for row in data:
            batch.add_object(properties=row)

    if collection.batch.failed_objects:
        raise RuntimeError(
            f"Failed to import courses: {len(collection.batch.failed_objects)} objects"
        )

    return len(data)


def main() -> None:
    config = load_environment_config()
    client = connect_weaviate_client(config)

    try:
        ensure_schema(client, reset_collections=config.reset_collections)
        instructor_count = import_instructors(client)
        course_count = import_courses(client)

        print("Data modeling and import completed successfully.")
        print(f"Imported instructors: {instructor_count}")
        print(f"Imported courses: {course_count}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
