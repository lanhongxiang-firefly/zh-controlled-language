# 扩展包与文体规范接口（收敛版 R2，含已决定项）

本文件定义第一版（v1）的模块契约。目标是：新增一个学科时，只需新增一个符合本接口的目录，不修改 `core/` 与 `skill/SKILL.md`。

标记：**Required v1** 第一版必需；**Deferred** 未来改进；**已决定** 维护者于 2026-11-11 对 D-1／D-2／D-3 作出的决定（见 `ADR-0001.md` 第 8 节）。本版无未决 Open 项；架构整体批准与迁移已于 2026-11-11 完成，见 `ADR-0001.md` 第 9 节。

## 1 通用约定（Required v1）

- 每个模块自带 `manifest.yaml`；`id` 为 kebab-case，全局唯一且与目录名一致。
- 模块不引用其他 Pack 的内部条目。
- 依据只登记类别与出处描述，禁止虚构标准编号或未经核实的文献信息。
- 规范文件为 Markdown／YAML／JSON，不引入运行时依赖。
- 模块级状态只有 `enabled`；条目级状态为四态，两者互不混用（见 `ADR-0001.md` 3.4）。

按 D-2，Core 只含通用语言规则与术语治理机制，不持有科研专业词汇表。「误差」「测量不确定度」「显著」等跨学科词汇由各 Pack 按本领域定义与实际需要自行登记，不要求收录全部科研词汇；共享资源抽取为 Deferred（F-7）。

按 D-1，技能包更名为通用名，旧名保留别名；目录名迁移与别名映射在实施阶段由安装脚本统一处理，贡献者不改目录名。

## 2 Domain Pack manifest（Required v1）

```yaml
id: engineering-thermophysics
name: 工程热物理
version: 0.1.0
core_version: "0.2"
enabled: true
maintainers: [<责任人>]
description: 工程热物理领域术语、符号与学科特有表达规范
```

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `id` | 是 | 与目录名一致 |
| `name` | 是 | 展示名 |
| `version` | 是 | 模块自身版本号，仅作标记 |
| `core_version` | 是 | 精确字符串匹配 Core 版本；第一版不做范围解析 |
| `enabled` | 是 | `false` 的模块不参与加载 |
| `maintainers` | 是 | 至少一名责任人 |
| `description` | 是 | 用途与触发说明 |

**Deferred**：`core_compat` 范围表达式、兼容矩阵、预设 Profile 组合、模块级审核策略、独立发布标签。第一版不实现，也不得在 manifest 中出现这些字段。

## 3 Domain Pack 目录（Required v1）

```text
domains/<id>/
├── manifest.yaml
├── terminology.md       # 术语条目（含依据类别与状态）
├── rules.md             # 学科特有规则
└── tests/
    └── cases.json       # 正例／反例／边界案例
```

`evidence.md` 与 `examples.md` 已合并：依据写入术语条目的 `evidence_type`／`evidence_source`，示例即 `cases.json` 的 `source` 字段。第一版不设独立依据文件与示例文件。

## 4 术语条目（Required v1）

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `id` | 是 | 条目唯一编号 |
| `lemma` | 是 | 主词形 |
| `variants` | 是 | 并存词形、缩写、译法 |
| `relation` | 是 | `同义`／`语境分工`／`不同概念`／`争议` |
| `evidence_type` | 是 | 依据类别；无依据写「未见统一强制依据」 |
| `status` | 是 | `Proposed`／`Accepted`／`Deprecated`／`Disputed` |
| `level` | 是 | `Error`／`Warning`／`Suggestion`／`仅登记` |
| `action` | 是 | 具体处置 |
| `notes` | 是 | **不构成违规的情形** |
| `scope` | 否 | 适用语境与文献范围 |
| `evidence_source` | 否 | 出处描述；不明写「待补」 |

依据类别（第一版固定枚举）：学科审定名词、国家标准或行业标准术语、法定计量单位、通用汉语字形规范、领域教材或权威文献、项目约定、未见统一强制依据。

**强制门槛**：`status = Accepted` 且 `evidence_type` 非「未见统一强制依据」且 `level = Error`，三者同时满足时条目才可作为强制规则。其余一律为 Warning、Suggestion 或仅登记。

状态机：`Proposed → Accepted → Deprecated`；任意状态可转 `Disputed`，`Disputed` 不得升级为强制。第一版不设复核记录表与升级审批流程（Deferred）。

`relation = 不同概念` 的条目不得合并，也不得作风格性换词。

## 5 规则条目（Required v1）

