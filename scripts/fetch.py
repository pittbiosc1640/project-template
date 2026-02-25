import argparse
import subprocess
import tarfile
from pathlib import Path

from utils import load_manifest


def main():
    config = load_manifest()
    repo = config["repo"]
    assets = config["assets"]
    available_assets = list(assets.keys())

    parser = argparse.ArgumentParser(
        description="Fetch data dependencies from GitHub Releases."
    )
    parser.add_argument(
        "assets",
        nargs="*",
        help=f"Specific archives to download. Leave blank for all. Available: {', '.join(available_assets)}",
    )
    args = parser.parse_args()

    targets = args.assets if args.assets else available_assets

    for archive_name in targets:
        if archive_name not in available_assets:
            print(f"Warning: {archive_name} is not in the manifest. Skipping.")
            continue

        target_path_str = assets[archive_name]
        target_path = Path(target_path_str)

        extract_dir = target_path.parent

        extract_dir.mkdir(parents=True, exist_ok=True)

        archive_path = extract_dir / archive_name

        print(f"Downloading {archive_name} into {extract_dir}...")
        subprocess.run(
            [
                "gh",
                "release",
                "download",
                "--repo",
                repo,
                "--pattern",
                archive_name,
                "--dir",
                str(extract_dir),
                "--clobber",
            ],
            check=True,
        )

        print(f"Extracting {archive_name}...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=extract_dir)

        archive_path.unlink()

    print("\nData fetch complete.")


if __name__ == "__main__":
    main()
