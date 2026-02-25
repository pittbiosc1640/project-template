import json
import subprocess
import sys
import tempfile
from pathlib import Path

from utils import calculate_md5, load_manifest


def main():
    config = load_manifest()
    repo = config["repo"]
    assets = config["assets"]

    print("Fetching latest checksums from GitHub...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        try:
            subprocess.run(
                [
                    "gh",
                    "release",
                    "download",
                    "--repo",
                    repo,
                    "--pattern",
                    "checksums.json",
                    "--dir",
                    str(tmp_path),
                    "--clobber",
                ],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            print("No previous release found or unable to download checksums.")
            sys.exit(1)

        with open(tmp_path / "checksums.json", "r") as f:
            remote_checksums = json.load(f)

    differences = False
    print("Comparing local paths against latest release...")

    for archive_name, target_path_str in assets.items():
        target_path = Path(target_path_str)
        local_hash = calculate_md5(target_path)
        remote_hash = remote_checksums.get(target_path_str)

        if local_hash is None:
            print(f"  [MISSING LOCAL] {target_path_str} (Target for {archive_name})")
            differences = True
        elif local_hash != remote_hash:
            print(f"  [CHANGED]       {target_path_str} (Target for {archive_name})")
            differences = True
        else:
            print(f"  [MATCH]         {target_path_str}")

    if not differences:
        print("\nLocal data matches the latest release. No new release needed.")
    else:
        print("\nChanges detected! You should cut a new release soon.")
        sys.exit(1)


if __name__ == "__main__":
    main()
