"""受控语言 Skill 有效性实验：确定性计数与判定表汇总。

仅使用 Python 标准库，做词形、句长与判定表的机械计数，不做语义判断。
语义判定（缺陷是否消除、信息是否保留、清单逐项结论）记录在 corpus.md，
本脚本只负责把它们汇总成可复核的数字。脚本不写入也不修改 SKILL.md。
"""

import re
from pathlib import Path

BASE = Path(__file__).parent
doc = (BASE / "corpus.md").read_text(encoding="utf-8")

BLOCK = re.compile(r"^### ([ABC])[^\n]*\n```text\n(.*?)\n```", re.M | re.S)
blocks = {"A": [], "B": [], "C": []}
for m in BLOCK.finditer(doc):
    blocks[m.group(1)].append(m.group(2))

SAMPLES = ["技术文档", "代码注释", "项目材料"]
LIMITS = [40, 30, 40]  # 正文 40 汉字；代码注释单行 30 汉字（S2、L4）

# 取自 SKILL.md 第 4.1、4.2、4.4 节及第 2.2 节弃用词形；仅作提示性计数
BANNED = [
    "众所周知", "值得一提的是", "不难看出", "显而易见",
    "进行了", "被", "所生成的", "基于", "在适当条件下",
    "基本", "大致", "较为", "相关", "相应", "一定",
    "显著", "良好", "可靠", "精度", "误差范围", "等", "等等",
    "必要时", "酌情", "最好务必", "建议必须", "尽快",
    "跑一下", "跑通", "跑起来", "调一调", "拉通", "对齐", "闭环",
    "过一遍", "拍板", "堆料", "拍一个", "差不多就行", "偷偷",
    "大家", "我们", "笔者", "实现了", "一种", "以使得", "它们",
    "换热系数", "导热性能", "热导率", "放热系数", "对流换热系数",
    "仿真", "试验", "测试",
]

# 取自 SKILL.md 2.2「不再使用的词形」列。含义不同的规范词（如准确度、
# 测量不确定度）刻意不合并，避免把术语分工误判为同义冗余。
DEPRECATED = [
    "热导率", "导热率", "导热性能",
    "对流换热系数", "换热系数", "放热系数", "给热系数",
    "压强", "热通量", "比热流", "K 值",
    "精度", "误差范围",
    "仿真", "数值仿真", "数值计算", "模拟计算",
    "试验", "测试", "实测", "校正", "校验", "调参",
    "参量", "经验公式", "拟合公式", "热交换",
    "稳定流", "不稳定流",
]
ABBR_FORMS = ["Re", "re", "R.E.", "RE", "Nu", "NU", "nu"]


def han(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def sentences(block):
    out = []
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("。") if p.strip()]
        out.extend(parts if parts else [line])
    return out


def measure(version):
    all_text = "\n".join(blocks[version])
    per_sample = []
    total_sentences = 0
    total_han = 0
    longest = 0
    over_limit = 0
    for i, block in enumerate(blocks[version]):
        lens = [han(s) for s in sentences(block)]
        lim = LIMITS[i]
        over = sum(1 for n in lens if n > lim)
        per_sample.append((SAMPLES[i], len(lens), max(lens) if lens else 0, lim, over))
        total_sentences += len(lens)
        total_han += sum(lens)
        longest = max(longest, max(lens) if lens else 0)
        over_limit += over
    hits = {w: all_text.count(w) for w in BANNED if w in all_text}
    # 长词优先，命中后从副本中移除，避免「对流换热系数」被「换热系数」重复计入
    deprecated = []
    residual = all_text
    for w in sorted(DEPRECATED, key=len, reverse=True):
        if w in residual:
            deprecated.append(w)
            residual = residual.replace(w, "")
    abbr = [w for w in ABBR_FORMS if w in all_text]
    return {
        "sentences": total_sentences,
        "han": total_han,
        "longest": longest,
        "over": over_limit,
        "per_sample": per_sample,
        "hits": hits,
        "hit_total": sum(hits.values()),
        "deprecated": deprecated,
        "abbr": abbr,
    }


DEF_ROW = re.compile(r"^\|\s*(D\d+-\d+)\s*\|[^|]*\|\s*(是|否)\s*\|\s*(是|否)\s*\|", re.M)
INF_ROW = re.compile(r"^\|\s*(I\d+-\d+)\s*\|[^|]*\|\s*(是|否)\s*\|\s*(是|否)\s*\|", re.M)
CHK_ROW = re.compile(r"^\|\s*([ABCDE]\d+)\s*\|\s*([✓✗—])\s*\|\s*([✓✗—])\s*\|\s*([✓✗—])\s*\|", re.M)
NEW_ROW = re.compile(r"^\|\s*([BC])\s*\|[^|]*\|", re.M)

