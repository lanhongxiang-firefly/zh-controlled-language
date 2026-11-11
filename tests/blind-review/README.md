# tests/blind-review

独立盲评与真实项目文本测试材料。现有 `core/results.json` 等观测记录由规则制定方填写，存在同源偏差；本目录提供把观测交给独立评审方的流程。

| 文件 | 用途 |
| --- | --- |
| `protocol.md` | 独立性要求、材料生成、填写口径、汇总方法与局限 |
| `generate_materials.py` | 从三组 `cases.json` 生成剥离答案的盲评材料 |
| `blind-cases.json`、`review-sheet.md`、`observations-template.json` | 生成物，供评审方使用；源用例变更后需重跑生成脚本 |
| `summarize.py` | 对比观测与期望，输出误判清单与 `RESULTS.md` |
| `corpus-template.json` | 真实项目文本语料空模板，登记后另存为 `corpus.json` 即自动纳入并按模块单独统计 |
| `real-corpus.md` | 真实项目文本的选取、脱敏与授权登记规范 |

```text
python tests/blind-review/generate_materials.py
# 由独立评审方填写 observations.json
python tests/blind-review/summarize.py
```

当前状态：协议、材料与汇总脚本已建立；尚无独立评审方填写的 `observations.json`，`real-corpus` 中尚无外部真实项目文本语料。独立盲评与真实文本测试尚未执行，不得据此宣称误判率已通过独立验证。
