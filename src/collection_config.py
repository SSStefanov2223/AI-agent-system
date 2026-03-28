import weaviate.classes as wvc
from weaviate.agents.classes import QueryAgentCollectionConfig


COURSES_COLLECTION = "Courses"
INSTRUCTORS_COLLECTION = "Instructors"

COURSE_VIEW_PROPERTIES = [
    "course_code",
    "title",
    "description",
    "department",
    "level",
    "ects",
    "language",
    "semester",
    "skills",
    "instructor_id",
]

INSTRUCTOR_VIEW_PROPERTIES = [
    "instructor_id",
    "full_name",
    "department",
    "bio",
    "research_interests",
    "years_experience",
]


def instructors_schema_properties() -> list[wvc.config.Property]:
    return [
        wvc.config.Property(name="instructor_id", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="full_name", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="department", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="bio", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(
            name="research_interests",
            data_type=wvc.config.DataType.TEXT_ARRAY,
        ),
        wvc.config.Property(
            name="years_experience",
            data_type=wvc.config.DataType.INT,
        ),
    ]


def courses_schema_properties() -> list[wvc.config.Property]:
    return [
        wvc.config.Property(name="course_code", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="description", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="department", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="level", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="ects", data_type=wvc.config.DataType.INT),
        wvc.config.Property(name="language", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="semester", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="skills", data_type=wvc.config.DataType.TEXT_ARRAY),
        wvc.config.Property(name="instructor_id", data_type=wvc.config.DataType.TEXT),
    ]


def query_agent_collections() -> list[QueryAgentCollectionConfig]:
    return [
        QueryAgentCollectionConfig(
            name=COURSES_COLLECTION,
            view_properties=COURSE_VIEW_PROPERTIES,
        ),
        QueryAgentCollectionConfig(
            name=INSTRUCTORS_COLLECTION,
            view_properties=INSTRUCTOR_VIEW_PROPERTIES,
        ),
    ]
