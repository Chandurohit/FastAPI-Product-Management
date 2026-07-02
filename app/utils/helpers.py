# Reusable utility and helper functions

def parse_int_safe(val: str, default: int = 0) -> int:
    """Safely parse a string value to an integer, returning default if parsing fails."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return default
