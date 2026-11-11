# 独立盲评与真实项目文本测试协议

## 1 目的

现有 28 条用例（Core 19、Domain Pack 6、集成 3）的 `results.json` 由规则制定方填写，存在同源偏差。本协议规定把观测交给独立评审方，并规定真实项目文本的登记与复核方式。本协议不改变已提交的自评基线，也不修改 `core/`、`skill/SKILL.md`。

## 2 独立性要求

- 评审方未参与 Core 规则、术语登记、Domain Pack 规则与测试用例的编写。
- 交付给评审方的材料只有 `blind-cases.json`、`review-sheet.md`、`observations-template.json`、三份 Core 规则文件与已加载 Pack 的规则文件。
- 不向评审方提供 `cases.json`、`results.json`、各组 `RESULTS.md` 与 `answer key`。判定所需的期望答案不落盘；`summarize.py` 直接从已提交的 `cases.json` 读取，不生成答案文件。
- 评审方按 `core/language-rules.md`、`core/terminology-governance.md`、`core/quality-control.md` 与 `domains/<id>/rules.md` 独立判定。
- 评审记录保留评审方标识、日期与所用规则版本；不得回填或修改已提交的自评基线。

## 3 材料生成

```text
python tests/blind-review/generate_materials.py
```

从 `core/cases.json`、`domains/engineering-thermophysics/tests/cases.json`、`tests/integration.json` 生成 28 条盲评用例。每条只保留 `id`、`module`、`text_type`、`source` 与动作取值枚举；剥离 `category`、`expected_action`、`expected_level`、`dimension`、`rationale`。用例编号加模块前缀，避免跨组重名。生成过程确定性，只用 Python 标准库。

## 4 评审填写

评审方为每条用例填写：

- `observed_action`：`no_change` / `error_fix` / `warning_note` / `review` 之一。
- `observed_level`：`none` / `Error` / `Warning` / `Suggestion`。级别仅作记录，不单独计入误判统计。
- `note`：判定依据或修改建议，可空。

填写结果保存为 `observations.json`，结构见 `observations-template.json`。误判统计以 `observed_action` 是否等于 `expected_action` 为准，与 `tests/run_tests.py` 的 `classify()` 口径一致。

## 5 汇总

```text
python tests/blind-review/summarize.py
```

对比观测与期望，按 `category` 分类误判：正例判为需改动记「过度修改」，边界例记「分级误判」，反例判为不改动记「漏判」。输出 `RESULTS.md`，含评审方、规则版本、用例数、误判清单与级别标注一致数。脚本只做确定性计数，不做语义判断。

## 6 真实项目文本测试

`real-corpus.md` 规定语料来源、选取标准、脱敏与授权状态登记。当前仓库尚无外部真实项目文本语料；`experiment/report.md` 第七节记录过一段真实会话文本的复核，样本量为 1 且由规则制定方复核，不能代表真实项目文本分布。

真实语料按 `real-corpus.md` 登记为 `corpus.json` 后，两个脚本自动纳入，用例编号前缀为 `real-corpus:`，汇总时按模块单独列出用例数与误判数，不与构造语料合并统计。真实语料的期望判定须由独立标注方给出，不得由规则制定方自评充当金标准。

## 7 局限

- 仓库公开，`cases.json` 本身可被查阅；独立性依赖协议约定，而非技术隔离。对外评审时应只发送盲评材料，不指向仓库中的答案文件。
- 单一评审方仍可能引入个体偏差；建议不少于两名评审方分别填写后比较一致性。
- 判定口径依赖评审方对规则文件版本的理解，需在 `observations.json` 记录 `rules_version`。
- 本框架检验规则判定的一致性，不测量阅读效率或理解正确率。