每条含 `id`（`R-<pack>-<nn>`）、`level`、`statement`、`applies_when`、`does_not_apply_when`（必填）、`evidence`、`source_pack`。

`does_not_apply_when` 沿用 V0.2 的误判控制要求；缺失该字段的条目不予受理。Pack 不重复定义 Core 已有规则，只补充学科特有约束。第一版 Pack 不定义新的 Error 级规则，除非对应术语条目满足第 4 节强制门槛。

## 6 测试集（Required v1）

`cases.json` 每条字段：`id`、`category`（`positive`／`negative`／`boundary`）、`text_type`、`source`、`expected_action`、`expected_level`、`dimension`、`rationale`；可选 `pack_id`、`term_id`。`source` 同时承担示例作用，不再另写示例文件。

顶层保留 `dimensions`、`text_types`、`actions`、`cases` 四个键，供执行器做结构校验；格式见 `templates/domain-pack/tests/cases.json`。

**统一执行命令**：`python tests/run_tests.py <module-dir>`。执行器位于 `tests/run_tests.py`，接受模块目录参数，读取该目录下的 `cases.json`，做结构校验、误判统计并生成 `RESULTS.md`。各模块不自带执行器副本。

集成用例统一放在 `tests/integration.json`，由同一执行器读取，用于组合与误用检测；不再设 `tests/integration/` 目录。

每 Pack 至少覆盖正例、反例、边界各 1 条。`results.json` 记录观测处置与评审方；评审方为规则制定方时，`RESULTS.md` 须标注同源偏差。

## 7 Writing Profile（Required v1）

```yaml
id: technical-documentation
name: 技术文档与使用手册
strength: full            # full | error-only
```

Profile 正文只含：适用强度、信息组织偏好、表达偏好（Suggestion 级）、正例与边界案例。`error-only` 时仅 Core 的 Error 生效，对应日常专业交流。

Profile 不得包含术语清单、译法、学科约束或 Error 级规则。第一版只建 `technical-documentation` 一个示例；其余文体为 Deferred。Profile 不设 `version`、`core_version`、`status`、`core_compat` 字段。

## 8 加载契约（Required v1）

1. 读取默认学科：使用者首次配置时写入 `skill/defaults.yaml`；本机默认工程热物理，公开版该字段为空。单次任务默认使用该 Pack，不需重复声明。用户明确要求时临时切换到其他学科，切换只影响本次任务。配置缺失且未指定时只加载 Core。
2. 校验 `id`、`core_version` 与 `enabled`；`enabled: false` 或版本不匹配的模块拒绝加载并记录原因。
3. 加载 Core；加载指定 Pack；加载指定 Profile。
4. 构建本次会话的模块白名单，判定只引用白名单内条目。
5. 学科未知时白名单只含 Core，不推断专业术语规范。
6. 判定优先级：Core Error ＞ 已加载且 Accepted 的 Pack 条目 ＞ Profile 的 Suggestion ＞ 未加载内容。
7. 术语冲突时保留各词形与上下文、登记待确认，不强制统一；依据不足时保留原词，不创造译法。

## 9 最小 stub Pack（验收方法）

用于验证「新增学科不改 Core 与 Skill」，不属于接口必需内容。第一版实施阶段用它做一次集成验证即可。

```yaml
id: stub-discipline
name: 模拟学科
version: 0.1.0
core_version: "0.2"
enabled: true
maintainers: [integration-test]
description: 用于跨学科模拟测试
```

```yaml
id: T-STUB-01
lemma: 示例术语
variants: [示例译法甲, 示例译法乙]
relation: 争议
evidence_type: 未见统一强制依据
status: Proposed
level: 仅登记
action: 保留原词，标记待确认
notes: 不得据此改写其他学科文本
```

断言：加载后 `core/` 与 `skill/SKILL.md` 文件内容不变；未加载该 Pack 的会话不得引用 `T-STUB-01`；两个 Pack 出现同名词形时保留上下文且不强制统一。

## 10 第一版不实现（Deferred）

语义化版本范围与兼容矩阵、模块级状态机、预设 Profile 组合、领域复核角色与审批流程、复核记录表、独立发布标签、6 类 Profile、Core 内子目录、tests 三层目录、多渠道发布与许可证、共享科研词汇资源抽取（F-7）。详见 `ADR-0001.md` 第 1 节与第 8 节。

D-1／D-2／D-3 已决定并写入本文件；架构整体批准与迁移已于 2026-11-11 完成，实施结果见 `ADR-0001.md` 第 9 节。
