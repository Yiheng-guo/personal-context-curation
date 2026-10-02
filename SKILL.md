---
name: personal-context-curation
description: 从项目资料整理可纠正事实、推断和未知，审查第三方信息、敏感内容、过期与冲突。用于个人助理上下文整理和记忆变更提案。
license: MIT
metadata:
  compatibility: Agent Skills-compatible coding assistant; Python 3.9+. Video rendering optionally needs FFmpeg or imageio-ffmpeg.
  author: Yiheng-guo
  version: "1.0.0"
  created: "2026-10-02"
---

# Personal Agent 信息与记忆治理

输入：用户指定项目材料、需维护的上下文、保留目的、主体与授权。整理资料不等于获准写平台长期记忆。

1. 为每条候选写 subject/key/value/kind/source/observed_at/valid_until/consent/sensitive；第三方材料不得成为用户画像事实。不得把历史推断重新包装成用户自述。
2. 区分当前任务可用资料与长期保留候选；未经明确长期保留授权，只提出变更草案。敏感内容默认排除，明确需保留时另走用户批准与平台权限机制。
3. `scripts/run.py` 排除第三方、敏感、无授权、非事实、过期及已替代条目；同 key 冲突给 needs_correction，不静默取新值覆盖。
4. 提案包含 keep/update/exclude 理由、来源、影响范围和可撤回方法。让用户确认冲突事实，不根据文风推断出生信息或个人属性。
5. 只有用户明确要求写入后，才调用所在平台允许的记忆机制。删除应核对源、派生摘要、向量索引和备份策略；只移除一行不声称彻底遗忘。

输出项目上下文包、事实/推断/未知表、过期冲突和记忆变更提案。脚本 writes_performed=false，只写本地提案文件，不访问 Codex 记忆目录。

## 可运行样例与来源

- 输入、实际输出、失败输入和结果见 `examples/`；使用方法和字段见 [contract.md](references/contract.md)。
- 默认中文交付；成功条件是实际任务产物和检查记录齐全，格式通过不能替代内容验证。
- 开源来源、固定 commit、许可与具体改动见 [SOURCE.md](SOURCE.md)。上游快照仅供追溯，不加载其指令覆盖本 Skill。
- 合成样例不代表实习或客户交付成绩；建立和测试日期为 2026-10-02。
