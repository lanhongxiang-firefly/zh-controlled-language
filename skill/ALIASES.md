# 技能名称与别名映射（D-1）

| 项 | 值 |
| --- | --- |
| 规范名称（frontmatter `name`） | `zh-controlled-language` |
| 旧名／兼容别名 | `engineering-thermophysics-zh-controlled-language` |
| 公开分发包目录 | `zh-controlled-language/`（`dist/zh-controlled-language.zip`） |
| 四宿主安装目录 | `engineering-thermophysics-zh-controlled-language/`（保留旧名作为兼容别名） |
| Core 规则版本 | `0.2`（内容迁移自 V0.2，规则未改动） |
| 本机默认学科 | `engineering-thermophysics` |
| 公开版默认学科 | 空，由使用者自行设置 |

## 别名生效方式

Claude Code 等宿主同时按 frontmatter `name` 与技能目录名发现技能。迁移后 `name` 为通用名，四宿主目录保留旧名，因此旧名仍可作为调用别名，且不会产生第二个技能或重复加载。`install_skills.py` 中的 `TARGET_DIR_NAME` 与 `SKILL_NAME` 为唯一映射来源。

V0.2 技能包完整保留在工作区 `engineering-thermophysics-zh-controlled-language/` 与 `dist/engineering-thermophysics-zh-controlled-language.zip`，作为回滚基线；其内容不参与新结构的加载。
