GRADE_MAPPING = {
    "AD": 4,
    "A": 3,
    "B": 2,
    "C": 1,
    "NA": 0
}

def get_from_alphabetical_to_numeric(value: str) -> int:
    """
    Convert an alphabetical grade (e.g., 'C', 'B', 'A' 'AD') to a numeric value.
    """
    return GRADE_MAPPING.get(value, 0)  # Default to 0 if not found
def get_from_numeric_to_alphabetical(value: int) -> str:
    """
    Convert a numeric grade (e.g., 4, 3, 2, 1) to an alphabetical value.
    """
    for key, val in GRADE_MAPPING.items():
        if val == value:
            return key
    return "NA"  # Default to 'NA' if not found
    # instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='categories')
    # title = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # weight = models.FloatField(null=True, blank=True)
DEFAULT_CATEGORIES = [
    {
        "title": "Tarea",
        "weight": 0.1,
    },
    {
        "title": "Examen",
        "weight": 0.4,
    },
    {
        "title": "Proyecto",
        "weight": 0.25,
    },
    {
        "title": "Evaluación",
        "weight": 0.2,
    },
    {
        "title": "Trabajo en clase",
        "weight": 0.05,
    },
]
    
    