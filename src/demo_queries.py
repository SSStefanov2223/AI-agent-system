DEMO_QUERY_ITEMS = [
    (
        "1) Ordinary search",
        "Find courses about machine learning or NLP with practical focus.",
    ),
    (
        "2) Multi-collection",
        "Which instructor teaches courses related to distributed systems and what is their research focus?",
    ),
    (
        "3) Follow-up",
        "Can you suggest 2 alternative courses from the same department and explain the difference?",
    ),
    (
        "4) Filter/Aggregation",
        "For English-language courses only, what is the average ECTS and how many such courses are there?",
    ),
    (
        "5) Free-form",
        "I want something future-proof for AI + software career, not too theoretical. What should I take first?",
    ),
]

DEMO_QUERIES = {
    "ordinary_search": DEMO_QUERY_ITEMS[0][1],
    "multi_collection": DEMO_QUERY_ITEMS[1][1],
    "follow_up": DEMO_QUERY_ITEMS[2][1],
    "filter_or_aggregation": DEMO_QUERY_ITEMS[3][1],
    "free_form": DEMO_QUERY_ITEMS[4][1],
}
