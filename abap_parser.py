#!/usr/bin/env python3
"""Parse ABAP code with ABAP Code Scanner and validate object names."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set

from scanner import Scanner


class SimpleConfig:
    """Minimal configuration for Scanner."""

    def __init__(self, checks: List[str], file_extensions: List[str] | None = None):
        self._checks = checks
        self._file_extensions = file_extensions or ['.abap']

    def get_checks(self) -> List[str]:
        return self._checks

    def get_file_extensions(self) -> List[str]:
        return self._file_extensions

    def get_exclude_patterns(self) -> List[str]:
        return []


def extract_objects(path: Path) -> Dict[str, List[str]]:
    """Run scanner on the file and collect object names."""
    config = SimpleConfig(['CheckClasses', 'CheckFunctions', 'CheckTables'], [path.suffix])
    scanner = Scanner(config)
    results = scanner.scan(str(path), num_threads=1)

    classes: Set[str] = set()
    functions: Set[str] = set()
    tables: Set[str] = set()

    for res in results:
        name = res.message.upper()
        if res.title == 'CLASS':
            classes.add(name)
        elif res.title == 'FUNCTION':
            functions.add(name)
        elif res.title == 'TABLE':
            tables.add(name)

    return {
        'classes': sorted(classes),
        'functions': sorted(functions),
        'tables': sorted(tables),
    }


def load_base_list(base_dir: Path, name: str) -> Set[str]:
    """Load reference names from BASE_DIR/NAME.txt."""
    path = base_dir / f"{name}.txt"
    if path.is_file():
        return {line.strip().upper() for line in path.read_text(encoding='utf8').splitlines() if line.strip()}
    return set()


def compare_found(found: List[str], base: Set[str]) -> Dict:
    """Compare extracted names with reference set."""
    found_set = set(found)
    total = len(found_set)
    invalid = sorted(found_set - base)
    valid = sorted(found_set & base)
    errors = len(invalid)
    percent = (errors / total * 100) if total > 0 else 0.0
    return {
        'total': total,
        'valid': len(valid),
        'invalid': errors,
        'error_percentage': round(percent, 2),
        'invalid_names': invalid,
    }


def main() -> None:
    parser_cli = argparse.ArgumentParser(description='Parse ABAP and validate object names.')
    parser_cli.add_argument('source', help='path to ABAP source file')
    parser_cli.add_argument('base_dir', help='directory with tables.txt/classes.txt/functions.txt')
    parser_cli.add_argument('output', help='JSON file for results')
    args = parser_cli.parse_args()

    base_path = Path(args.base_dir)
    extracted = extract_objects(Path(args.source))

    base_sets = {
        'tables': load_base_list(base_path, 'tables'),
        'classes': load_base_list(base_path, 'classes'),
        'functions': load_base_list(base_path, 'functions'),
    }

    stats = {category: compare_found(extracted[category], base_sets.get(category, set()))
             for category in base_sets.keys()}

    result = {
        'extracted': extracted,
        'statistics': stats,
    }

    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')


if __name__ == '__main__':
    main()
