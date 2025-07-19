from dataclasses import dataclass
from typing import List
import re

@dataclass
class CheckResult:
    line_number: int
    line_content: str

class CheckTables:
    """Extract table names from SELECT statements."""
    title = "TABLE"
    severity = "Info"

    pattern = re.compile(r"\bFROM\s+([A-Za-z0-9_/]+)|\bJOIN\s+([A-Za-z0-9_/]+)", re.IGNORECASE)

    def run(self, file_content: str) -> List[CheckResult]:
        results = []
        lines = file_content.split('\n')
        for i, line in enumerate(lines, 1):
            for match in self.pattern.finditer(line):
                name = match.group(1) or match.group(2)
                results.append(CheckResult(i, name.upper()))
        return results
