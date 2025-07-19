#!/usr/bin/env python3
"""Parse ABAP code using ABAP-Code-Scanner and validate object names.

This script extracts classes, function modules, FORMs and table names from an
ABAP source file. Extracted names are compared with reference lists stored in a
`base` directory containing `tables.txt`, `classes.txt` and `functions.txt`.
The script relies on a minimal copy of the ABAP-Code-Scanner library included in
this repository.

Usage:
    python abap_parser.py SOURCE_FILE BASE_DIR OUTPUT_JSON
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scanner_lib.config import Config
from scanner_lib.scanner import Scanner


CHECK_TITLE = "ObjectExtractor"


def extract_objects(path: Path) -> dict[str, list[str]]:
    """Parse ABAP source and return detected object names."""
    config_path = Path(__file__).parent / "scanner_lib" / "config.yml"
    config = Config(str(config_path))
    scanner = Scanner(config)
    results = scanner.scan(str(path))

    classes: set[str] = set()
    functions: set[str] = set()
    forms: set[str] = set()
    tables: set[str] = set()

    for result in results:
        if result.title != CHECK_TITLE:
            continue
        if result.message.startswith("class:"):
            classes.add(result.message.split(":", 1)[1])
        elif result.message.startswith("function:"):
            functions.add(result.message.split(":", 1)[1])
        elif result.message.startswith("form:"):
            forms.add(result.message.split(":", 1)[1])
        elif result.message.startswith("table:"):
            tables.add(result.message.split(":", 1)[1])

    return {
        "classes": sorted(classes),
        "functions": sorted(functions),
        "forms": sorted(forms),
        "tables": sorted(tables),
    }


def load_base_list(base_dir: Path, name: str) -> set[str]:
    """Load reference names from BASE_DIR/NAME.txt."""
    path = base_dir / f"{name}.txt"
    if path.is_file():
        return {line.strip() for line in path.read_text(encoding="utf8").splitlines() if line.strip()}
    return set()


def compare_found(found: list[str], base: set[str]) -> dict:
    """Compare extracted names with reference set."""
    found_set = set(found)
    total = len(found_set)
    invalid = sorted(found_set - base)
    valid = sorted(found_set & base)
    errors = len(invalid)
    percent = (errors / total * 100) if total > 0 else 0.0
    return {
        "total": total,
        "valid": len(valid),
        "invalid": errors,
        "error_percentage": round(percent, 2),
        "invalid_names": invalid,
    }


def main() -> None:
    parser_cli = argparse.ArgumentParser(description="Parse ABAP and validate object names.")
    parser_cli.add_argument("source", help="path to ABAP source file")
    parser_cli.add_argument("base_dir", help="directory with tables.txt/classes.txt/functions.txt")
    parser_cli.add_argument("output", help="JSON file for results")
    args = parser_cli.parse_args()

    base_path = Path(args.base_dir)
    extracted = extract_objects(Path(args.source))

    base_sets = {
        "tables": load_base_list(base_path, "tables"),
        "classes": load_base_list(base_path, "classes"),
        "functions": load_base_list(base_path, "functions"),
    }

    stats = {category: compare_found(extracted[category], base_sets.get(category, set()))
             for category in base_sets.keys()}

    result = {
        "extracted": extracted,
        "statistics": stats,
    }

    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf8")


if __name__ == "__main__":
    main()
