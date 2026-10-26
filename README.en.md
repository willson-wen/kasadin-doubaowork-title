# kasadin-doubaowork-title

> Make your DoubaoWork conversation titles show what you're doing at a glance.

Give your DoubaoWork conversations consistent, scannable titles: in the sidebar you see the **subject** first, then the **core goal**. No matter how many conversations you have, you can find the right one fast. The naming approach is ported from [oil-codex-title](https://github.com/oil-oil/oil-codex-title) for Codex, adapted to DoubaoWork's Skill system, and ships with a zero-dependency deterministic validator.

English | [中文](README.md)

## Result

| Before | After |
| --- | --- |
| new chat | 🧩 Todo list app｜Fix |
| Help me compare | 🔎 Headphones A / B｜Spec comparison |
| Keep editing | 🎬 Product promo video｜Script planning |
| This week's report | 📝 Team weekly report｜2026-10-26 |
| (empty conversation) | 💬 Greeting chat｜2026-10-26 |

## Title format

Every title follows **"category emoji + subject｜goal"**:

```
category emoji + one space + subject + full-width "｜" + core goal
```

- **Subject first**: put identifying words like "todo list", "login form", or "headphones" up front; omit the outer project name by default.
- **Fixed categories**: 8 categories chosen by the lasting work product; the icon doesn't switch just because of the last action.
- **Stable names**: don't rename a title whose main line is already accurate; actions like "continue" or "push" never replace the main thread.
- **Follows your language**: name in the user's dominant language and keep product names, e.g. `🧩 Login verification｜Fix expiry`.
- **Date recurring work**: daily or weekly series are distinguished by date or issue number.
- **No forced naming**: when there's only a greeting or the conversation is truly empty, don't invent a subject.

### The 8 categories

| Emoji | Category | Fits |
| --- | --- | --- |
| 🎬 | Content production | video topics, scripts, shooting, editing, publishing |
| 🧩 | Tool development | software, code, plugins, Skills, automation tools |
| 🔎 | Comparison & research | model comparisons, analysis, research judgment |
| 🎨 | Page design | layout, visual design, style restoration |
| 📝 | Methods & docs | methodologies, guides, docs, articles, slides |
| 📅 | Scheduling | dated schedules, reminders, to-dos |
| ⚙️ | Environment setup | installation, connections, accounts, runtime |
| 💬 | General discussion | has a clear subject but none of the above |

## Installation

DoubaoWork auto-loads Skills under `workspace/.user_skills/`. Just put this repo there:

```bash
# 1. Your .user_skills directory
SKILLS_DIR="$HOME/Library/Application Support/DoubaoWork/Default/.doubaowork/agent_mode/workspace/.user_skills"

# 2. Clone into it
git clone https://github.com/willson-wen/kasadin-doubaowork-title.git "$SKILLS_DIR/kasadin-doubaowork-title"
```

Or simply tell DoubaoWork: "Install the conversation-naming Skill kasadin-doubaowork-title."

> The Skill takes effect after you open a new conversation (or start a new session).

## Usage

Just say to DoubaoWork:

- "Give this conversation a title."
- "Rename this conversation."
- "Batch organize the titles of my past conversations."
- "Preview the new titles for these conversations."

- **Single conversation**: read the content, identify the subject and goal, confirm the format with the validator, then rename through the UI and read it back.
- **Batch organizing**: DoubaoWork exposes no conversation-list API to the Agent, so provide a sidebar screenshot or authorize computer use to open them one by one; each batch reports "named / kept / failed".

## Validator

```bash
# Single title
python3 scripts/validate_title.py "🧩 Todo list app｜Fix"
# Batch (one title per line on stdin)
printf '%s\n' "Title 1" "Title 2" | python3 scripts/validate_title.py
# JSON output
python3 scripts/validate_title.py --json "📝 Team weekly report｜2026-10-26"
```

Valid titles exit with code 0 and print `OK`; invalid ones exit with code 1 and print the reason. Standard library only, compatible with Python 3.9+.

## Project structure

```
kasadin-doubaowork-title/
├── SKILL.md                    # Main DoubaoWork Skill file
├── references/
│   └── naming-guide.md         # Full naming rules (language shifts, main-line judgment, disambiguation)
└── scripts/
    └── validate_title.py       # Deterministic title validator
```

## Acknowledgements

The naming approach and title structure come from [oil-oil/oil-codex-title](https://github.com/oil-oil/oil-codex-title); this project is its adaptation and extension for DoubaoWork.

## License

[MIT](LICENSE)
