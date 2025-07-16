#!/usr/bin/env python3
"""Parse ABAP code with Tree-sitter and validate object names.

This script extracts tables, classes and function modules from an ABAP
source file using the Tree-sitter grammar for ABAP. Extracted names are
compared with reference lists stored in a directory `base` containing
`tables.txt`, `classes.txt` and `functions.txt`.

Usage:
    python abap_parser.py SOURCE_FILE BASE_DIR OUTPUT_JSON
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from tree_sitter import Language, Parser

# Path to compiled Tree-sitter languages library
LANG_SO = Path('build') / 'my-languages.so'

# Initialise parser
ABAP_LANGUAGE = Language(str(LANG_SO), 'abap')
parser = Parser()
parser.set_language(ABAP_LANGUAGE)


def extract_objects(path: Path) -> dict[str, list[str]]:
    """Parse ABAP source and return detected object names."""
    code = path.read_bytes()
    text = code.decode('utf8', errors='ignore')
    tree = parser.parse(code)
    root = tree.root_node

    classes: set[str] = set()
    functions: set[str] = set()
    forms: set[str] = set()

    def walk(node):
        if node.type == 'class_definition':
            name = node.child_by_field_name('name')
            if name:
                classes.add(text[name.start_byte:name.end_byte])
        elif node.type == 'function_definition':
            name = node.child_by_field_name('name')
            if name:
                functions.add(text[name.start_byte:name.end_byte])
        elif node.type == 'form_definition':
            name = node.child_by_field_name('name')
            if name:
                forms.add(text[name.start_byte:name.end_byte])
        for child in node.children:
            walk(child)

    walk(root)

    tables = set(re.findall(r"FROM\s+([A-Za-z0-9_/]+)", text, flags=re.IGNORECASE))

    return {
        'classes': sorted(classes),
        'functions': sorted(functions),
        'forms': sorted(forms),
        'tables': sorted(tables),
    }


def load_base_list(base_dir: Path, name: str) -> set[str]:
    """Load reference names from BASE_DIR/NAME.txt."""
    path = base_dir / f"{name}.txt"
    if path.is_file():
        return {line.strip() for line in path.read_text(encoding='utf8').splitlines() if line.strip()}
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
