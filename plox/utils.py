def display_error(line: int, location: str, message: str):
    print(f"[Line {line}] Error: {location}: {message}")


def log(line: int, location: str, message: str):
    print(f"[Line {line}] Info: {location}: {message}")
