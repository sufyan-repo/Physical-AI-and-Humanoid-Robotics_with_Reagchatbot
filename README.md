# 🚀 SPECT-Kit Hackathon Project – Overview

Robust documentation for your Docusaurus + Specs + Claude Code project. Clean, structured, technical.

---

## 📌 Overview

This project is a full engineering stack combining **Docusaurus**, **Claude Code**, and **Spec-Driven Development**, designed for building structured, AI‑assisted documentation systems.

Key capabilities:

* Specification-first workflow
* Docusaurus-based docs site
* Claude Code automation
* Organized feature specs + ADRs

---

## 📁 Project Structure

```
.docusaurus/        # Docusaurus build system
build/              # Production output
book/               # Additional course/textbook assets
.claude/            # Claude Code configuration
.github/            # CI/CD
.specify/           # Specfy configs

src/
  components/       # UI components
  css/              # Styles
  hooks/            # React hooks
  pages/            # Custom routes
  theme/            # Docusaurus theme overrides
  utils/            # Utilities
  static/           # Static assets

docs/               # Documentation modules (MDX)
chatbot/            # Chatbot logic
history/            # ADRs & decisions
specs/              # Feature specifications
```

---

## 📚 Documentation System

* **Docusaurus 3.x** for modular MDX-based docs
* Custom themes + UI components
* Chatbot integrated within docs

---

## ⚙️ Tech Stack

**Frontend**

* React + TypeScript
* Docusaurus 3
* MDX

**Backend (optional extension)**

* FastAPI
* Python 3.12

**AI Tools**

* Claude Code
* Gemini API

---

## ▶️ Quick Start

### 🔧 Install Dependencies

```bash
npm install
```

### 🟦 Start Docusaurus Local Server

```bash
npm run start
```

Local URL: `http://localhost:3000`

---

## 📑 Specs Workflow

All features follow a structured spec-driven model:

1. Write spec → `specs/`
2. Implement feature
3. Add ADR → `history/`
4. Commit + PR

---

## 📌 Example Features (Sample)

| Spec | Feature                | Status    |
| ---- | ---------------------- | --------- |
| 001  | Chat UI integration    | Completed |
| 002  | RAG chatbot backend    | Completed |
| 003  | Gemini API upgrade     | Completed |
| 004  | Retrieval improvements | Completed |

---

## 🧩 Development Agents

* **frontend-ui-specialist** – React components
* **spec-engineer** – Specs + ADRs
* **docusaurus-architect** – Docs structure
* **integration-engineer** – Glue logic

---

## 🖥️ Hardware (If Using Robotics or Heavy AI)

* CPU: i7 / Ryzen 9
* GPU: RTX 4070 Ti or above
* RAM: 32–64GB

---

## 💬 Custom Commands

```
/sp.specify   → Generate feature spec
/sp.plan      → Create implementation plan
/sp.adr       → Generate ADR
```

---

## 🤝 Contributing

1. Add new spec to `specs/`
2. Implement feature
3. Document ADR in `history/`
4. Submit PR linking the spec

---

## 📄 License

MIT

## 🤖 New Feature: AI Chatbot Integration

This project now includes an AI chatbot feature with the following capabilities:

- A floating robot button that displays the `Robot.png` image from `book/static/img/`
- Clicking the button opens a chatbot modal
- Integration with the existing RAG (Retrieval-Augmented Generation) backend
- Real-time conversation with the AI assistant
- Source citations for AI responses
- Authentication support to maintain user sessions

The chatbot is available on all pages of the textbook site through a floating button on the bottom-right corner.
"# Physical-AI-and-Humanoid-Robotics"  "# Physical-AI-and-Humanoid-Robotics"
"# Physical-AI-and-Humanoid-Robotics"