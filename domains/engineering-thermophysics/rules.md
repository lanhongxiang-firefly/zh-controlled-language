# 学科特有规则：工程热物理

> 只补充 Core 未覆盖的学科约束。`does_not_apply_when` 必填。Core 的 E3／E4 已覆盖「臆造单位」「概念混淆」，本 Pack 不重复定义 Error 级规则。

## R-ET-01 准则数与量符号一致性

| 字段 | 内容 |
| --- | --- |
| `level` | Warning |
| `statement` | 准则数（Re／Nu／Pr／Ma／Pe／Bi／Gr／Ra／St）与量符号（T／t／p／ρ／λ／c_p／q／Φ）在同一文档内保持同一写法；首次出现宜给出中文全称。 |
| `applies_when` | 技术文档、论文稿件、数据说明中出现准则数或量符号时 |
| `does_not_apply_when` | 引用原文、公式内部、图表原有标注、既有标准或教材中的固定写法 |
| `evidence` | 学科通用写法；依据类别「领域教材或权威文献」 |
| `source_pack` | engineering-thermophysics |

## R-ET-02 术语按对象分工

| 字段 | 内容 |
| --- | --- |
| `level` | Warning |
| `statement` | 「传热／换热」按学科统称与设备语境分工；「稳态／瞬态」与「定常／非定常」按传热过程与流动描述分工；「实验／试验」按取得数据与装置或样机考核分工。 |
| `applies_when` | 同一文档内需要区分对象或过程类型时 |
| `does_not_apply_when` | 文献中混用且上下文已明确所指；引用原文或既有标准译名 |
| `evidence` | 术语登记表 B 层；依据类别「项目约定」 |
| `source_pack` | engineering-thermophysics |

## R-ET-03 结果评价量分列

| 字段 | 内容 |
| --- | --- |
| `level` | Warning |
| `statement` | 误差、偏差、测量不确定度、准确度、精密度须按各自定义分列；「精度」为泛指，须写明所指。 |
| `applies_when` | 实验数据说明、不确定度评定、结果讨论中 |
| `does_not_apply_when` | 已给出明确定义或引用特定评定规范时；日常交流中的定性表述 |
| `evidence` | 按 D-2 由本 Pack 按本领域定义登记；依据类别「领域教材或权威文献」 |
| `source_pack` | engineering-thermophysics |

## R-ET-04 同文档并存词形一致

| 字段 | 内容 |
| --- | --- |
| `level` | Warning |
| `statement` | 同一文档内，同一概念的并存词形宜择一并保持一致；不禁止任何词形。 |
| `applies_when` | 术语登记表 B 层条目在文中反复出现时 |
| `does_not_apply_when` | 两词含义不同且已分列语境；引述不同文献的原有词形 |
| `evidence` | Core 术语治理机制 W7；依据类别「未见统一强制依据」 |
| `source_pack` | engineering-thermophysics |

## 约束

- 不定义新的 Error 级规则；概念混淆与单位臆造由 Core 的 E4／E3 处理。
- 不规定句长、段落长度、标题层级、连接词数量等机械阈值。
- 未加载本 Pack 的会话不得引用上述条目；其他学科的词汇规范不由本 Pack 判定。
