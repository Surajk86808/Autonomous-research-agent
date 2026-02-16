# 🤖 AI-Powered Multi-Agent Research Assistant

> A scalable, production-ready research agent that breaks down complex questions into parallel research tasks, leverages vector memory, and synthesizes comprehensive answers using LangGraph and multiple LLMs.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Usage](#api-usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## 🎯 Overview

This project demonstrates a **sophisticated AI agent system** that mimics how human researchers approach complex questions. Instead of giving surface-level answers, it:

1. **Plans** - Breaks questions into focused sub-questions
2. **Researches** - Executes parallel web searches or retrieves from memory
3. **Synthesizes** - Combines findings into comprehensive answers

**Perfect for:** Job market analysis, technology trends, competitive research, or any multi-faceted question requiring deep investigation.

---

## ✨ Key Features

### 🧠 **Intelligent Question Decomposition**
- Automatically breaks complex queries into 3-5 focused research tasks
- Uses Gemini 2.0 Flash for fast, intelligent planning
- Generates diverse perspectives (technical, economic, social impact)

### ⚡ **Parallel Processing**
- Research tasks execute **simultaneously** using LangGraph's `Send` API
- Dramatically reduces response time vs sequential processing
- Scales efficiently with question complexity

### 💾 **Vector Memory System**
- Stores research findings in Qdrant vector database
- Retrieves relevant past knowledge before new web searches
- Uses `all-MiniLM-L6-v2` embeddings for semantic similarity
- **Persistent storage** - memory survives restarts

### 🌐 **Multi-Source Research**
- Integrates Tavily API for advanced web search
- Fallback mechanisms ensure reliability
- Limits results to prevent information overload

### 🔄 **LLM Routing**
- **Gemini 2.0 Flash** - Planning & quick responses
- **Groq (Llama 3.1)** - High-speed research synthesis
- Automatic fallback if any LLM fails

### 🚀 **Production-Ready API**
- FastAPI backend with async support
- Simple GET endpoints for easy integration
- Structured state management via TypedDict

---

## 🏗️ Architecture

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  PLANNER │ (Gemini 2.0)
    └────┬─────┘
         │
         │ Generates 3-5 sub-questions
         │
    ┌────▼──────────────────┐
    │  PARALLEL RESEARCH   │
    │  ┌───┐ ┌───┐ ┌───┐  │
    │  │ R │ │ R │ │ R │  │ (Groq/Gemini)
    │  └─┬─┘ └─┬─┘ └─┬─┘  │
    └────┼─────┼─────┼─────┘
         │     │     │
    Check Memory → Web Search → Store Results
         │     │     │
    ┌────▼─────▼─────▼─────┐
    │    SYNTHESIZER       │
    │  (Combines Findings) │
    └──────────────────────┘
```

**Flow:**
1. **Planner Node** → Decomposes question
2. **Conditional Routing** → Sends tasks to parallel research
3. **Research Nodes** → Check vector DB → Web search → Store memory
4. **Synthesizer Node** → Aggregates all findings
5. **Return** → Comprehensive answer

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Framework** | LangGraph | Multi-agent orchestration |
| **API** | FastAPI | REST endpoints |
| **LLMs** | Gemini 2.0, Groq (Llama 3.1) | Question processing |
| **Search** | Tavily API | Advanced web search |
| **Vector DB** | Qdrant | Semantic memory storage |
| **Embeddings** | SentenceTransformers | Text-to-vector conversion |
| **Environment** | Python-dotenv | Secure config management |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- API Keys:
  - [Google Gemini API](https://ai.google.dev/)
  - [Tavily API](https://tavily.com/)
  - [Groq API](https://console.groq.com/) (optional, auto-fallback)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-research-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .envTemplate.txt .env
```

### Configuration

Edit `.env` with your API keys:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here  # Optional
```

### Run the Application

```bash
# Start FastAPI server
uvicorn app.main:app --reload

# Server runs on http://localhost:8000
```

### Test the Graph

```bash
# Run standalone test
python test_graph.py
```

---

## 📡 API Usage

### Health Check

```bash
GET http://localhost:8000/
```

**Response:**
```json
{
  "status": "Agent Running"
}
```

### Ask a Question

```bash
GET http://localhost:8000/ask?question=Will AI replace software engineers?
```

**Response:**
```json
{
  "question": "Will AI replace software engineers?",
  "tasks": [
    "What are current AI capabilities in software development?",
    "How is AI impacting software engineering jobs?",
    ...
  ],
  "findings": [
    "Research finding 1...",
    "Research finding 2...",
    ...
  ],
  "final_answer": "Synthesized comprehensive answer..."
}
```

### Example cURL

```bash
curl -X GET "http://localhost:8000/ask?question=What%20are%20the%20latest%20trends%20in%20quantum%20computing?"
```

---

## 📁 Project Structure

```
ai-research-agent/
│
├── app/
│   ├── graph/
│   │   ├── build_graph.py      # LangGraph workflow definition
│   │   └── state.py            # Shared state schema
│   │
│   ├── llm/
│   │   └── router.py           # LLM selection logic
│   │
│   ├── memory/
│   │   └── vector_db.py        # Qdrant vector operations
│   │
│   ├── tools/
│   │   └── web_search.py       # Tavily web search integration
│   │
│   └── main.py                 # FastAPI application
│
├── qdrant_data/                # Vector DB persistence (auto-created)
├── test_graph.py               # Standalone testing script
├── .env                        # API keys (DO NOT COMMIT)
├── .envTemplate.txt            # Template for .env
├── .gitignore                  # Excludes secrets & cache
└── README.md                   # You are here!
```

---

## 🔍 How It Works

### 1. **Question Planning** (`planner_node`)

When you ask: *"Will AI replace software engineers?"*

The planner generates:
- "What are current AI coding capabilities?"
- "What tasks can AI not handle yet?"
- "How is the job market responding?"
- "What do industry experts predict?"

**Why?** Single broad question → Multiple focused angles = better research

---

### 2. **Parallel Research** (`research_node`)

Each sub-question triggers:

```python
# Check memory first (fast)
past_knowledge = get_memories(task, limit=2)

if past_knowledge:
    # Use cached research
else:
    # New web search via Tavily
    web_data = search_web(task)
    # Store for future use
    store_memory(result)
```

**Benefit:** Avoids redundant API calls, builds knowledge over time

---

### 3. **Vector Memory** (`vector_db.py`)

- Converts text → 384-dim embeddings
- Stores in Qdrant with UUID
- Retrieves via cosine similarity
- **Persistent** across server restarts

**Example:**
```
Query: "AI in healthcare"
Retrieves: Past research on medical AI, diagnostic tools, etc.
```

---

### 4. **Synthesis** (`synthesizer_node`)

Aggregates all findings using the `Annotated[List[str], operator.add]` pattern:

```python
findings: Annotated[List[str], operator.add]
```

This automatically merges results from parallel nodes.

---

## ⚙️ Configuration

### LLM Models

Edit `app/llm/router.py` to change models:

```python
# Gemini
model="gemini-2.0-flash"  # Fast & cost-effective

# Groq
model="llama-3.1-8b-instant"  # Speed-optimized
```

### Search Depth

Modify `app/tools/web_search.py`:

```python
search_depth="advanced"  # Options: basic, advanced
max_results=3            # Increase for more sources
```

### Memory Settings

Adjust `app/memory/vector_db.py`:

```python
limit=3  # Number of memories to retrieve
size=384  # Must match embedding model dimensions
```

---

## 🎯 Skills Demonstrated (For Recruiters)

This project showcases:

✅ **Multi-Agent Systems** - LangGraph orchestration  
✅ **Parallel Processing** - Async task distribution  
✅ **Vector Databases** - Qdrant for semantic search  
✅ **API Integration** - Multiple LLM providers, web search  
✅ **State Management** - TypedDict, annotations  
✅ **Production Patterns** - Error handling, retries, fallbacks  
✅ **RESTful APIs** - FastAPI backend  
✅ **Environment Security** - dotenv, .gitignore best practices  
✅ **Code Organization** - Modular, scalable architecture  

---

## 🚧 Future Enhancements

- [ ] **Streaming Responses** - Real-time findings as they arrive
- [ ] **Advanced Synthesis** - Use LLM to create final summary
- [ ] **User Sessions** - Personalized memory per user
- [ ] **Fact Verification** - Cross-reference sources
- [ ] **Export Reports** - PDF/Markdown output
- [ ] **Web UI** - React/Streamlit frontend
- [ ] **Caching Layer** - Redis for frequent queries
- [ ] **Monitoring** - Logging, metrics, tracing

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Questions?** Open an issue or reach out:

- Email: your.email@example.com
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Portfolio: [yourwebsite.com](https://yourwebsite.com)

---

## 🙏 Acknowledgments

- **LangGraph** - For making multi-agent workflows simple
- **Google Gemini** - Lightning-fast LLM inference
- **Tavily** - Best-in-class web search API
- **Qdrant** - Efficient vector database
- **Groq** - Blazing fast LLM infrastructure

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Built with ❤️ using LangGraph & FastAPI

</div>
