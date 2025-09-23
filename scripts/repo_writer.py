"""Repo writer: reconstructs the repository files from embedded markers.
This script is itself a writer; for now it will simply print the current manifest.
"""
import os, json
from pathlib import Path

def manifest(root):
    files = []
    for p in Path(root).rglob('*'):
        if p.is_file():
            files.append(str(p.relative_to(root)))
    return files

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print("Repository manifest for:", root)
    for f in manifest(root):
        print(" -", f)
