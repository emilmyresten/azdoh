import uuid

from pathlib import Path


def create_tmp_dir() -> Path:
    tmp_dir = Path("azdoh-tmp")
    tmp_dir.mkdir(exist_ok=True)
    return tmp_dir


def write_content_to_tmp_file(script: str) -> Path:
    tmp_file = create_tmp_file()
    with open(tmp_file, "w") as tf:
        tf.write(script)
    return tmp_file


def create_tmp_file() -> Path:
    tmp_file = Path(f"azdoh-tmp/tmp_file-{str(uuid.uuid4())}")
    tmp_file.touch()
    return tmp_file


def delete_tmp_file(tmp_file: Path):
    tmp_file.unlink()


def delete_tmp_dir(tmp_dir: Path):
    """
    Requires the directory to be empty, i.e. each tmp_file needs to be created and then cleaned up.
    """
    tmp_dir.rmdir()
