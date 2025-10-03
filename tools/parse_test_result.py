#!/usr/bin/env python3
"""
Parse pytest JUnitXML output and generate a Markdown summary.

Usage:
    python tools/parse_test_result.py path/to/test-results.xml runtime
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_junit_xml(xml_file: Path) -> dict:
    """Parse a JUnit XML file and extract test results."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Top-level attributes from <testsuite>
    total = int(root.get("tests", 0))
    failures = int(root.get("failures", 0))
    errors = int(root.get("errors", 0))
    skipped = int(root.get("skipped", 0))
    time = float(root.get("time", 0))

    failed_tests = []
    for testcase in root.findall(".//testcase"):
        failure = testcase.find("failure")
        error = testcase.find("error")
        if failure is not None or error is not None:
            element = failure if failure is not None else error
            failed_tests.append(
                {
                    "name": f"{testcase.get('classname')}::{testcase.get('name')}",
                    "message": element.get("message", "").strip(),
                    "type": "failure" if failure is not None else "error",
                }
            )

    return {
        "total": total,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "passed": total - failures - errors - skipped,
        "time": time,
        "failed_tests": failed_tests,
    }


def generate_test_summary(results: dict, runtime: str) -> str:
    """Generate a Markdown summary for test results."""
    lines = []
    lines.append(f"# Test Results ({runtime})\n")
    lines.append(f"- Passed: {results['passed']}")
    lines.append(f"- Failed: {results['failures']}")
    lines.append(f"- Errors: {results['errors']}")
    lines.append(f"- Skipped: {results['skipped']}")
    lines.append(f"- Duration: {results['time']:.1f}s\n")

    if results["failed_tests"]:
        lines.append("## Failed Tests\n")
        for test in results["failed_tests"][:20]:  # limit to 20 failures
            lines.append(f"- {test['name']}")
            if test["message"]:
                msg = test["message"].split("\n")[0][:200]
                lines.append(f"  ```\n  {msg}\n  ```")

        if len(results["failed_tests"]) > 20:
            lines.append(
                f"\n...and {len(results['failed_tests']) - 20} more failures.\n"
            )

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: parse_test_result.py <xml_file> <runtime>")
        sys.exit(1)

    xml_file = Path(sys.argv[1])
    runtime = sys.argv[2]
    results = parse_junit_xml(xml_file)
    summary = generate_test_summary(results, runtime)
    print(summary)
