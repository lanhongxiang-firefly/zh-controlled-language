# 仓库元数据（About 描述与 topics）

GitHub 仓库的 About 描述与 topics 只能通过 REST API 或网页设置，Git 推送无法写入。本文件是文案来源、执行方式与状态记录。

## 1 文案

**About 描述**（GitHub 上限 350 字符）

当前值（仓库创建时已设置，与 README tagline 一致）：

> 面向科研与工程技术交流的中文受控语言规范，以及基于该规范的 Agent Skill 实现。通用核心稳定、学科扩展独立、文体规范可组合。

建议替换值（更短，补入分级与原文保护；是否替换由维护者决定）：

> 面向科研与工程技术交流的中文受控语言规范与 Agent Skill 实现：通用核心稳定、学科扩展独立、文体规范可组合；纠正真实语言问题，保护科学含义。

**Topics**（小写字母与连字符，共 8 个）：

`chinese` · `controlled-language` · `technical-writing` · `style-guide` · `documentation` · `agent-skill` · `writing-guide` · `engineering-thermophysics`

**Homepage**：暂不设置。

## 2 设置方式

需要先取得对该仓库具备管理写权限的 Personal Access Token：classic PAT 需 `repo` 作用域；fine-grained PAT 需 Repository permissions → Administration: Read and write。Token 仅在本机终端使用，不写入仓库。

```bash
REPO=lanhongxiang-firefly/zh-controlled-language
TOKEN=<your-token>

curl -L -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/$REPO \
  -d '{"description":"面向科研与工程技术交流的中文受控语言规范与 Agent Skill 实现：通用核心稳定、学科扩展独立、文体规范可组合；纠正真实语言问题，保护科学含义。"}'

curl -L -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/$REPO/topics \
  -d '{"names":["chinese","controlled-language","technical-writing","style-guide","documentation","agent-skill","writing-guide","engineering-thermophysics"]}'
```

网页方式：仓库首页右侧 About 区域的齿轮图标，填写 Description 与 Topics 后保存。也可在会话中通过 GitHub 连接器设置。

`PATCH /repos/{owner}/{repo}` 更新描述，`PUT /repos/{owner}/{repo}/topics` 整体替换 topics；两者都需要认证与仓库管理权限。

## 3 核验

```bash
curl -s https://api.github.com/repos/$REPO | grep -E '"description"'
curl -s https://api.github.com/repos/$REPO/topics
```

也可读取 `https://api.github.com/repos/$REPO/license` 核验许可证识别状态。

## 4 状态

- 2026-11-11 核验（GitHub REST API）：`description` 已有值，与 README tagline 一致；`topics` 为空数组；`homepage` 为 null；`license` 为 `other / NOASSERTION`。
- 文案与执行方式已写入本文件。本会话未改动任何 GitHub 仓库元数据：本机未安装 `gh`，无可用 GitHub token 或凭据文件，REST API 需要认证，会话内也没有可直接写入仓库元数据的工具。
- 待办：设置第 1 节的 8 个 topics；决定是否替换 About 描述取值。执行第 2 节命令、在网页端操作，或启用 GitHub 连接器后，把本节改为「已设置」并注明日期与核验结果。
