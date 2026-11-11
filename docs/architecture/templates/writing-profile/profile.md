---
id: <profile-id>
name: <文体中文名>
strength: full
---

# 文体规范：<文体名>

> 第一版 Profile 只有 3 个 frontmatter 字段；不设 version、core_version、status、core_compat、applies_to。字段定义见 `pack-interface.md` 第 7 节。

## 适用强度

| 级别 | 本 Profile 下是否生效 | 说明 |
| --- | --- | --- |
| Error | 始终生效 | Core 的原文保护与真实错误纠正 |
| Warning | <生效／按需> | `strength = error-only` 时不生效 |
| Suggestion | 默认不改 | 由上下文决定 |

`strength` 取 `full` 或 `error-only`；`error-only` 对应日常专业交流，仅 Core 的 Error 生效。

## 信息组织偏好（Suggestion）

- <结论是否前置、段落与标题层级、清单颗粒度等>
- 每条须写明「由文体与读者决定，不作为错误判据」。

## 表达偏好（Suggestion）

- <人称、第二人称、语气强度、情态词择一、铺垫语等>
- 每条须写明「默认不改」。

## 正例与边界案例

1.（<文本类型>）「<原文>」→ 不修改。依据：<可保留的语境>。
2.（<文本类型>）「<原文>」→ Warning 建议，不硬改。依据：<上下文说明>。

## 禁止事项

- 不定义术语、译法、缩写或学科特有规则。
- 不规定句长、段落长度、标题层级等硬性阈值。
- 不覆盖或削弱 Core 的 Error 级保护。
