import hashlib
import json
from pathlib import Path


def calculate_md5(target_path: Path) -> str | None:
    """Returns the MD5 hash of a file or directory, or None if missing."""
    if not target_path.exists():
        return None

    hasher = hashlib.md5()

    # If it's a single file, hash it directly
    if target_path.is_file():
        _hash_file(target_path, hasher)
    # If it's a directory, hash all files inside it deterministically
    elif target_path.is_dir():
        for file_path in sorted(target_path.rglob("*")):
            if file_path.is_file():
                _hash_file(file_path, hasher)

    return hasher.hexdigest()


def _hash_file(file_path: Path, hasher):
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)


def load_manifest() -> dict:
    manifest_path = Path(__file__).parent / "manifest.json"
    with open(manifest_path, "r") as f:
        return json.load(f)
