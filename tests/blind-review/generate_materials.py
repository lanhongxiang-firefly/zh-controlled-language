"""生成独立盲评材料：剥离期望答案，不写入答案文件。仅用 Python 标准库。"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCES = [
    ROOT / "core" / "cases.json",
    ROOT / "domains" / "engineering-thermophysics" / "tests" / "cases.json",
    ROOT / "tests" / "integration.json",
]
CORPUS = HERE / "corpus.json"
LEVELS = ["none", "Error", "Warning", "Suggestion"]


def source_files():
    return SOURCES + ([CORPUS] if CORPUS.exists() else [])


def load():
    actions, cases = {}, []
    for path in source_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        actions.update(data.get("actions", {}))
        module = data.get("module", path.parent.name)
        for c in data["cases"]:
            cases.append({
                "id": f"{module}:{c['id']}",
                "module": module,
                "text_type": c["text_type"],
                "source": c["source"],
            })
    return actions, cases


def cell(text):
    return text.replace("|", "\\|").replace("\n", "<br>")


def main():
    actions, cases = load()
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise SystemExit("用例编号重复，请先修正源用例")

    blind = {
        "note": "独立盲评材料。不含期望答案；判定口径见 protocol.md，动作取值见 actions。",
        "actions": actions,
        "levels": LEVELS,
        "cases": [dict(c, observed_action="", observed_level="", note="") for c in cases],
    }
    (HERE / "blind-cases.json").write_text(
        json.dumps(blind, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    template = {
        "reviewer": "",
        "date": "",
        "rules_version": "0.2",
        "note": "填写 observed_action 与 observed_level；保存为 observations.json。",
        "observations": {
            c["id"]: {"observed_action": "", "observed_level": "", "note": ""}
            for c in cases
        },
    }
    (HERE / "observations-template.json").write_text(
        json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 独立盲评评审表",
        "",
        f"- 用例数：{len(cases)}",
        "- 动作取值：" + "、".join(f"`{k}`（{v}）" for k, v in actions.items()),
        "- 级别取值：`none`、`Error`、`Warning`、`Suggestion`；级别仅作记录，不计入误判统计。",
        "- 填写后保存为 `observations.json`，运行 `python tests/blind-review/summarize.py`。",
        "",
        "| ID | 文体 | 原文 | 处置 | 级别 | 备注 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for c in cases:
        lines.append(f"| {c['id']} | {c['text_type']} | {cell(c['source'])} |  |  |  |")
    (HERE / "review-sheet.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"已生成 {len(cases)} 条盲评材料：blind-cases.json / review-sheet.md / observations-template.json")
    print("答案键未落盘；summarize.py 直接从三组 cases.json 读取期望值。")


if __name__ == "__main__":
    main()
