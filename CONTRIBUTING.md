# 贡献指南

新增学科扩展包或修改文体规范，请先阅读 `docs/architecture/pack-interface.md` 与 `docs/architecture/CONTRIBUTING.md`。贡献者只需理解这两份文件，不必熟悉 Core 的全部规则或 Skill 的实现。

## 最小流程

1. 复制 `docs/architecture/templates/domain-pack/` 到 `domains/<id>/`，目录名与 `manifest.yaml` 的 `id` 一致。
2. 填写 manifest、术语条目（状态从 `Proposed` 起步）、学科规则（每条含「不构成违规的情形」）与正例／反例／边界用例。
3. 运行 `python tests/run_tests.py domains/<id>`，确认结构校验通过并查看误判记录。
4. 按 `docs/architecture/CONTRIBUTING.md` 第 4 节的 PR 模板提交。

## 约束

- 不修改 `core/` 来适配单一学科；不在 Writing Profile 中写术语、译法或学科约束。
- 未经可靠依据支持、或状态为 `Proposed`／`Disputed` 的条目不得设为 Error 级。
- 不虚构标准编号、文献信息或确认记录。
- 不预设默认学科，不修改技能包目录名（更名与别名映射由维护者统一处理）。
- 新增 Pack 不应影响其他 `domains/`、任何 `profiles/` 或 `skill/SKILL.md`。

## 测试

```text
python tests/run_tests.py --integration --strict
```

术语与规则的审核门槛、状态机、依据类别与独立发布约定见 `docs/architecture/pack-interface.md` 与 `docs/architecture/CONTRIBUTING.md`。

涉及规则或术语判定的改动，构造用例与自评基线不能替代独立盲评；材料生成、评审口径与汇总方式见 `tests/blind-review/protocol.md`。真实项目文本语料按 `tests/blind-review/real-corpus.md` 登记。

## 许可证

规范文本、术语表、模板，以及项目原创的测试用例与评测数据的表达、整理和编排采用 CC BY 4.0；可执行脚本采用 MIT。事实、方法、概念、术语本身与第三方材料不因本项目获得专有权利，边界见 `LICENSE-DOCS`「许可范围边界」。范围划分见 `README.md`「许可证」小节。提交贡献即表示同意按对应许可授权所提交内容。

贡献者需确认对所提交内容拥有授权所需权利；引用第三方文本时保留出处并说明其权利状态，不将无权再授权的第三方材料按本项目许可授权。
