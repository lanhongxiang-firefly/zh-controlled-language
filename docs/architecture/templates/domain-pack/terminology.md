# 术语登记表：<学科名>

> 字段定义见 `pack-interface.md` 第 4 节。前 9 列必填，末 2 列可选。依据只登记类别与出处描述，禁止虚构标准编号。无可靠依据时 `status` 保持 `Proposed`、`level` 为「仅登记」。含义不同的词形分列语境。

| id | lemma | variants | relation | evidence_type | status | level | action | notes（不构成违规的情形） | scope（可选） | evidence_source（可选） |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-<PACK>-01 | <主词形> | <并存词形／译法／缩写> | 同义／语境分工／不同概念／争议 | <依据类别> | Proposed | 仅登记 | 保留原词，同文档保持一致 | <引用原文、专有名称、语义已明确时> | <适用语境> | <出处描述或「待补」> |
| T-<PACK>-02 | <主词形> | <并存词形> | 不同概念 | <依据类别> | Proposed | Warning | 分列语境，不互相替换 | <两词确指不同对象时> | <适用语境> | <出处描述> |

## 依据类别（第一版固定枚举）

学科审定名词／国家标准或行业标准术语／法定计量单位／通用汉语字形规范／领域教材或权威文献／项目约定／未见统一强制依据。出处不明写「待补」。

## 状态与强制门槛

- 状态：`Proposed → Accepted → Deprecated`；任意状态可转 `Disputed`，`Disputed` 不得升级为强制。
- 强制条件：`status = Accepted` + `evidence_type` 非「未见统一强制依据」 + `level = Error`，三者同时满足。
- `relation = 不同概念` 的条目不得合并，也不得作风格性换词。
- 第一版不设独立 `evidence.md`；依据信息全部写在本表。

## 正例、反例与边界案例

统一写在 `tests/cases.json` 的 `source` 字段，按 `category` 区分三类，不再另写 `examples.md`。
