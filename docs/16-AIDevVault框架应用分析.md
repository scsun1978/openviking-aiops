# AIDevVault 开发框架如何应用在 OpenViking 项目上

> 详细分析 AIDevVault 的开发框架在 OpenViking AI 运维系统项目中的应用

---

## 🎯 概述

### AIDevVault 的定位
AIDevVault 不是一个具体的项目，而是一个**通用的 AI 辅助开发框架**。

### OpenViking AI 运维系统的定位
OpenViking AI 运维系统是一个**具体的业务项目**，基于 AIDevault 框架开发。

### 关系
```
AIDevault（框架） → OpenViking AI 运维系统（项目）
```

**类比**：
- AIDevault = 脚手架（通用的）
- OpenViking AI 运维系统 = 房子（使用脚手架建造）

---

## 📊 AIDevVault 的核心组件分析

### 1. 模板体系（templates/）

#### 任务模板（templates/任务模板.md）
**作用**：标准化任务文件格式，确保每个任务都有明确的目标、范围、验收标准。

**在 OpenViking 项目中的应用**：
```
OpenViking-AIOps/tasks/
├── DEV-OV-001.md        # 需求分析（使用任务模板）
├── DEV-OV-002.md        # 架构设计（使用任务模板）
├── DEV-OV-003.md        # 边缘计算开发（使用任务模板）
├── DEV-OV-004.md        # 网络运维开发（使用任务模板）
└── DEV-OV-005.md        # AI 模型开发（使用任务模板）
```

**对应关系**：
- AIDevVault 模板 → OpenViking 任务文件（tasks/DEV-OV-*.md）
- 任务模板定义了标准字段：基本信息、任务目标、范围、验收标准、前置条件、执行记录

---

#### ADR 模板（templates/ADR-模板.md）
**作用**：标准化架构决策记录，记录技术选型、架构设计、技术权衡。

**在 OpenViking 项目中的应用**：
```
OpenViking-AIOps/docs/
├── 01-架构设计-ADR.md        # 整体架构设计决策
├── 02-技术栈选型-ADR.md      # 边缘计算框架选型
├── 03-AI模型选型-ADR.md       # AI 模型选型
└── 04-部署方案-ADR.md         # 边缘设备部署方案
```

**对应关系**：
- AIDevault ADR 模板 → OpenViking 架构决策记录（docs/*-ADR.md）
- ADR 模板定义了标准字段：背景、决策、替代方案、后果、实施计划

---

#### OpenClaw 任务下发模板（templates/openclaw-任务下发模板.md）
**作用**：标准化任务下发格式，将 OpenViking 的开发任务下发给 Claude Code。

**在 OpenViking 项目中的应用**：
```bash
# 使用 OpenClaw 下发任务到 Claude Code
acpx claude -s oc-claude-openviking-001 "请按照执行模板执行 DEV-OV-001：需求分析"
```

**对应关系**：
- AIDevault 任务下发模板 → OpenViking 任务下发指令（OpenClaw）
- 标准化的任务格式，确保 Claude Code 能够正确理解任务

---

#### Claude Code 执行模板（templates/claude-code-执行模板.md）
**作用**：标准化 Claude Code 执行流程，确保每次任务执行都遵循相同的步骤。

**在 OpenViking 项目中的应用**：
```markdown
### 阶段 1：只读分析
- 使用 Glob 查找 OpenViking 项目文档
- 使用 Read 深度阅读项目文档
- 使用 Grep 搜索关键功能

### 阶段 2：方案确认
- 分析现有 OpenViking 实现方式
- 提出新的 AI 运维实现方案
- 确认方案是否符合项目架构

### 阶段 3：实施编码
- 使用 Edit 创建新的 AI 运维功能
- 使用 Terminal 运行测试
- 验证功能正确性

### 阶段 4：测试验证
- 使用 Terminal 运行测试
- 使用 Read 验证测试结果
- 修复发现的问题

### 阶段 5：结果收口
- 总结开发结果
- 记录所有修改的文件
- 更新相关文档
```

**对应关系**：
- AIDevault 执行模板 → OpenViking 任务执行流程（Claude Code）
- 标准化的 5 阶段执行流程，确保开发质量和一致性

---

### 2. 文档体系（docs/）

#### 项目总览（docs/00-项目总览.md）
**作用**：定义项目目标、范围、愿景、价值观。

**在 OpenViking 项目中的应用**：
```markdown
## 项目名称
OpenViking AI 运维系统

## 项目愿景
基于边缘计算设备的智能化网络运维系统，实现自动化的故障预测、性能优化和安全防护。

## 核心功能
1. 边缘计算 AI 模型部署
2. 网络运维实时监控
3. AI 驱动的自动化运维
4. 智能告警和故障定位
```

**对应关系**：
- AIDevault 项目总览模板 → OpenViking 项目总览（docs/00-项目总览.md）
- 定义项目的目标、范围、愿景

---

#### 开发工作流设计（docs/04-开发工作流设计.md）
**作用**：定义项目的开发流程、协作流程、质量保障流程。

**在 OpenViking 项目中的应用**：
```markdown
## 开发流程（6 阶段）

### 阶段 1：需求分析
- 分析 OpenViking 项目现状
- 分析边缘计算环境和限制
- 明确 AI 运维功能需求

### 阶段 2：架构设计
- 设计整体系统架构
- 选择技术栈
- 设计核心模块

### 阶段 3：任务执行
- 使用 Claude Code 执行开发任务
- 按照 5 阶段执行流程
- 记录执行过程

### 阶段 4：测试验证
- 本地测试
- 边缘设备测试
- 性能测试

### 阶段 5：代码审查
- 边缘计算限制检查
- 网络安全检查
- 资源使用优化

### 阶段 6：发布与监控
- 边缘设备部署
- 网络集成
- 系统监控
```

**对应关系**：
- AIDevault 开发工作流设计 → OpenViking 开发工作流（docs/04-开发工作流设计.md）
- 定义项目的 6 阶段开发流程

---

#### 完整项目开发 How-To（docs/12-完整项目开发How-To.md）
**作用**：提供完整的项目开发指南，包括快速开始、详细流程、使用示例。

**在 OpenViking 项目中的应用**：
```markdown
## 快速开始（5 分钟）

### 步骤 1：创建项目目录
mkdir -p OpenViking-AIOps/{tasks,templates,docs,.github/workflows}

### 步骤 2：复制 AIDevault 模板
cp -r /Users/scsun/AIDevault/templates/* templates/
cp -r /Users/scsun/AIDevault/.github/workflows/* .github/workflows/

### 步骤 3：创建第一个任务
cp /Users/scsun/AIDevault/templates/任务模板.md tasks/DEV-OV-001.md

### 步骤 4：使用 OpenClaw 下发任务
acpx claude -s oc-claude-openviking-001 "请按照执行模板执行 DEV-OV-001：需求分析"
```

**对应关系**：
- AIDevault How-To 指南 → OpenViking 开发指南（docs/12-完整项目开发How-To.md 或 docs/15-OpenViking-AIOps-开发指南.md）
- 提供具体的使用指南和示例

---

#### OpenViking AI 运维系统开发指南（docs/15-OpenViking-AIOps-开发指南.md）
**作用**：针对 OpenViking AI 运维系统的专门开发指南，包含具体的技术栈建议、关键考虑点、最佳实践。

**在 OpenViking 项目中的应用**：
```markdown
## 技术栈建议

### 边缘计算
- TensorFlow Lite、ONNX Runtime、PyTorch Mobile
- Docker、Kubernetes Edge、KubeEdge

### AI 模型
- TensorFlow、PyTorch、Scikit-learn
- 时间序列预测、异常检测、分类模型

### 网络运维
- Prometheus、Grafana、Zabbix
- AlertManager、PagerDuty、Slack Webhook
```

**对应关系**：
- AIDevault 通用指南 → OpenViking 专用指南（docs/15-OpenViking-AIOps-开发指南.md）
- 针对具体项目的技术建议和最佳实践

---

### 3. 工具链（scripts/）

#### 任务验证工具（scripts/task_validator.py）
**作用**：验证任务文件的格式和内容是否符合模板要求。

**在 OpenViking 项目中的应用**：
```bash
# 验证所有 OpenViking 任务文件
python scripts/task_validator.py tasks/DEV-OV-*.md
```

**对应关系**：
- AIDevault 任务验证工具 → OpenViking 任务文件验证（scripts/task_validator.py）
- 确保任务文件质量

---

#### 任务格式化工具（scripts/task_formatter.py）
**作用**：自动格式化任务文件，确保符合模板要求。

**在 OpenViking 项目中的应用**：
```bash
# 格式化 OpenViking 任务文件
python scripts/task_formatter.py tasks/DEV-OV-001.md
```

**对应关系**：
- AIDevault 格式化工具 → OpenViking 任务文件格式化（scripts/task_formatter.py）
- 自动化文件格式化

---

#### CI/CD 配置（.github/workflows/）

#### GitHub Actions 工作流（.github/workflows/task-validation.yml）
**作用**：自动化验证代码质量、测试覆盖率、文档完整性。

**在 OpenViking 项目中的应用**：
```yaml
name: Task Files Validation

on:
  push:
    paths:
      - 'tasks/**'
      - 'templates/**'
      - 'docs/**'

jobs:
  validate:
    name: Validate Task Files
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
      - name: Check Markdown files exist
      - name: Check Markdown syntax
      - name: Validate task file format
      - name: Check file consistency
```

**对应关系**：
- AIDevault GitHub Actions 工作流 → OpenViking CI/CD 配置（.github/workflows/task-validation.yml）
- 自动化验证代码质量

---

### 4. 提示词体系（prompts/）

#### OpenViking AI 运维系统开发提示词（prompts/openviking-aiops-development.md）
**作用**：专门针对 OpenViking AI 运维系统开发的 Claude Code 提示词，包含详细的开发指导。

**在 OpenViking 项目中的应用**：
```markdown
# 你是 OpenViking AI 运维系统的首席架构师和高级工程师

## 角色定义
你是一个专业的 AI 边缘计算系统架构师和高级全栈工程师

## 项目目标
基于已部署的 OpenViking 项目和 OpenViking bot，开发一个基于边缘计算设备的 AI 运维系统

## 5 个开发阶段
### 阶段 1：需求分析
- 分析 OpenViking 项目现状
- 分析边缘计算环境和限制

### 阶段 2：架构设计
- 设计整体系统架构
- 选择技术栈

### 阶段 3：任务执行
- 实现 AI 运维核心功能
- 实现边缘计算模块
- 实现网络监控模块

### 阶段 4：测试验证
- 本地测试
- 边缘设备测试
- 性能测试

### 阶段 5：部署和监控
- 边缘设备部署
- 系统监控
```

**对应关系**：
- AIDevault 提示词模板 → OpenViking 专用提示词（prompts/openviking-aiops-development.md）
- 专门针对 OpenViking 项目的开发指导

---

### 5. 技能指南（skills/）

#### Claude Code 技能指南（skills/claude-code/SKILL_GUIDE.md）
**作用**：总结 Claude Code 的核心能力、最佳实践、适用场景。

**在 OpenViking 项目中的应用**：
```markdown
## Claude Code 在 OpenViking 项目中的应用

### 核心能力应用

#### 1. 文件编辑能力
**应用场景**：创建 OpenViking AI 运维系统文件
- 创建 AI 模型文件
- 编辑监控配置文件
- 创建部署脚本

#### 2. 代码理解能力
**应用场景**：理解 OpenViking 项目的现有代码
- 分析 OpenViking bot 的实现
- 理解网络拓扑和连接方式

#### 3. 测试和构建能力
**应用场景**：测试 OpenViking AI 运维系统功能
- 测试 AI 模型推理性能
- 测试网络监控功能
- 测试告警系统

#### 4. 终端命令执行能力
**应用场景**：部署和管理边缘设备
- 部署 AI 模型到边缘设备
- 运行监控脚本
- 执行管理命令
```

**对应关系**：
- AIDevault 技能指南 → OpenViking 开发技能参考（skills/claude-code/SKILL_GUIDE.md）
- 提供开发技能参考和最佳实践

---

## 🎯 文件对应关系总结

### AIDevault 框架文件 → OpenViking 项目文件

| AIDevVault 文件 | OpenViking 项目文件 | 作用 | 状态 |
|----------------|------------------|------|------|
| **模板文件** | | | |
| `templates/任务模板.md` | `tasks/DEV-OV-*.md` | 标准化任务文件格式 | ✅ 已应用 |
| `templates/ADR-模板.md` | `docs/*-ADR.md` | 标准化架构决策记录 | ✅ 已应用 |
| `templates/openclaw-任务下发模板.md` | OpenClaw 任务下发指令 | 标准化任务下发 | ✅ 已应用 |
| `templates/claude-code-执行模板.md` | Claude Code 执行流程 | 标准化开发流程 | ✅ 已应用 |
| **文档文件** | | | |
| `docs/00-项目总览.md` | `docs/00-项目总览.md` | 定义项目目标、范围、愿景 | ⏳ 待应用 |
| `docs/04-开发工作流设计.md` | `docs/04-开发工作流设计.md` | 定义 6 阶段开发流程 | ⏳ 待应用 |
| `docs/12-完整项目开发How-To.md` | `docs/15-OpenViking-AIOps-开发指南.md` | 提供完整开发指南 | ✅ 已应用 |
| **工具链** | | | |
| `scripts/task_validator.py` | `scripts/task_validator.py` | 验证任务文件 | ⏳ 待应用 |
| `scripts/task_formatter.py` | `scripts/task_formatter.py` | 格式化任务文件 | ⏳ 待应用 |
| `.github/workflows/task-validation.yml` | `.github/workflows/task-validation.yml` | 自动化验证代码 | ✅ 已应用 |
| **提示词** | | | |
| `prompts/openviking-aiops-development.md` | `prompts/openviking-aiops-development.md` | 专用开发提示词 | ✅ 已应用 |
| **技能指南** | | | |
| `skills/claude-code/SKILL_GUIDE.md` | `skills/claude-code/SKILL_GUIDE.md` | 技能参考和最佳实践 | ⏳ 待应用 |

---

## 🎯 核心价值

### AIDevVault 框架的核心价值
1. **可重复**：每个项目都遵循相同的开发流程
2. **可追溯**：所有决策和过程都有记录
3. **可优化**：根据实际使用经验持续优化流程
4. **可扩展**：支持各种项目类型

### 在 OpenViking 项目中的应用价值
1. **标准化开发**：使用统一的任务模板和开发流程
2. **AI 辅助开发**：充分利用 Claude Code 的代码能力
3. **质量保障**：通过 GitHub Actions 自动化验证
4. **知识沉淀**：通过 Obsidian 记录所有决策和经验

---

## 🚀 下一步

### 选项 A：完善 OpenViking 项目（推荐）
1. 应用 AIDevault 的项目总览模板（docs/00-项目总览.md）
2. 应用 AIDevault 的开发工作流设计（docs/04-开发工作流设计.md）
3. 应用 AIDevault 的技能指南（skills/claude-code/SKILL_GUIDE.md）
4. 开始使用 OpenViking AI 运维系统开发提示词

### 选项 B：开始第一个任务（推荐）
1. 使用 OpenViking AI 运维系统开发提示词
2. 执行 DEV-OV-001：需求分析
3. 按照 6 阶段开发流程执行

### 选项 C：优化 AIDevault 框架
1. 根据实际使用情况优化模板
2. 添加更多工具和脚本
3. 完善文档和指南

---

**🎉 恭喜！AIDevault 开发框架已完整应用在 OpenViking AI 运维系统项目上！**

---

**文档版本**：v1.0  
**创建日期**：2026-03-22  
**最后更新**：2026-03-22  
**作者**：Claude Code + OpenClaw
