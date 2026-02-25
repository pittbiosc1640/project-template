import subprocess
import sys
import tomllib
from pathlib import Path

from utils import load_manifest


def get_project_version() -> str:
    pixi_path = Path("pixi.toml")
    if not pixi_path.exists():
        print("Error: pixi.toml not found. Run this from the project root.")
        sys.exit(1)

    with open(pixi_path, "rb") as f:
        return tomllib.load(f)["workspace"]["version"]


def main():
    config = load_manifest()
    repo = config["repo"]
    assets = config["assets"]

    version = get_project_version()
    tag = f"v{version}"

    files_to_upload = [Path("checksums.json")]
    for archive_name, target_path_str in assets.items():
        archive_path = Path(target_path_str).parent / archive_name
        files_to_upload.append(archive_path)

    for f in files_to_upload:
        if not f.exists():
            print(f"Error: Expected file {f} not found. Did you run compress.py first?")
            sys.exit(1)

    print(f"Creating GitHub release {tag}...")

    gh_command = (
        ["gh", "release", "create", tag]
        + [str(f) for f in files_to_upload]
        + [
            "--repo",
            repo,
            "--title",
            f"{tag}",
            "--notes",
            f"Automated release for version {version}.",
        ]
    )

    subprocess.run(gh_command, check=True)

    print("Cleaning up local archives...")
    for f in files_to_upload:
        f.unlink()

    print(f"Successfully published {tag}.")


if __name__ == "__main__":
    main()
