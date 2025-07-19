from dataclasses import dataclass
from typing import List
import re

@dataclass
class CheckResult:
    line_number: int
    line_content: str

class CheckObjectExtractor:
    """Extract classes, functions, forms and tables from ABAP code."""

    title = "ObjectExtractor"
    severity = "Info"

    def __init__(self):
        self.class_pattern = re.compile(r"\b(?:NEW\s+|)([A-Za-z0-9_/]+)=>|\bNEW\s+([A-Za-z0-9_/]+)\(", re.IGNORECASE)
        self.function_pattern = re.compile(r"CALL\s+FUNCTION\s+'([A-Za-z0-9_/]+)'", re.IGNORECASE)
        self.form_pattern = re.compile(r"FORM\s+([A-Za-z0-9_/]+)", re.IGNORECASE)
        self.table_pattern = re.compile(r"FROM\s+([A-Za-z0-9_/]+)", re.IGNORECASE)

    def run(self, file_content: str) -> List[CheckResult]:
        results: List[CheckResult] = []
        lines = file_content.splitlines()
        for idx, line in enumerate(lines, 1):
            for match in self.class_pattern.finditer(line):
                name = match.group(1) or match.group(2)
                results.append(CheckResult(idx, f"class:{name}"))
            for match in self.function_pattern.finditer(line):
                results.append(CheckResult(idx, f"function:{match.group(1)}"))
            for match in self.form_pattern.finditer(line):
                results.append(CheckResult(idx, f"form:{match.group(1)}"))
            for match in self.table_pattern.finditer(line):
                results.append(CheckResult(idx, f"table:{match.group(1)}"))
        return results
