"""汇总独立盲评结果。仅用 Python 标准库，不做语义判断。"""

import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCES = [
    ROOT / "core" / "cases.json",
    ROOT / "domains" / "engineering-thermophysics" / "tests" / "cases.json",
    ROOT / "tests" / "integration.json",
]
CORPUS = HERE / "corpus.json"
MISCLASS = {"positive": "过度修改", "boundary": "分级误判", "negative": "漏判"}


def source_files():
    return SOURCES + ([CORPUS] if CORPUS.exists() else [])


def expected():
    out = {}
    for path in source_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        module = data.get("module", path.parent.name)
        for c in data["cases"]:
            out[f"{module}:{c['id']}"] = {
                "module": module,
                "category": c["category"],
                "expected_action": c["expected_action"],
                "expected_level": c["expected_level"],
            }
    return out


def main():
    obs_file = HERE / "observations.json"
    if not obs_file.exists():
        raise SystemExit(
            "缺少 observations.json；请由独立评审方按 observations-template.json 填写后放入本目录。")
    obs_data = json.loads(obs_file.read_text(encoding="utf-8"))
    observations = obs_data["observations"]
    exp = expected()
    missing = sorted(set(exp) - set(observations))
    extra = sorted(set(observations) - set(exp))
    if missing or extra:
        raise SystemExit(f"用例编号不匹配：缺少 {missing}；多出 {extra}")

    bad = []
    level_match = 0
    for cid, e in exp.items():
        o = observations[cid]
        action = o.get("observed_action", "")
        if action != e["expected_action"]:
            bad.append((cid, e["category"], MISCLASS[e["category"]],
                        e["expected_action"], action))
        if o.get("observed_level", "") == e["expected_level"]:
            level_match += 1

    counts = Counter(t[2] for t in bad)
    modules = sorted({e["module"] for e in exp.values()})
    group_lines = [
        f"- `{m}`：用例 {sum(1 for e in exp.values() if e['module'] == m)}，"
        f"误判 {sum(1 for t in bad if exp[t[0]]['module'] == m)}"
        for m in modules
    ]
    lines = [
        "# 独立盲评结果",
        "",
        f"- 运行日期：{date.today().isoformat()}",
        f"- 评审方：{obs_data.get('reviewer', '未填写')}",
        f"- 规则版本：{obs_data.get('rules_version', '未填写')}",
        f"- 用例数：{len(exp)}",
        f"- 误判：{len(bad)}（过度修改 {counts['过度修改']}／分级误判 {counts['分级误判']}／漏判 {counts['漏判']}）",
        f"- 级别标注与期望一致：{level_match}/{len(exp)}（级别不单独计入误判）",
        "",
        "## 分组统计",
        "",
        *group_lines,
        "",
        "## 误判清单",
        "",
    ]
    if bad:
        lines += ["| 用例 | 类别 | 误判类型 | 期望 | 观测 |", "| --- | --- | --- | --- | --- |"]
        lines += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in bad]
    else:
        lines.append("本次执行未出现误判。")
    lines += [
        "",
        "## 局限",
        "",
        "1. 用例为构造语料，非真实项目文本分布；真实语料须单独登记与统计。",
        "2. 单一评审方仍可能引入个体偏差；建议不少于两名评审方分别填写后比较。",
        "3. 判定口径依赖评审方对规则文件版本的理解。",
        "4. 本汇总检验规则判定一致性，不测量阅读效率或理解正确率。",
        "",
    ]
    (HERE / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 RESULTS.md：用例 {len(exp)} 条，误判 {len(bad)} 条，级别一致 {level_match}/{len(exp)}")


if __name__ == "__main__":
    main()
