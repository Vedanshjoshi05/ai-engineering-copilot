import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

SEMGREP_RULES = Path(__file__).with_name("review_rules.yml").resolve()


def finding(path, line, tool, category, severity, explanation, recommendation):
    return {
        "path": path,
        "line": line,
        "tool": tool,
        "category": category,
        "severity": severity,
        "explanation": explanation,
        "recommendation": recommendation,
    }


def syntax_findings(files):
    from tree_sitter import Language, Parser
    import tree_sitter_python

    parser = Parser(Language(tree_sitter_python.language()))
    findings = []
    for path, source in files.items():
        root = parser.parse(source.encode("utf-8")).root_node
        pending = [root]
        while pending:
            node = pending.pop()
            if node.is_error or node.is_missing:
                findings.append(finding(
                    path, node.start_point.row + 1, "Tree-sitter", "bug", "high",
                    "Missing Python syntax." if node.is_missing else "Invalid Python syntax.",
                    "Check the surrounding tokens, delimiters, and indentation.",
                ))
            elif node.has_error:
                pending.extend(reversed(node.children))
    return findings


def analyzer_reports(directory, filenames):
    commands = {
        "Ruff": [
            "ruff", "check", "--isolated", "--no-cache", "--output-format=json",
            "--select=E4,E7,E9,F,B",
        ],
        "Pylint": [
            "pylint", "--rcfile=pylint.ini", "--persistent=no", "--output-format=json",
            "--disable=all",
            "--enable=used-before-assignment,undefined-variable,unreachable,dangerous-default-value,inconsistent-return-statements",
        ],
        "Bandit": ["bandit", "-f", "json", "-q", "-c", "bandit.yml"],
        "Semgrep": [
            "semgrep", "scan", "--config", str(SEMGREP_RULES), "--json",
            "--metrics=off", "--disable-version-check", "--no-git-ignore",
        ],
    }

    def run(command):
        executable = shutil.which(command[0])
        if not executable:
            return None
        try:
            process = subprocess.run(
                [executable, *command[1:], *filenames],
                cwd=directory,
                capture_output=True,
                encoding="utf-8",
                timeout=25,
                check=False,
            )
            return json.loads(process.stdout)
        except (OSError, subprocess.TimeoutExpired, ValueError):
            return None

    with ThreadPoolExecutor(max_workers=len(commands)) as executor:
        reports = executor.map(run, commands.values())
        return dict(zip(commands, reports))


def normalize_findings(tool, report, paths):
    pylint_fixes = {
        "E0001": "Correct the syntax and run the review again.",
        "E0601": "Assign the variable along every path that reaches this line.",
        "E0602": "Define or import the name before using it, and check its spelling.",
        "R1710": "Make every reachable return path explicit and consistent.",
        "W0101": "Remove the unreachable statement or revise the preceding control flow.",
        "W0102": "Use None as the default and create a fresh value inside the function.",
    }
    if tool == "Ruff":
        for item in report:
            recommendation = (item.get("fix") or {}).get("message")
            yield finding(
                paths[Path(item["filename"]).name], item["location"]["row"], tool,
                "bug" if item["code"] in {"F821", "F823", "invalid-syntax"} else "quality",
                "medium", f'{item["code"]}: {item["message"]}',
                recommendation or "Resolve the reported lint issue on this line.",
            )
    elif tool == "Pylint":
        for item in report:
            is_error = item["type"] in {"error", "fatal"}
            yield finding(
                paths[Path(item["path"]).name], item["line"], tool,
                "bug" if is_error else "logic", "high" if is_error else "medium",
                f'{item["message-id"]}: {item["message"]}',
                pylint_fixes.get(item["message-id"], "Review the expression named in the diagnostic."),
            )
    elif tool == "Bandit":
        for item in report["results"]:
            rule = item["test_id"]
            if rule in {"B105", "B106", "B107"}:
                explanation = "Possible hard-coded credential."
                recommendation = "Load the credential from an environment variable or secret store."
            else:
                explanation = item["issue_text"]
                recommendation = f'Review the remediation in the Bandit documentation for {rule}.'
            yield finding(
                paths[Path(item["filename"]).name], item["line_number"], tool,
                "quality", item["issue_severity"].lower(),
                f"{rule}: {explanation}", recommendation,
            )
    else:
        for item in report["results"]:
            yield finding(
                paths[Path(item["path"]).name], item["start"]["line"], tool,
                "logic", "medium", f'Matched rule {item["check_id"].split(".")[-1]}.',
                item["extra"]["message"],
            )


def analyze_python(files):
    if not files:
        return [], []

    findings = []
    warnings = []
    try:
        findings.extend(syntax_findings(files))
    except ImportError:
        warnings.append("Tree-sitter is unavailable. Install the review dependencies.")
    with TemporaryDirectory(prefix="nexora-review-") as temporary:
        directory = Path(temporary)
        paths = {}
        for index, (path, source) in enumerate(files.items()):
            name = f"review_{index}.py"
            paths[name] = path
            (directory / name).write_bytes(source.encode("utf-8"))

        (directory / "pylint.ini").write_text("[MAIN]\n", encoding="utf-8")
        (directory / "bandit.yml").write_text("{}\n", encoding="utf-8")
        for tool, report in analyzer_reports(directory, list(paths)).items():
            if report is None:
                warnings.append(f"{tool} did not complete. Check the review dependencies.")
                continue
            try:
                findings.extend(list(normalize_findings(tool, report, paths)))
                if isinstance(report, dict) and report.get("errors"):
                    warnings.append(f"{tool} reported errors while scanning some files.")
            except (KeyError, ValueError, TypeError):
                warnings.append(f"{tool} returned an unreadable report.")

    return findings, warnings
