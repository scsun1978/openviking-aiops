# OpenViking AI 运维系统

## 项目导航
- [[docs/01-项目总览]] - 项目总览、双层架构、核心原则
- [[docs/02-研发架构]] - 研发层详细架构设计
- [[docs/03-运维架构]] - 运维层详细架构设计
- [[docs/04-开发工作流]] - 研发工作流设计
- [[05-任务看板]] - 任务管理和追踪
- [[docs/15-OpenViking-AIOps-开发指南]] - 完整开发指南
- [[docs/16-AIDevVault框架应用分析]] - AIDevault 框架应用分析

## 子目录
- [[templates/README]] - 模板使用指南
- [[templates/任务模板]] - 标准任务文件格式
- [[templates/ADR-模板]] - 架构决策记录模板
- [[templates/openclaw-任务下发模板]] - 任务下发格式
- [[templates/claude-code-执行模板]] - 执行流程模板
- [[docs/]] - 项目文档

## 技能指南
- [[skills/claude-code/SKILL_GUIDE]] - Claude Code 完整技能指南（参考 AIDevault）

## 提示词
- [[prompts/openviking-aiops-development]] - OpenViking AI 运维系统开发提示词

## 当前重点
- 当前阶段：项目总览完成，准备需求分析
- 当前里程碑：✅ AIDevault 框架完成 → ✅ OpenViking 项目现状分析 → ✅ 框架应用分析 → ✅ 双层架构设计 → ✅ 项目总览完成 → 🎯 开始需求分析
- 当前主任务：[[tasks/DEV-OV-001]] - 框架应用分析（已完成）
- 待开始任务：[[tasks/DEV-OV-002]] - 需求分析
- 待开始任务：[[tasks/DEV-OV-003]] - 架构设计

## 当前成果
- AIDevault 开发框架（参考）：
  - 完整的开发链路已建立
  - 7 个任务全部完成（DEV-001 ~ DEV-007）
  - 完整的项目指南和技能指南
  - 完整的 CI/CD 流程（GitHub Actions，100% 成功率）

- OpenViking AI 运维系统：
  - ✅ OpenViking 项目现状分析完成
  - ✅ AIDevault 框架应用分析完成
  - ✅ 双层架构设计完成（研发层 + 运维层）
  - ✅ 项目总览文档完成（docs/01-项目总览.md）
  - ✅ 开发指南完成（docs/15-OpenViking-AIOps-开发指南.md）
  - ✅ 开发提示词完成（prompts/openviking-aiops-development.md）
  - ✅ 框架应用分析完成（docs/16-AIDevVault框架应用分析.md）

## 快速入口
- 最新文档：[[docs/01-项目总览]]
- 最新任务：[[tasks/DEV-OV-001]]
- 开发指南：[[docs/15-OpenViking-AIOps-开发指南]]
- 开发提示词：[[prompts/openviking-aiops-development]]
- 框架分析：[[docs/16-AIDevVault框架应用分析]]
- 任务看板：[[05-任务看板]]

## 项目状态
- AIDevault 框架（参考）：✅ 完成
- OpenViking AI 运维系统：⏳ 进行中（项目总览完成）
- 部署环境：✅ OpenViking 已部署（172.16.100.101:1933）
- 部署环境：✅ OpenViking Bot 已部署（172.16.100.101:18791）
- 推送状态：⏳ 待创建 GitHub 仓库

## 核心原则

### 研发层原则
1. **OpenClaw 负责总控与任务编排** - 任务下发、进程管理、会话协调
2. **Claude Code 负责代码修改与执行** - 代码开发、测试、调试
3. **Obsidian 负责项目知识沉淀** - 需求分析、架构设计、最佳实践记录
4. **Git / CI 负责质量门禁** - 代码审查、自动化测试、质量门禁

### 运维层原则
1. **OpenViking 不参与研发主流程** - 仅作为运维环境的上下文数据库
2. **OpenViking Bot 负责 LLM 智能运维推理** - 运维决策、故障诊断、自动修复建议
3. **运维产品在运行时与 LLM 交互** - 通过 Bot 接口进行智能运维推理
4. **运维经验沉淀在 OpenViking** - 不回流到研发层，只在运维环境内循环

### 边界原则
- OpenClaw / Claude Code 不直接访问生产运维环境（除非部署）
- OpenViking / OpenViking Bot 不参与代码开发和研发流程
- 研发与运维的数据严格分离（研发知识 vs 运维知识）
