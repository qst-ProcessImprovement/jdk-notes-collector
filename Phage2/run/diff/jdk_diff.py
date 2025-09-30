from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Mapping

DEFAULT_TEMURIN_PATH = Path("Phage2/run/temurin/output_temurin/jdk-21.0.8.txt")
DEFAULT_OPENJDK_PATH = Path("Phage2/run/openjdk/output_openjdk/jdk-21.0.8.txt")
DEFAULT_OUTPUT_DIR = Path("Phage2/run/diff/output")
TEMURIN_ONLY_FILENAME = "temurin_only.txt"
OPENJDK_ONLY_FILENAME = "openjdk_only.txt"


def read_identifiers(file_path: Path) -> set[str]:
    """Return the set of non-empty identifiers from the given file."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    identifiers: set[str] = set()
    with file_path.open("r", encoding="utf-8") as reader:
        for raw_line in reader:
            identifier = raw_line.strip()
            if identifier:
                identifiers.add(identifier)
    return identifiers


def write_identifiers(identifiers: Iterable[str], output_path: Path) -> None:
    """Write identifiers to the given path, one per line."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as writer:
        for identifier in sorted(set(identifiers)):
            writer.write(f"{identifier}\n")


def compute_differences(
    temurin_identifiers: set[str],
    openjdk_identifiers: set[str],
) -> Mapping[str, set[str]]:
    """Compute directional set differences for the two inputs."""
    return {
        "temurin_only": temurin_identifiers - openjdk_identifiers,
        "openjdk_only": openjdk_identifiers - temurin_identifiers,
    }


def collect_jdk_diff(
    temurin_path: Path = DEFAULT_TEMURIN_PATH,
    openjdk_path: Path = DEFAULT_OPENJDK_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Mapping[str, Path]:
    """Generate diff files and return their paths."""
    temurin_identifiers = read_identifiers(temurin_path)
    openjdk_identifiers = read_identifiers(openjdk_path)

    differences = compute_differences(temurin_identifiers, openjdk_identifiers)

    temurin_only_path = output_dir / TEMURIN_ONLY_FILENAME
    openjdk_only_path = output_dir / OPENJDK_ONLY_FILENAME

    write_identifiers(differences["temurin_only"], temurin_only_path)
    write_identifiers(differences["openjdk_only"], openjdk_only_path)

    return {
        "temurin_only": temurin_only_path,
        "openjdk_only": openjdk_only_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate diff files from Temurin and OpenJDK issue lists.",
    )
    parser.add_argument(
        "--temurin-path",
        type=Path,
        default=DEFAULT_TEMURIN_PATH,
        help="Path to the Temurin JDK issue list.",
    )
    parser.add_argument(
        "--openjdk-path",
        type=Path,
        default=DEFAULT_OPENJDK_PATH,
        help="Path to the OpenJDK JDK issue list.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where diff files will be stored.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = collect_jdk_diff(args.temurin_path, args.openjdk_path, args.output_dir)
    for label, path in outputs.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
