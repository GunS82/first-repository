from dataclasses import dataclass
from typing import List
import re

@dataclass
class CheckResult:
    line_number: int
    line_content: str

class CheckClasses:
    """Extract class names used in static method calls or type refs."""
    title = "CLASS"
    severity = "Info"

    pattern = re.compile(r"([A-Za-z0-9_/]+)=>", re.IGNORECASE)

    def run(self, file_content: str) -> List[CheckResult]:
        results = []
        lines = file_content.split('\n')
        for i, line in enumerate(lines, 1):
            for match in self.pattern.finditer(line):
                results.append(CheckResult(i, match.group(1).upper()))
        return results
