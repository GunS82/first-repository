import re
import json
from typing import Dict, List, Tuple

def parse_abap_file(path: str) -> Dict[str, int]:
    counts = {'class': 0, 'form': 0, 'function': 0}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line_up = line.strip().upper()
            if line_up.startswith('CLASS ') and 'DEFINITION' in line_up:
                counts['class'] += 1
            elif line_up.startswith('FORM '):
                counts['form'] += 1
            elif line_up.startswith('FUNCTION '):
                counts['function'] += 1
    return counts

def parse_object_base(path: str) -> List[Tuple[str, str]]:
    objects = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                name, obj_type = parts[0], parts[1]
                objects.append((name, obj_type))
    return objects

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: python abap_parser.py <abap_file> <object_base>')
        sys.exit(1)
    counts = parse_abap_file(sys.argv[1])
    objs = parse_object_base(sys.argv[2])
    print('Counts:', json.dumps(counts))
    print('Objects:', json.dumps(objs))
