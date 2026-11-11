"""按 manifest 组装中文受控语言技能包，并同步到四个 Agent 宿主。

- 源文件分散在 skill/、core/、domains/、profiles/；组装产物在 build/zh-controlled-language/
- frontmatter name 为 zh-controlled-language（D-1）；四宿主目录保留旧名作为兼容别名
- build 与 dist 为公开分发包：defaults.yaml 不带默认学科
- 四宿主为本机安装：defaults.yaml 写入 default_domain: engineering-thermophysics
- WorkBuddy 副本保留 agent_created；其余副本裁掉该字段以符合 Agent Skills 规范
- 安装前把四宿主旧目录完整备份到 backup/，并把残留 references/、tests/ 移入 _v0.2_archive/
- 不删除任何文件；可重复运行
- 仅用 Python 标准库
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL_NAME = "zh-controlled-language"
TARGET_DIR_NAME = "engineering-thermophysics-zh-controlled-language"
LOCAL_DEFAULT_DOMAIN = "engineering-thermophysics"
PUBLIC_DOMAIN = ""
HOME = Path.home()
BUILD = ROOT / "build" / SKILL_NAME
BACKUP = ROOT / "backup"

# (源文件, 技能包内相对路径)
FILE_MAP = [
    ("skill/SKILL.md", "SKILL.md"),
    ("skill/ALIASES.md", "ALIASES.md"),
    ("core/language-rules.md", "core/language-rules.md"),
    ("core/terminology-governance.md", "core/terminology-governance.md"),
    ("core/quality-control.md", "core/quality-control.md"),
    ("domains/engineering-thermophysics/manifest.yaml",
     "domains/engineering-thermophysics/manifest.yaml"),
    ("domains/engineering-thermophysics/terminology.md",
     "domains/engineering-thermophysics/terminology.md"),
    ("domains/engineering-thermophysics/rules.md",
     "domains/engineering-thermophysics/rules.md"),
    ("domains/engineering-thermophysics/tests/cases.json",
     "domains/engineering-thermophysics/tests/cases.json"),
    ("profiles/technical-documentation/profile.md",
     "profiles/technical-documentation/profile.md"),
]

DEFAULTS_HEADER = (
    "# 默认学科配置。公开分发版本为空，由使用者首次配置时填写。\n"
    "# 本机安装由 install_skills.py 写入。\n"
)


def skill_text(keep_agent_created):
    text = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
    if not keep_agent_created:
        text = "".join(
            line for line in text.splitlines(keepends=True)
            if not line.startswith("agent_created:")
        )
    return text


def assemble(destination, default_domain, keep_agent_created):
    destination.mkdir(parents=True, exist_ok=True)
    written = []
    for source_rel, target_rel in FILE_MAP:
        content = (skill_text(keep_agent_created)
                   if target_rel == "SKILL.md"
                   else (ROOT / source_rel).read_text(encoding="utf-8"))
        target = destination / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            target.write_text(content, encoding="utf-8")
            written.append(target_rel)
    defaults = DEFAULTS_HEADER + f"default_domain: \"{default_domain}\"\n"
    target = destination / "defaults.yaml"
    if not target.exists() or target.read_text(encoding="utf-8") != defaults:
        target.write_text(defaults, encoding="utf-8")
        written.append("defaults.yaml")
    return written


def backup_and_archive(directory, label):
    if not directory.exists():
        return [], []
    backup_dir = BACKUP / label
    backup_dir.mkdir(parents=True, exist_ok=True)
    # 首次运行备份原始 V0.2 目录；重复运行时保留已有干净备份，避免写入迁移后的内容
    if not any(backup_dir.iterdir()):
        shutil.copytree(directory, backup_dir, dirs_exist_ok=True)
    moved = []
    archive = directory / "_v0.2_archive"
    for name in ("references", "tests"):
        source = directory / name
        if source.exists() and not (archive / name).exists():
            archive.mkdir(exist_ok=True)
            source.rename(archive / name)
            moved.append(name)
    return moved, sorted(str(p.relative_to(backup_dir)) for p in backup_dir.rglob("*") if p.is_file())


dsh_home = os.environ.get("DSH_HOME") or str(HOME / ".dsh")
targets = [
    ("WorkBuddy", HOME / ".workbuddy" / "skills" / TARGET_DIR_NAME, True),
    ("Codex", HOME / ".codex" / "skills" / TARGET_DIR_NAME, False),
    ("DeepSeek Harness", Path(dsh_home) / "skills" / TARGET_DIR_NAME, False),
    ("Claude Code", HOME / ".claude" / "skills" / TARGET_DIR_NAME, False),
]

# 1) 公开分发包：defaults 为空
public_written = assemble(BUILD, PUBLIC_DOMAIN, False)
print(f"[公开包] {BUILD}\n  文件 {len(FILE_MAP) + 1} 个，changed={len(public_written)}")

# 2) 四宿主：defaults 写本机默认学科
for label, directory, keep_flag in targets:
    moved, backup_files = backup_and_archive(directory, label.replace(" ", "-").lower())
    written = assemble(directory, LOCAL_DEFAULT_DOMAIN, keep_flag)
    print(
        f"[{label}] {directory}\n"
        f"  changed={len(written)} archived={moved or '无'} "
        f"backup_files={len(backup_files)} backup={BACKUP / label.replace(' ', '-').lower()}"
    )

print(f"\n规范名称 = {SKILL_NAME}；兼容别名（四宿主目录名）= {TARGET_DIR_NAME}")
print(f"本机默认学科 = {LOCAL_DEFAULT_DOMAIN}；公开版默认学科 = 空")
print(f"DSH_HOME = {os.environ.get('DSH_HOME') or '<unset, 使用默认 ~/.dsh>'}")
