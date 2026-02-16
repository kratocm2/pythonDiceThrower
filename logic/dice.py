import random

def roll_dice(count: int, sides: int) -> list[int]:
    """Roll dice and return list of results."""
    return [random.randint(1, sides) for _ in range(count)]

def calculate_total(rolls: list[int]) -> int:
    """Return sum of rolls."""
    return sum(rolls)