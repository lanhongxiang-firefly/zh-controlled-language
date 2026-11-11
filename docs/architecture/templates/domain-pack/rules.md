# 学科特有规则：<学科名>

> 只补充 Core 未覆盖的学科约束。`does_not_apply_when` 必填；Core 已有规则不重复定义。字段定义见 `pack-interface.md` 第 5 节。

## R-<PACK>-01

| 字段 | 内容 |
| --- | --- |
| `id` | R-<PACK>-01 |
| `level` | Warning |
| `statement` | <规则正文> |
| `applies_when` | <适用条件> |
| `does_not_apply_when` | <不构成违规或可保留的语境，必填> |
| `evidence` | <依据类别；出处描述见 terminology.md> |
| `source_pack` | <pack-id> |

## R-<PACK>-02

| 字段 | 内容 |
| --- | --- |
| `id` | R-<PACK>-02 |
| `level` | Suggestion |
| `statement` | <规则正文> |
| `applies_when` | <适用条件> |
| `does_not_apply_when` | <可保留的语境，必填> |
| `evidence` | <依据类别> |
| `source_pack` | <pack-id> |

## 约束

- 第一版不定义新的 Error 级规则，除非对应术语条目满足 `terminology.md` 的强制门槛。
- 不规定句长、段落长度、标题层级、连接词数量等机械阈值。
- 不把本学科术语规范应用于其他学科文本；未加载本 Pack 的会话不得引用上述条目。
