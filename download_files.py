#!/usr/bin/env python3
"""
Download files specified in downloads_config.json into the configured downloads directory.

SharePoint sharing links are resolved by appending '?download=1' to trigger a direct
file download, following any redirects automatically.
"""

import json
import os
import sys

import requests


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "downloads_config.json")
DOWNLOAD_TIMEOUT_SECONDS = 120


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_download_url(share_url: str) -> str:
    """Append the download=1 query parameter to a SharePoint sharing URL."""
    separator = "&" if "?" in share_url else "?"
    return f"{share_url}{separator}download=1"


def download_file(description: str, filename: str, share_url: str, dest_dir: str) -> bool:
    """
    Download a single file from a SharePoint sharing link.

    Returns True on success, False on failure.
    """
    dest_path = os.path.join(dest_dir, filename)
    download_url = build_download_url(share_url)

    print(f"Downloading: {description}")
    print(f"  URL : {share_url}")
    print(f"  Dest: {dest_path}")

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        with requests.get(download_url, headers=headers, stream=True, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
            response.raise_for_status()
            with open(dest_path, "wb") as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
        size = os.path.getsize(dest_path)
        print(f"  Done ({size:,} bytes)\n")
        return True
    except requests.RequestException as exc:
        print(f"  ERROR: {exc}\n", file=sys.stderr)
        return False


def main() -> int:
    config = load_config(CONFIG_FILE)
    downloads_dir = config["downloads_dir"]

    os.makedirs(downloads_dir, exist_ok=True)

    files = config["files"]
    total = len(files)
    succeeded = 0

    for entry in files:
        ok = download_file(
            description=entry["description"],
            filename=entry["filename"],
            share_url=entry["url"],
            dest_dir=downloads_dir,
        )
        if ok:
            succeeded += 1

    print(f"Downloaded {succeeded}/{total} files into '{downloads_dir}/'.")
    return 0 if succeeded == total else 1


if __name__ == "__main__":
    sys.exit(main())
