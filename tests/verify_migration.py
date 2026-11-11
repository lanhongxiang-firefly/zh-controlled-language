"""迁移回归校验：内容完整性、用例分布、四宿主一致性、公开包与备份完整性。

用法：python tests/verify_migration.py
仅用 Python 标准库；不修改任何文件。
"""

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "zh-controlled-language"
HOME = Path.home()
ALIAS = "engineering-thermophysics-zh-controlled-language"

core = (ROOT / "core" / "language-rules.md").read_text(encoding="utf-8")
gov = (ROOT / "core" / "terminology-governance.md").read_text(encoding="utf-8")
qc = (ROOT / "core" / "quality-control.md").read_text(encoding="utf-8")
skill = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
profile = (ROOT / "profiles" / "technical-documentation" / "profile.md").read_text(encoding="utf-8")
terminology = (ROOT / "domains" / "engineering-thermophysics" / "terminology.md").read_text(encoding="utf-8")
rules = (ROOT / "domains" / "engineering-thermophysics" / "rules.md").read_text(encoding="utf-8")

checks = {
    "E1–E7 全在 Core": all("E%d" % i in core for i in range(1, 8)),
    "W1–W7 全在 Core": all("W%d" % i in core for i in range(1, 8)),
    "Suggestion 与误判控制在 Core": "## 6 Suggestion" in core and "## 3 误判控制" in core,
    "已移除机械判据记录保留": "## 8 已移除的机械判据" in core and "单句超过 40 汉字" in core,
    "表达问题词形表保留": "## 7 表达问题词形" in core and "赋能" in core,
    "三层治理与强制门槛在 Core": all(x in gov for x in ["A 权威规范", "B 领域常用", "C 争议", "强制门槛", "D-2 边界"]),
    "保留项 6 条在 Core": "## 1 保留项" in qc and all("%d." % i in qc for i in range(1, 7)),
    "按需核对点 14 项": len(re.findall(r"^- \[ \]", qc, re.M)) == 14,
    "误判类型 5 类": len(re.findall(r"^\| (过度修改|漏判|分级误判|依据误判|保真误判)", qc, re.M)) == 5,
    "校准示例 22 条": len(re.findall(r"^\d+\.", qc, re.M)) >= 22,
    "术语表 19 条在 Pack": len(re.findall(r"^\| T-ET-\d+", terminology, re.M)) == 19,
    "Pack 规则 4 条": len(re.findall(r"^## R-ET-\d+", rules, re.M)) == 4,
    "7 类文本覆盖在 Profile": all(x in profile for x in ["代码注释", "技术文档", "科研申请书", "技术报告", "项目材料", "日志与错误提示", "日常技术交流"]),
    "执行层含默认学科与白名单": all(x in skill for x in ["default_domain", "白名单", "临时切换", "只加载 Core"]),
    "frontmatter 为通用名": re.search(r"^name: zh-controlled-language", skill, re.M) is not None,
    "别名映射已记录": ALIAS in (ROOT / "skill" / "ALIASES.md").read_text(encoding="utf-8"),
    "公开版 defaults 为空": 'default_domain: ""' in (BUILD / "defaults.yaml").read_text(encoding="utf-8"),
    "ADR 状态为已批准并实施": "Approved" in (ROOT / "docs" / "architecture" / "ADR-0001.md").read_text(encoding="utf-8"),
}

print("== 内容完整性 ==")
for name, ok in checks.items():
    print("  %s %s" % ("OK  " if ok else "FAIL", name))
print("  全部通过:", all(checks.values()))

groups = [
    ROOT / "core" / "cases.json",
    ROOT / "domains" / "engineering-thermophysics" / "tests" / "cases.json",
    ROOT / "tests" / "integration.json",
]
counts = [len(json.loads(p.read_text(encoding="utf-8"))["cases"]) for p in groups]
print("\n== 用例分布 ==")
print("  Core %d / Pack %d / Integration %d / 合计 %d（V0.2 基线 25）" % (*counts, sum(counts)))
print("  总数不减:", sum(counts) >= 25)

build_files = sorted(p.relative_to(BUILD).as_posix() for p in BUILD.rglob("*") if p.is_file())
print("\n== 公开包 ==")
print("  文件数:", len(build_files))

dsh = Path(__import__("os").environ.get("DSH_HOME") or HOME / ".dsh")
hosts = {
    "WorkBuddy": HOME / ".workbuddy" / "skills" / ALIAS,
    "Codex": HOME / ".codex" / "skills" / ALIAS,
    "DeepSeek Harness": dsh / "skills" / ALIAS,
    "Claude Code": HOME / ".claude" / "skills" / ALIAS,
}
print("\n== 四宿主副本 ==")
host_ok = True
for name, directory in hosts.items():
    shared = all(
        (directory / rel).exists() and (directory / rel).read_bytes() == (BUILD / rel).read_bytes()
        for rel in build_files if rel not in ("SKILL.md", "defaults.yaml")
    )
    sk = (directory / "SKILL.md").read_text(encoding="utf-8")
    defs = (directory / "defaults.yaml").read_text(encoding="utf-8")
    local = 'default_domain: "engineering-thermophysics"' in defs
    name_ok = "zh-controlled-language" in sk
    archived = (directory / "_v0.2_archive").exists()
    ok = shared and local and name_ok and archived
    host_ok = host_ok and ok
    print("  %-18s 共享文件一致=%s 本机默认=%s 通用名=%s 归档=%s → %s"
          % (name, shared, local, name_ok, archived, ok))
print("  四宿主全部通过:", host_ok)

z = zipfile.ZipFile(ROOT / "dist" / "zh-controlled-language.zip")
zip_ok = len(z.infolist()) == len(build_files) and all(
    z.read("zh-controlled-language/" + rel).decode("utf-8").replace("\r\n", "\n")
    == (BUILD / rel).read_text(encoding="utf-8").replace("\r\n", "\n")
    for rel in build_files
)
print("\n== 分发包 ==")
print("  dist/zh-controlled-language.zip 文件数:", len(z.infolist()), "与公开包一致:", zip_ok)

print("\n== 回滚备份 ==")
backups = sorted((ROOT / "backup").iterdir())
backup_ok = True
for b in backups:
    n = len([p for p in b.rglob("*") if p.is_file()])
    ok = n >= 9
    backup_ok = backup_ok and ok
    print("  %-20s %d 文件 → %s" % (b.name, n, ok))
print("  备份完整:", backup_ok and len(backups) == 4)

print("\n== 结论 ==")
print("  迁移校验通过:", all(checks.values()) and sum(counts) >= 25 and host_ok and zip_ok and backup_ok)
