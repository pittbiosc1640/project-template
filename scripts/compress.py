import json
import sys
import tarfile
from pathlib import Path

from utils import calculate_md5, load_manifest


def main():
    config = load_manifest()
    assets = config["assets"]

    print("Generating MD5 checksums and archives...")
    checksums = {}

    for archive_name, target_path_str in assets.items():
        target_path = Path(target_path_str)

        if not target_path.exists():
            print(f"Error: Target {target_path} does not exist.")
            sys.exit(1)

        checksums[target_path_str] = calculate_md5(target_path)

        archive_path = target_path.parent / archive_name

        print(f"  Compressing {target_path_str} -> {archive_path}...")
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(target_path, arcname=target_path.name)

    with open("checksums.json", "w") as f:
        json.dump(checksums, f, indent=2)

    print("Compression complete. Archives and checksums are ready for inspection.")


if __name__ == "__main__":
    main()
