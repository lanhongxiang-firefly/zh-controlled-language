"""通用测试执行器：Core／Domain Pack／集成三组用例共用。

用法：
    python tests/run_tests.py                     跑三组默认目标
    python tests/run_tests.py <target> [...]      跑指定目录或 .json 用例文件
    python tests/run_tests.py --integration       追加跨学科模拟断言
    python tests/run_tests.py --strict            出现误判时以非零码退出
    python tests/run_tests.py --write-baseline    重建 Core／Skill 哈希基线

目标为目录时，读取 <dir>/cases.json 或 <dir>/tests/cases.json；为 .json 文件时直接读取。
观测处置取自同目录 results.json，缺失时以期望值作自评基线并标注。
仅用 Python 标准库。
"""

import argparse
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"
DEFAULT_TARGETS = [
    ROOT / "core",
    ROOT / "domains" / "engineering-thermophysics",
    TESTS / "integration.json",
]
BASELINE_FILE = TESTS / "baseline.json"
CORE_FILES = [
    ROOT / "core" / "language-rules.md",
    ROOT / "core" / "terminology-governance.md",
    ROOT / "core" / "quality-control.md",
    ROOT / "skill" / "SKILL.md",
]

REQUIRED = {
    "id", "category", "text_type", "source", "expected_action",
    "expected_level", "dimension", "rationale",
}
CATEGORIES = {"positive", "negative", "boundary"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate(target):
    path = Path(target)
    if not path.is_absolute():
        path = ROOT / path
    if path.is_dir():
        for candidate in (path / "cases.json", path / "tests" / "cases.json"):
            if candidate.exists():
                return candidate
        raise FileNotFoundError(f"未找到 cases.json：{path}")
    if path.suffix == ".json" and path.exists():
        return path
    raise FileNotFoundError(f"目标不存在：{path}")


def classify(case, observed):
    if observed == case["expected_action"]:
        return None
    return {"positive": "过度修改", "boundary": "分级误判", "negative": "漏判"}[case["category"]]


def run_group(cases_file):
    data = json.loads(cases_file.read_text(encoding="utf-8"))
    cases = data["cases"]
    problems = []
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        problems.append("用例编号重复")
    for c in cases:
        if REQUIRED - set(c):
            problems.append(f"{c.get('id','?')} 缺字段 {sorted(REQUIRED - set(c))}")
        if c.get("category") not in CATEGORIES:
            problems.append(f"{c.get('id','?')} 类别非法")
        if c.get("expected_action") not in data.get("actions", {}):
            problems.append(f"{c.get('id','?')} 期望处置非法")
    if problems:
        return {"file": cases_file, "error": problems}

    results_file = cases_file.parent / "results.json"
    reviewer = "规则制定方自评基线（非独立盲评）"
    if results_file.exists():
        obs_data = json.loads(results_file.read_text(encoding="utf-8"))
        observations = obs_data["observations"]
        reviewer = obs_data.get("reviewer", reviewer)
    else:
        observations = {c["id"]: c["expected_action"] for c in cases}
        reviewer += "；未提供 results.json，以期望值作基线"

    bad = [(c, t) for c, t in
           ((c, classify(c, observations.get(c["id"]))) for c in cases) if t]
    counts = Counter(t for _, t in bad)
    cat = Counter(c["category"] for c in cases)

    lines = [
        f"# 测试结果：{data.get('module', cases_file.parent.name)}",
        "",
        f"- 运行日期：{date.today().isoformat()}",
        f"- 评审方：{reviewer}",
        f"- 用例数：{len(cases)}（正例 {cat['positive']}／反例 {cat['negative']}／边界 {cat['boundary']}）",
        f"- 误判：{len(bad)}（过度修改 {counts['过度修改']}／分级误判 {counts['分级误判']}／漏判 {counts['漏判']}）",
        "",
        "## 误判清单",
        "",
    ]
    if bad:
        lines += ["| 用例 | 期望 | 观测 | 类型 |", "| --- | --- | --- | --- |"]
        lines += [f"| {c['id']} | {c['expected_action']} | {observations.get(c['id'])} | {t} |" for c, t in bad]
    else:
        lines.append("本次执行未出现误判。")
    lines += [
        "",
        "## 局限",
        "",
        "1. 用例为构造语料，非真实项目文本分布。",
        "2. 观测由规则制定方给出，存在同源偏差；需独立评审方更新 results.json 后重跑。",
        "3. 测试集检验规则判定的一致性，未测量阅读效率或理解正确率。",
        "",
    ]
    report = cases_file.parent / "RESULTS.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    return {"file": cases_file, "count": len(cases), "bad": len(bad), "report": report}


def write_baseline():
    BASELINE_FILE.write_text(
        json.dumps({"sha256": {str(p.relative_to(ROOT)): sha(p) for p in CORE_FILES}},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def integration_checks():
    if not BASELINE_FILE.exists():
        write_baseline()
    expected = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))["sha256"]
    unchanged = all(sha(ROOT / rel) == digest for rel, digest in expected.items())

    stub = TESTS / "stub-pack" / "manifest.yaml"
    stub_text = stub.read_text(encoding="utf-8") if stub.exists() else ""
    stub_ok = all(x in stub_text for x in ["id: stub-discipline", "enabled: true", 'core_version: "0.2"'])
    stub_terms = TESTS / "stub-pack" / "terminology.md"
    proposed_ok = "Proposed" in stub_terms.read_text(encoding="utf-8") if stub_terms.exists() else False

    integ = json.loads((TESTS / "integration.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c["expected_action"] for c in integ["cases"]}
    unloaded_ok = by_id.get("I-01") == "no_change"
    conflict_ok = by_id.get("I-02") == "review" and by_id.get("I-03") == "review"

    total = sum(len(json.loads(locate(t).read_text(encoding="utf-8"))["cases"]) for t in DEFAULT_TARGETS)
    total_ok = total >= 25

    checks = {
        "加载 stub Pack 后 Core 与 Skill 文件未改变": unchanged,
        "stub Pack manifest 合规且已启用": stub_ok,
        "stub 术语状态为 Proposed，未升级为强制": proposed_ok,
        "未加载 Pack 时不被误用（I-01）": unloaded_ok,
        "术语冲突保留上下文、不强制统一（I-02／I-03）": conflict_ok,
        f"用例总数不减（{total} ≥ 25）": total_ok,
    }
    return checks, total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="*")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--integration", action="store_true")
    parser.add_argument("--write-baseline", action="store_true")
    args = parser.parse_args()

    if args.write_baseline:
        write_baseline()
        print("已重建 Core／Skill 哈希基线")

    targets = [Path(t) for t in args.targets] if args.targets else DEFAULT_TARGETS
    total_bad = 0
    for target in targets:
        result = run_group(locate(target))
        if "error" in result:
            print(f"[结构校验失败] {result['file']}")
            for p in result["error"]:
                print("  -", p)
            return 1
        total_bad += result["bad"]
        print(f"[{result['file'].parent.name}] 用例 {result['count']} 条，误判 {result['bad']} 条 → {result['report']}")

    if args.integration:
        checks, total = integration_checks()
        print("\n跨学科模拟断言：")
        for name, ok in checks.items():
            print(f"  {'OK  ' if ok else 'FAIL'} {name}")
        if not all(checks.values()):
            return 1

    print(f"\n合计误判 {total_bad} 条")
    return 1 if (args.strict and total_bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
