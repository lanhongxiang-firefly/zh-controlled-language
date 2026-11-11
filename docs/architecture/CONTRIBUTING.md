# 贡献指南（收敛版 R2，含已决定项）

面向希望新增或维护学科扩展包、文体规范的研究者。贡献者只需理解本文件与 `pack-interface.md`，不必熟悉 Core 的全部规则或 Skill 的实现。本指南只覆盖第一版（v1）；D-1／D-2／D-3 已由维护者决定，见第 7 节与 `ADR-0001.md` 第 8 节。

## 1 角色

| 角色 | 职责 |
| --- | --- |
| 贡献者 | 编写条目、依据与测试，提交变更 |
| 维护者 | 核对接口合规性，确认术语状态升级，合并变更 |

第一版不设独立领域复核角色与审批流程；由贡献者提供依据、维护者确认。此项为 Deferred。

## 2 新增一个 Domain Pack（5 步）

1. 复制 `templates/domain-pack/` 到 `domains/<id>/`，目录名与 `manifest.yaml` 的 `id` 一致。
2. 填写 `manifest.yaml`：`core_version` 写当前 Core 版本，`enabled` 初始为 `false`，`maintainers` 至少一人。
3. 在 `terminology.md` 登记术语：填全 `pack-interface.md` 第 4 节的必填字段；无依据时 `evidence_type` 写「未见统一强制依据」、`status` 保持 `Proposed`。在 `rules.md` 补充学科特有规则，每条必填 `does_not_apply_when`。
4. 在 `tests/cases.json` 按统一格式至少写正例、反例、边界各 1 条；运行 `python tests/run_tests.py domains/<id>`，确认结构校验通过并查看误判记录。
5. 把 `enabled` 改为 `true`，按第 4 节模板提交 PR。

新增 Pack 不修改 `core/`、其他 `domains/`、任何 `profiles/` 或 `skill/SKILL.md`。确有必要时单独说明理由，交维护者评审。

## 3 术语条目要求

- 并存词形只登记，不禁止；只有 `Accepted` + 有效依据 + `Error` 三者齐备才可强制。
- 不得把争议译法、内部简称、设备昵称写成强制规范。
- 含义不同的词形须分列语境，不合并、不互相替换。
- 引用教材或文献时描述出处类型即可；具体编号暂缺写「待补」，不臆造。
- 术语冲突时保留各自词形与上下文，交由集成用例登记，不强制统一。
- 状态：`Proposed → Accepted → Deprecated`；任意状态可转 `Disputed`，`Disputed` 不得升级为强制。

## 4 Pull Request 模板

```markdown
## 变更类型
- [ ] 新增 Domain Pack
- [ ] 术语条目
- [ ] 学科规则
- [ ] Writing Profile
- [ ] Core 变更（需维护者评审）

## 模块
id: <pack-id 或 profile-id>
version: <版本号>
core_version: <精确版本>

## 依据与状态
- 依据类别：
- 出处描述（不明写「待补」）：
- 条目状态：Proposed / Accepted / Deprecated / Disputed

## 影响范围
- 是否修改 core/ 或其他模块：否 / 是（说明理由）
- 未加载时是否会被误用：已验证 / 待验证
- 测试：python tests/run_tests.py <module-dir> → 通过 / 未通过
- 误判记录：见 RESULTS.md

## 声明
- [ ] 未虚构标准编号或文献信息
- [ ] 未把未确认术语设为强制规则
- [ ] 未把学科规则写入 Core
```

## 5 测试与误判

- 通用执行器位于 `tests/run_tests.py`，接受模块目录参数；集成用例位于 `tests/integration.json`。
- 评审方为规则制定方时，`RESULTS.md` 须标注同源偏差，并建议独立复核。
- 发现误判时追加用例、写明 `rationale`、重跑执行器，修正措施写入 PR 的「影响范围」。

## 6 禁止事项

- 不修改 Core 来适配单一学科。
- 不在 Profile 中写入术语、译法或学科约束。
- 不把 `Proposed`／`Disputed` 条目写成 Error 级。
- 不虚构依据、标准编号或确认记录。
- 不在未加载其他 Pack 的会话中引用其条目。
- 不为风格统一替换文献中实际使用的词形。

## 7 第一版不要求

语义化版本范围、兼容矩阵、独立发布标签、复核记录表、领域复核角色、升级审批流程、6 类 Profile、多渠道发布与许可证、共享科研词汇资源。这些记在 `ADR-0001.md` 的 Deferred 清单中，待实际使用提出需求后再评估。

维护者已于 2026-11-11 决定 D-1／D-2／D-3，贡献者按以下约束参与：

- 按 D-2，只登记本领域实际需要规范的词汇；「误差」「测量不确定度」「显著」等跨学科词汇按本 Pack 的定义与语境登记，不写入 Core，也不要求收录全部科研词汇。
- 按 D-3，默认学科由使用者配置；贡献者不预设默认学科，也不在 Pack 中声明全局默认。
- 按 D-1，技能包更名与别名映射由维护者在实施阶段统一处理；贡献者不修改技能包目录名。
