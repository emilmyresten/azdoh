from pathlib import Path


def check_if_file_exists(file: Path) -> bool:
    return file.exists() and file.is_file()
