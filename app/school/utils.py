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
    
    