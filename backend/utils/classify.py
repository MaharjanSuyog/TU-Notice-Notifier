import re

ALLOWED_TAGS = [
    "exam",
    "result",
    "form_fill_up",
    "syllabus",
    "academic_calendar",
    "admission",
    "routine",
    "1st_sem",
    "2nd_sem",
    "3rd_sem",
    "4th_sem",
    "5th_sem",
    "6th_sem",
    "7th_sem",
    "8th_sem",
    "bsc_csit",
    "bit",
]

_ROMAN_TO_SEM = {
    "VIII": "8th_sem",
    "VII": "7th_sem",
    "VI": "6th_sem",
    "V": "5th_sem",
    "IV": "4th_sem",
    "III": "3rd_sem",
    "II": "2nd_sem",
    "I": "1st_sem",
}

_SEMESTER_PATTERN = re.compile(
    r"\b(VIII|VII|VI|V|IV|III|II|I)\s+Semester\b", re.IGNORECASE
)

_KEYWORD_TAGS = {
    "exam": ["exam", "examination"],
    "result": ["result", "नतिजा"],
    "form_fill_up": ["form fill", "form-fill"],
    "syllabus": ["syllabus", "curriculum"],
    "admission": ["admission", "entrance"],
    "routine": ["routine", "schedule"],
    "academic_calender": ["academic calendar"],
    "bsc_csit": ["b.sc.csit"],
    "bit": ["bit"],
}


def classify(title: str) -> list[str]:
    tags: set[str] = set()
    lower = title.lower()

    for tag, keywords in _KEYWORD_TAGS.items():
        if any(kw in lower for kw in keywords):
            tags.add(tag)

    if "result" in tags:
        tags.discard("exam")

    match = _SEMESTER_PATTERN.search(title)
    if match:
        sem_tag = _ROMAN_TO_SEM.get(match.group(1).upper())
        if sem_tag:
            tags.add(sem_tag)

    return sorted(t for t in tags if t in ALLOWED_TAGS)
