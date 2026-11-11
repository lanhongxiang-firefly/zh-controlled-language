# 分发渠道边界

本文记录第一版实际支持的分发渠道，以及仍待评估的渠道。F-4 的许可证选型已由维护者决定，见 `README.md`「许可证」小节；多渠道发布仍列为 Deferred。本文不改变该状态，只明确其范围与再评估条件。

## 1 第一版已支持

| 渠道 | 入口 | 内容 | 默认学科 |
| --- | --- | --- | --- |
| Git 仓库 | `git clone` 本仓库 | 全部受版本控制文件，含 `core/`、`domains/`、`profiles/`、`skill/`、`docs/`、`tests/`、`experiment/` 与两份许可文件 | 公开版 `default_domain: ""` |
| 技能包 zip | `dist/zh-controlled-language.zip` | `build/zh-controlled-language/` 内的 13 个文件，含 `LICENSE` 与 `LICENSE-DOCS` | 公开版为空 |
| 本机四宿主安装 | `python install_skills.py` | 按 `FILE_MAP` 组装同上 13 个文件，写入 WorkBuddy、Codex、DeepSeek Harness、Claude Code 的用户级技能目录 | 本机写入 `engineering-thermophysics` |

`build/` 与 `dist/` 由 `.gitignore` 排除，属于构建产物；Git 仓库是唯一版本化来源。`install_skills.py` 的 `FILE_MAP` 是包内文件清单的唯一映射来源，`tests/verify_migration.py` 校验公开包、zip 与四宿主副本的一致性。

## 2 仍待评估（Deferred）

- GitHub Releases 版本化附件与变更记录。
- 技能市场或注册表上架。
- 语言包管理器分发。
- 单个 Domain Pack 独立发布与独立打标签。
- 按 Writing Profile 组合的预置技能包。

再评估条件：出现多版本并存需求、第三方请求单独获取某个 Pack、或出现需要按渠道区分默认配置的真实使用场景。在这些需求出现前不新增渠道，避免维护多套产物、版本号与兼容性矩阵。

## 3 约束

- 新增渠道不得修改 `core/` 与 `skill/SKILL.md`；`tests/baseline.json` 的哈希基线保持不变。
- 每个渠道的产物必须包含 `LICENSE` 与 `LICENSE-DOCS`。
- 公开渠道不预设默认学科；本机安装才写入维护者指定的默认学科。
- 渠道清单变更须同步 `install_skills.py`、`tests/verify_migration.py` 与本文件。
