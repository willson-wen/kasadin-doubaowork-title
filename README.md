# kasadin-doubaowork-title

> 让豆包工作的对话标题，一眼看出你在做什么。

给豆包工作（DoubaoWork）的对话起统一、可扫读的标题：侧边栏里先看到**对象**，再看到**核心目标**。对话再多，也能快速找回。命名理念移植自 Codex 上的 [oil-codex-title](https://github.com/oil-oil/oil-codex-title)，并针对豆包工作的 Skill 机制做了适配，附带一个零依赖的确定性校验脚本。

[English](README.en.md) | 中文

## 命名效果

| 原来的标题 | 整理后的标题 |
| --- | --- |
| new chat | 🧩 待办清单App｜修复 |
| 帮我对比一下 | 🔎 降噪耳机A / B｜参数对比 |
| 继续修改 | 🎬 产品宣传片｜脚本策划 |
| 这周的周报 | 📝 团队周报｜2026-10-26 |
| （空白对话） | 💬 问候对话｜2026-10-26 |

## 标题结构

统一采用 **「类别 emoji + 对象｜目标」**：

```
类别 emoji + 一个空格 + 对象 + 全角「｜」+ 核心目标
```

- **对象在前**：把“待办清单”“登录表单”“降噪耳机”等辨识词放到前面，默认省略外层项目名。
- **类别固定**：8 个类别，按持续工作的产物选，不会因为最后一个动作就切换图标。
- **名称稳定**：主线准确的标题不重复改名；“继续”“推送”等动作不会取代主线。
- **跟随语言**：按用户主要交流语言命名，保留产品名，如 `🧩 Login verification｜Fix expiry`。
- **周期加日期**：日报、周报等系列内容用日期或期号区分。
- **不强行命名**：只有问候或确实空白时，不臆造对象。

### 8 个类别

| emoji | 类别 | 适用 |
| --- | --- | --- |
| 🎬 | 内容制作 | 视频选题、脚本、拍摄、剪辑、发布 |
| 🧩 | 工具开发 | 软件、代码、插件、Skill、自动化工具 |
| 🔎 | 对比调研 | 模型对比、资料分析、研究判断 |
| 🎨 | 页面设计 | 页面布局、视觉设计、样式还原 |
| 📝 | 方法整理 | 方法论、指南、文档、文章、演示文稿 |
| 📅 | 日程安排 | 有明确时间的日程、提醒、待办 |
| ⚙️ | 环境配置 | 安装、连接、账号、运行环境 |
| 💬 | 一般讨论 | 有明确对象但不属以上类型 |

## 安装

豆包工作会自动加载 `workspace/.user_skills/` 下的 Skill，把本仓库放到该目录即可：

```bash
# 1. 你的 .user_skills 目录
SKILLS_DIR="$HOME/Library/Application Support/DoubaoWork/Default/.doubaowork/agent_mode/workspace/.user_skills"

# 2. 克隆到该目录
git clone https://github.com/willson-wen/kasadin-doubaowork-title.git "$SKILLS_DIR/kasadin-doubaowork-title"
```

也可以直接在豆包工作里说：“帮我安装 kasadin-doubaowork-title 这个对话命名 Skill。”

> 重新打开一个对话（或新开会话）后，Skill 即生效。

## 怎么用

直接对豆包工作说：

- “给这个对话起个标题。”
- “把这个对话重命名一下。”
- “帮我批量整理历史对话的标题。”
- “预览一下这些对话的新标题。”

- **单个对话**：通读内容、锁定对象与目标，用校验脚本确认格式，再通过界面重命名并回读确认。
- **批量整理**：豆包工作没有向 Agent 暴露对话列表接口，需要你提供侧边栏截图，或授权电脑自动化（computer use）逐个打开；每批会汇报「已命名 / 保留 / 失败」。

## 校验脚本

```bash
# 单条
python3 scripts/validate_title.py "🧩 待办清单App｜修复"
# 批量（stdin 每行一个）
printf '%s\n' "标题1" "标题2" | python3 scripts/validate_title.py
# JSON 结果
python3 scripts/validate_title.py --json "📝 团队周报｜2026-10-26"
```

合法返回退出码 0 并打印 `OK`，非法返回退出码 1 并给出原因。纯标准库实现，兼容 Python 3.9+。

## 项目结构

```
kasadin-doubaowork-title/
├── SKILL.md                    # 豆包工作 Skill 主文件
├── references/
│   └── naming-guide.md         # 完整命名规则（语言迁移、主线判断、消歧等）
└── scripts/
    └── validate_title.py       # 确定性标题校验脚本
```

## 致谢

命名理念与标题结构来自 [oil-oil/oil-codex-title](https://github.com/oil-oil/oil-codex-title)，本项目是其在豆包工作上的适配与扩展。

## 许可证

[MIT](LICENSE)
