def display_error(line: int, message: str):
    log(line, "", message)


def log(line: int, location: str, message: str):
    print(f'[Line {line}] Error: {location}: {message}')
