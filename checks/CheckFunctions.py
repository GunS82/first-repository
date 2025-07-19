from dataclasses import dataclass
from typing import List
import re

@dataclass
class CheckResult:
    line_number: int
    line_content: str

class CheckFunctions:
    """Extract function module calls."""
    title = "FUNCTION"
    severity = "Info"

    pattern = re.compile(r"CALL\s+FUNCTION\s+'?([A-Za-z0-9_/]+)'?", re.IGNORECASE)

    def run(self, file_content: str) -> List[CheckResult]:
        results = []
        lines = file_content.split('\n')
        for i, line in enumerate(lines, 1):
            for match in self.pattern.finditer(line):
                results.append(CheckResult(i, match.group(1).upper()))
        return results
