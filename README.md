# 中文受控语言规范 / Chinese Controlled Language

面向科研与工程技术交流的中文受控语言规范，以及基于该规范的 Agent Skill 实现。通用核心稳定、学科扩展独立、文体规范可组合。

> 规范表达，而不是限制表达；纠正真实问题，而不是制造新的写作模板。

## 项目定位

- 中文技术写作的分级规则：Error（明确错误，必须纠正）、Warning（建议）、Suggestion（文体偏好，默认不改）。
- 只纠正真实问题：不设句长、段落长度、标题层级、连接词数量等机械阈值；原文已准确、自然、简洁时不作修改。
- 保护科学含义、技术事实、公式与数据、限定条件、证据强度与结论边界；不臆造单位、数值或判据。
- 借鉴 ASD-STE100 的受控语言思想，按中文技术写作语境独立制定规则。本项目不构成对 ASD-STE100 的合规声明。

## 架构

| 层 | 目录 | 职责 |
| --- | --- | --- |
| Core | `core/` | 通用语言规则、术语治理机制、质量控制与原文保护 |
| Domain Pack | `domains/` | 学科术语、译法依据、学科特有规则与独立测试集 |
| Writing Profile | `profiles/` | 按文体调整适用强度与表达偏好 |
| Skill 执行层 | `skill/` | 加载、白名单路由、冲突处置、按需审查记录 |

首个完整验证领域为 `domains/engineering-thermophysics/`。新增学科只需新增一个符合 `docs/architecture/pack-interface.md` 的目录，不修改 Core 与 Skill 执行层。Core 不承担科研专业词汇表；「误差」「测量不确定度」「显著」等跨学科词汇由各 Pack 按本领域定义自行登记。

## 覆盖文本

代码注释、技术文档、科研申请书、技术报告、项目材料、日志与错误提示、日常技术交流。

## 获取与安装

```text
git clone https://github.com/lanhongxiang-firefly/zh-controlled-language.git
cd zh-controlled-language
python install_skills.py
```

`install_skills.py` 按 manifest 组装技能包并同步到 WorkBuddy、Codex、DeepSeek Harness、Claude Code 的用户级技能目录，同时生成 `build/zh-controlled-language/` 作为公开分发包目录，可打包为 zip 供上传安装。

- 技能规范名为 `zh-controlled-language`；四宿主目录保留 `engineering-thermophysics-zh-controlled-language` 作为兼容别名，映射见 `skill/ALIASES.md`。
- 默认学科由使用者首次配置 `skill/defaults.yaml` 的 `default_domain`；公开版本为空。单次任务默认使用已配置的 Pack，用户明确要求时可临时切换；配置缺失时只加载 Core。
- 本机安装与公开分发包的差异、以及构建产物与备份的排除规则，见 `.gitignore` 与 `skill/ALIASES.md`。

## 测试

```text
python tests/run_tests.py --integration --strict
python tests/verify_migration.py
python tests/blind-review/generate_materials.py
```

测试集分 Core、Domain Pack、集成三组，覆盖正例、反例与边界案例，并记录误判情况。`tests/stub-pack/` 用于验证新增学科不影响 Core 与 Skill。`verify_migration.py` 为本机迁移校验，运行时需要保留 `backup/` 与四宿主安装副本。

现有观测记录由规则制定方填写，存在同源偏差。`tests/blind-review/` 提供剥离期望答案的 28 条盲评材料、评审表与汇总脚本，以及真实项目文本语料的登记规范；独立盲评与真实文本测试尚待外部评审方与语料，协议见 `tests/blind-review/protocol.md`。

## 贡献

见 `CONTRIBUTING.md`、`docs/architecture/CONTRIBUTING.md` 与 `docs/architecture/pack-interface.md`。术语条目具有 Proposed／Accepted／Deprecated／Disputed 状态；未经可靠依据支持或领域确认的条目不得升级为强制规范。涉及规则或术语判定的改动，建议同时提供 `tests/blind-review/` 的独立评审记录。

## 文档

| 文件 | 内容 |
| --- | --- |
| `docs/architecture/ADR-0001.md` | 分层架构、决策记录与迁移实施结果 |
| `docs/architecture/pack-interface.md` | Domain Pack 与 Writing Profile 接口 |
| `docs/architecture/CONTRIBUTING.md` | 贡献流程、审核门槛与 PR 模板 |
| `docs/architecture/templates/` | 可直接复制的扩展包与文体模板 |
| `docs/distribution.md` | 第一版分发渠道边界与仍待评估的渠道 |
| `docs/repository-metadata.md` | GitHub About 描述与 topics 文案、设置方式 |
| `tests/blind-review/` | 独立盲评协议、材料、汇总脚本与真实语料登记规范 |
| `experiment/` | V0.1 对照实验与历史记录 |

## 许可证

本项目按内容类型分别授权。

| 范围 | 文件 | 许可 |
| --- | --- | --- |
| 规范文本、术语表、模板、文档、测试用例与数据 | `*.md`、`*.json`、`*.yaml`、`*.txt` 及非脚本配置 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| 可执行脚本 | `*.py` | MIT |

条款见 `LICENSE-DOCS`（CC BY 4.0 声明与范围）与 `LICENSE`（MIT 全文及 Scope 说明）。GitHub 的仓库级许可证识别不能完整表示本项目按文件划分的双许可证安排；因 `LICENSE` 含范围说明，当前仓库被识别为 Other（NOASSERTION）。无论侧栏显示何种结果，实际授权范围以本文件的许可证范围表及 `LICENSE`、`LICENSE-DOCS` 为准。引用或改编规范文本时按 CC BY 4.0 署名。

许可覆盖项目原创的规范文本、测试案例、评测数据及其表达、整理与编排。规则思想、科学规律、判定方法、概念、术语与事实本身不因本项目获得专有权利；既有标准译名、专有名称与第三方材料遵循原有权利状态。项目名称与标识不在授权范围内。贡献内容默认按上表对应的许可授权。

## 状态

- 架构：ADR-0001 已批准并实施；V0.2 内容已迁移至分层结构。
- 许可证：规范文本与数据 CC BY 4.0，脚本 MIT；F-4 的许可证选型已决定，多渠道发布仍列为 Deferred，渠道边界见 `docs/distribution.md`。
- 分发：Git 仓库、技能包 zip 与四宿主本机安装均含 `LICENSE` 与 `LICENSE-DOCS`；公开版不预设默认学科。
- 验证：28 条构造用例误判 0，跨学科模拟断言 6 项通过；独立盲评与真实项目文本测试尚未执行。
- 仓库元数据：About 描述已存在，topics 待设置，文案与命令见 `docs/repository-metadata.md`。