defects = DEF_ROW.findall(doc)
infos = INF_ROW.findall(doc)
checks = CHK_ROW.findall(doc)
new_issues = NEW_ROW.findall(doc)

assert len(blocks["A"]) == len(blocks["B"]) == len(blocks["C"]) == 3, "样本数不匹配"
assert defects and infos and checks, "判定表解析失败"

d_total = len(defects)
i_total = len(infos)
d_b = sum(1 for _, b, _ in defects if b == "是")
d_c = sum(1 for _, _, c in defects if c == "是")
i_b = sum(1 for _, b, _ in infos if b == "是")
i_c = sum(1 for _, _, c in infos if c == "是")
new_b = new_issues.count("B")
new_c = new_issues.count("C")

m = {v: measure(v) for v in "ABC"}
chk = {}
for v, idx in (("A", 1), ("B", 2), ("C", 3)):
    applicable = [r for r in checks if r[idx] != "—"]
    passed = [r for r in applicable if r[idx] == "✓"]
    chk[v] = (len(passed), len(applicable))

lines = []
add = lines.append
add("受控语言 Skill 有效性实验｜确定性评测结果")
add("=" * 62)
add("")
add(f"样本：{len(blocks['A'])} 类文本（技术文档 / 代码注释 / 项目材料），每类 3 个版本")
add(f"植入缺陷基准：{d_total} 条；信息单元基准：{i_total} 条；校验清单：{len(checks)} 项")
add("")
add("一、判定表汇总")
add("-" * 62)
add(f"{'版本':<6}{'缺陷消除':<14}{'消除率':<10}{'残留':<8}{'新增违规':<10}{'净违规':<8}{'信息保留':<14}{'保真度':<10}")
for v, elim, newv, keep in (("A", 0, 0, i_total), ("B", d_b, new_b, i_b), ("C", d_c, new_c, i_c)):
    residual = d_total - elim
    add(f"{v:<6}{f'{elim}/{d_total}':<14}{f'{elim/d_total*100:.1f}%':<10}{residual:<8}{newv:<10}{residual+newv:<8}{f'{keep}/{i_total}':<14}{f'{keep/i_total*100:.1f}%':<10}")
add("")
add("注：A 组为原始文本，其植入缺陷视为全部残留，信息视为全部保留；")
add("    净违规 = 残留植入缺陷 + 改写引入的新增违规（按类型计）。")
add("")
add("二、确定性文本计数")
add("-" * 62)
add(f"{'版本':<6}{'句数':<8}{'汉字数':<10}{'最长句':<10}{'超限句':<10}{'禁用/慎用命中':<16}{'弃用词形种类':<14}{'缩写词形':<10}")
for v in "ABC":
    x = m[v]
    add(f"{v:<6}{x['sentences']:<8}{x['han']:<10}{x['longest']:<10}{x['over']:<10}{x['hit_total']:<16}{len(x['deprecated']):<14}{len(x['abbr']):<10}")
add("")
add("注：禁用/慎用命中为词次提示，不等于判定违规；弃用词形种类按 2.2 弃用列统计；")
add("    含义不同的规范词不合并统计；超限阈值按样本分别为 40/30/40 汉字。")
add("")
add("三、分样本句长（版本 C）")
add("-" * 62)
for name, n, longest, lim, over in m["C"]["per_sample"]:
    add(f"{name}：{n} 句，最长 {longest} 汉字，阈值 {lim} 汉字，超限 {over} 句")
add("")
add("四、校验清单符合率（— 为不适用，已排除）")
add("-" * 62)
for v in "ABC":
    p, a = chk[v]
    add(f"{v} 组：{p}/{a} = {p/a*100:.1f}%")
add("")
add("五、命中明细（供人工复核）")
add("-" * 62)
for v in "ABC":
    add(f"{v} 组禁用/慎用命中：{m[v]['hits']}")
    add(f"{v} 组弃用词形：{m[v]['deprecated']}")
    add(f"{v} 组缩写词形：{m[v]['abbr']}")
add("")
add("六、派生结论")
add("-" * 62)
add(f"B 与 C 的缺陷消除率差：{(d_c-d_b)/d_total*100:.1f} 个百分点")
add(f"B 与 C 的信息保真度差：{(i_c-i_b)/i_total*100:.1f} 个百分点")
add(f"B 与 C 的净违规差：{(d_total-d_b+new_b)-(d_total-d_c+new_c)} 条")
add(f"C 相对 A 的汉字数变化：{m['C']['han']-m['A']['han']:+d}（{(m['C']['han']/m['A']['han']-1)*100:+.1f}%）")
add("")

out = "\n".join(lines)
(BASE / "results.txt").write_text(out, encoding="utf-8")
print(out)
