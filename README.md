# APIBridge: Generate AI Agent Tools from Swagger/OpenAPI Specs

**Subtitle:** Transform REST APIs into AI-Ready Tools in Seconds—No Manual Integration Code Required

---

## 📖 Introduction | Overview

### Problem Statement
Modern AI applications need seamless access to REST APIs, but developers currently must write custom integration code for each API. This is:
- **Time-consuming**: Hours of boilerplate code per API
- **Error-prone**: Manual specifications lead to bugs and inconsistencies
- **Hard to maintain**: API changes require manual code updates
- **Not scalable**: Adding new APIs becomes exponentially complex

### What You'll Learn
By the end of this guide, you'll understand:
- How to convert any Swagger/OpenAPI specification into Python tool code
- How to create dynamic ADK agents with auto-generated tools
- How to build a master agent that orchestrates multiple APIs
- How to deploy this on Google Cloud Run for production use

### Target Audience
- **Backend engineers** building AI applications
- **DevOps teams** managing API integrations
- **FinTech/Banking developers** bridging APIs and AI (like NatWest's Model Context Protocol use case)
- **Hackathon participants** in cloud-native AI development
- **Enterprise architects** standardizing AI-API interactions

### Expected Outcome
By the end of this tutorial, you'll have:
- ✅ A fully functional tool generator from any Swagger spec
- ✅ A working ADK agent with dynamically generated tools
- ✅ Generated Python code for all API endpoints
- ✅ A master agent coordinating multiple APIs
- ✅ Deployment-ready Docker setup for Cloud Run
- ✅ A blog post explaining the architecture

---

## 🏗️ Design

### Architecture Overview

Swagger/OpenAPI Specification (JSON)
↓
SwaggerToolGenerator
├─ Parses endpoints
├─ Extracts parameters
├─ Generates Python code
└─ Creates tool definitions
↓
DynamicToolAgent (ADK-powered)
├─ Compiles generated tools
├─ Registers with LLM (Gemini)
├─ Manages tool execution
└─ Handles errors
↓
MasterAgent (Orchestrator)
├─ Routes queries to sub-agents
├─ Coordinates multi-API workflows
└─ Provides unified interface
↓
Cloud Run / Vertex AI Deployment


### Why This Design?

**Scalability:** Generate tools for 100+ endpoints without manual code
**Flexibility:** Works with any Swagger/OpenAPI spec
**Security:** Isolated tool execution with error handling
**Production-ready:** Built for enterprise deployment on GCP
**LLM-agnostic:** Tool definitions compatible with any ADK model

### Design Rationale

This design solves the **Model Context Protocol (MCP) challenge** identified by NatWest: AI agents need standardized access to business tools and data. Instead of manual API adapters, ToolForge auto-generates them from API specifications.

**Impact on Usability:**
- Developers reduce integration time from hours to minutes
- No custom code maintenance required
- API changes auto-propagate

**Impact on Functionality:**
- Agents can instantly access any REST API
- Multi-API orchestration is seamless
- Error handling is built-in

---

## 📋 Prerequisites

### Software & Tools

| Tool | Version | Purpose | Download |
|------|---------|---------|----------|
| Python | 3.10+ | Runtime environment | [python.org](https://www.python.org/downloads/) |
| Google Cloud SDK | Latest | Cloud deployment | [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install) |
| Docker | 24.0+ | Containerization | [docker.com](https://docs.docker.com/get-docker/) |
| Git | Latest | Version control | [git-scm.com](https://git-scm.com/) |
| VS Code | Latest | Code editor (optional) | [code.visualstudio.com](https://code.visualstudio.com/) |

### Required Python Libraries

google-adk>=0.1.0 # Google Agents Development Kit
google-generativeai>=0.3.0 # Gemini API access
google-cloud-aiplatform # Vertex AI integration
requests>=2.31.0 # HTTP requests
pydantic>=2.0.0 # Data validation
jsonschema>=4.20.0 # JSON Schema validation


### Prior Concepts/Knowledge

- **REST APIs**: Understand HTTP methods (GET, POST, PUT, DELETE)
- **JSON**: Familiarity with JSON structure and parsing
- **Python**: Basic Python classes, functions, decorators
- **Swagger/OpenAPI**: Understanding of API specifications (brief intro provided)
- **Google Cloud**: Basic GCP project setup knowledge

### System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for dependencies and generated files
- **Network**: Internet access for Google Cloud services
- **OS**: Linux, macOS, or Windows (with WSL)

---

## 🔧 Step-by-Step Instructions

### Step 1: Clone & Setup Project

- Clone the repository

```
git clone https://github.com/yourusername/toolforge.git
cd toolforge
```
- Create virtual environment
```
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

- Install dependencies
```
pip install -r requirements.txt
```


**What's happening:**
- Virtual environment isolates project dependencies
- `requirements.txt` contains all necessary packages

### Step 2: Prepare Your Swagger Specification

Place your Swagger/OpenAPI JSON file in `specifications/NatWest.json`:


