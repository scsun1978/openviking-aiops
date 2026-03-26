# OpenViking AI 运维系统

> 基于边缘计算设备的智能化运维系统，实现网络监控、设备健康度监控、AI 智能运维等功能

## 🎯 项目简介

OpenViking AI 运维系统是一个基于边缘计算设备的智能化运维系统，结合 OpenViking（上下文数据库）和 VikingBot（AI 智能体），实现网络监控、设备健康度监控、AI 智能运维等功能，为整个网络提供智能化运维能力。

### 核心特性

- **边缘计算**：AI 能力部署到边缘计算设备中
- **网络运维**：覆盖整个网络的运维管理
- **AI 辅助**：使用 AI 技术实现智能化运维
- **实时监控**：实时监控网络状态和设备健康度
- **智能告警**：基于规则和 AI 的智能告警系统

## 🏗️ 双层架构

### 研发层（开发与管理）

```
OpenClaw（总控与任务编排）
    ↓
Claude Code（代码修改与执行）
    ↓
Obsidian（项目知识沉淀）
    ↓
Git / CI（质量门禁）
    ↓
部署交付
```

### 运维层（生产环境）

```
OpenViking（上下文管理 / AGFS）
    ↓
OpenViking Bot（LLM 智能运维推理）
    ↓
边缘设备群（网络监控 / 自动运维）
```

## 📊 项目状态

- **当前阶段**：M2（需求与架构设计）已完成
- **下一个里程碑**：M3（核心功能开发）
- **GitHub 仓库**：https://github.com/scsun1978/openviking-aiops

## 🚀 快速开始

### 前置条件

- **Python 3.10+**
- **Docker** 和 **Docker Compose**
- **OpenViking**（已部署在 172.16.100.101:1933）
- **VikingBot**（已部署在 172.16.100.101:18791）
- **Prometheus**、**Grafana**、**AlertManager**（已部署）

### 克隆仓库

```bash
git clone git@github.com:scsun1978/openviking-aiops.git
cd openviking-aiops
```

### 开发环境配置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入相关配置
```

### 启动开发环境

```bash
# 启动所有服务（Docker Compose）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 访问服务

- **Prometheus**：http://172.16.100.101:9090
- **Grafana**：http://172.16.100.101:3000（admin/admin）
- **AlertManager**：http://172.16.100.101:9093
- **OpenViking**：http://172.16.100.101:1933
- **VikingBot**：http://172.16.100.101:18791

## 📁 项目结构

```
OpenViking-AIOps/
├── docs/                      # 项目文档
│   ├── 01-项目总览.md
│   ├── 02-研发架构.md
│   ├── 03-运维架构.md
│   ├── 04-开发工作流.md
│   ├── 15-开发指南.md
│   ├── 16-AIDevault框架应用分析.md
│   └── 20-34（阶段报告）
├── tasks/                     # 任务文件
│   ├── DEV-OV-001.md（已完成）
│   ├── DEV-OV-002.md（已完成）
│   ├── DEV-OV-003.md（已完成）
│   └── DEV-OV-005.md（进行中）
├── src/                       # 源代码
│   ├── network-monitoring/    # 网络监控模块
│   ├── edge-computing/        # 边缘计算模块
│   ├── ai-models/             # AI 模型模块
│   ├── monitoring/            # 监控配置
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   └── loki/
│   └── deployment/            # 部署脚本
├── scripts/                   # 脚本工具
│   ├── deploy/
│   ├── monitor/
│   └── train/
├── templates/                 # 任务模板
├── prompts/                   # 提示词
└── README.md                  # 项目说明
```

## 🎯 开发指南

### 开发流程

1. **任务创建**：在 Obsidian 中创建任务文件（如 `tasks/DEV-OV-005.md`）
2. **任务下发**：通过 OpenClaw 下发任务到 Claude Code
3. **代码执行**：Claude Code 执行开发任务
4. **测试验证**：在边缘设备上测试
5. **文档更新**：更新 Obsidian 知识库
6. **代码提交**：推送到 Git / CI

### 开发规范

- **代码规范**：遵循 PEP 8 规范
- **测试要求**：代码覆盖率 > 80%
- **文档要求**：所有函数都有文档字符串
- **Git 提交**：使用规范化的提交信息（Conventional Commits）

## 📊 项目里程碑

### ✅ M1：研发框架建立（已完成）
- 完成 OpenViking 项目现状分析
- 完成 AIDevault 框架应用分析
- 明确双层架构设计
- 创建项目文档骨架

### ✅ M2：需求与架构设计（已完成）
- 完成需求分析（DEV-OV-002）
- 完成架构设计（DEV-OV-003）
- 完成技术栈选型
- 完成核心模块设计

### ⏳ M3：核心功能开发（进行中）
- 网络运维模块开发（DEV-OV-005）
- 监控告警模块开发（DEV-OV-006）
- 集成和部署（DEV-OV-007）

### ⏳ M4：测试与优化（计划中）
- 本地测试
- 边缘设备测试
- 性能优化
- 安全加固

### ⏳ M5：部署与监控（计划中）
- 部署到生产边缘设备
- 配置监控和告警
- 运维知识库初始化
- 智能运维验证

## 🛠️ 技术栈

### 研发技术栈
- **总控与编排**：OpenClaw
- **代码执行**：Claude Code（ACP Session）
- **知识沉淀**：Obsidian
- **质量保障**：Git / GitHub Actions

### 运维技术栈
- **上下文管理**：OpenViking（AGFS 文件系统 + 向量数据库）
- **LLM 推理**：火山引擎豆包 Pro 260215
- **监控告警**：Prometheus / Grafana / AlertManager
- **边缘计算**：Docker / Docker Compose
- **智能运维**：OpenViking Bot

### 开发技术栈
- **编程语言**：Python 3.10+
- **Web 框架**：FastAPI / Flask
- **监控客户端**：prometheus_client
- **系统监控**：psutil
- **容器化**：Docker / Docker Compose

## 📖 相关文档

### 项目核心文档
- [[docs/01-项目总览]] - 项目总览、双层架构、核心原则
- [[docs/02-研发架构]] - 研发层详细架构设计
- [[docs/03-运维架构]] - 运维层详细架构设计
- [[docs/04-开发工作流]] - 研发工作流设计

### 开发指南
- [[docs/15-OpenViking-AIOps-开发指南]] - 完整开发指南
- [[docs/16-AIDevault框架应用分析]] - AIDevault 框架应用分析

### 架构设计
- [[docs/30-架构设计]] - 完整的架构设计文档
- [[docs/31-DEV-OV-003-阶段3核心模块架构设计报告]] - 核心模块架构设计
- [[docs/32-DEV-OV-003-阶段4接口定义和数据模型设计报告]] - 接口定义和数据模型设计

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue
1. 使用规范的 Issue 模板
2. 详细描述问题和期望
3. 提供复现步骤和环境信息

### 提交 Pull Request
1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/your-feature`）
3. 提交代码（`git commit -m 'Add some feature'`）
4. 推送到分支（`git push origin feature/your-feature`）
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 👥 作者

- **scsun** - 项目负责人

## 🔗 相关链接

- **OpenViking 项目**：https://github.com/scsun1978/openviking
- **AIDevault 框架**：https://github.com/scsun1978/aidevault
- **OpenClaw 文档**：https://docs.openclaw.ai
- **Claude Code 文档**：https://code.claude.com/docs

---

**最后更新**：2026-03-26
**版本**：v1.0
