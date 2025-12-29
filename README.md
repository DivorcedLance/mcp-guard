# 🛡️ MCP-Guard: Secure RAG Architecture

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-4285F4?style=flat&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Pinecone](https://img.shields.io/badge/Vector%20DB-Pinecone-beta?style=flat&color=FF5300)](https://www.pinecone.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

> **A Secure Retrieval-Augmented Generation (RAG) System featuring a pre-emptive security layer based on Model Context Protocol (MCP) principles to mitigate Prompt Injection attacks.**

---

## 🎥 Project Demo

Here is a demonstration of the system handling PDF ingestion, RAG retrieval, and successfully blocking a Prompt Injection attack in real-time.

[![Ver Video Demo](screenshots/demo_thumbnail.png)](https://drive.google.com/file/d/1tj-II4icP0pN-4CMiWHdfAHoBFTQw5Wu/view?usp=sharing)
*(Click the image above to watch the full demo)*

---

## 🚀 Overview

**MCP-Guard** is a backend system designed to manage knowledge bases securely. Unlike traditional RAG applications, this project implements a **Security Guard Layer** that acts as a middleware between the user input and the LLM/Vector Store.

This architecture was developed as part of a thesis project for **UNMSM**, focusing on the mitigation of adversarial attacks on Large Language Models.

### Key Features

* **🔒 Pre-emptive Security Layer:** Implements heuristic analysis and Regex pattern matching to detect and block Prompt Injection attacks (e.g., "DAN mode", "Ignore previous instructions") *before* they reach the LLM, saving costs and protecting system integrity.
* **📄 Smart Ingestion Pipeline:** Automated processing of PDF documents using `LangChain`, with chunking strategies optimized for retrieval.
* **🧠 Advanced RAG:** Utilizes **Google Gemini 1.5 Flash** for generation and **Google Text-Embedding-004** for high-precision semantic search.
* **⚡ Async Architecture:** Built on **FastAPI** with `async/await` for high-concurrency performance.
* **☁️ Vector Search:** Integration with **Pinecone** (Serverless) for scalable vector storage.
* **🐳 Containerized:** Fully dockerized environment with `Docker Compose` for easy deployment.

---

## 🏗️ Architecture

The system follows **Clean Architecture** principles to ensure scalability and maintainability.

```text
mcp-guard/
├── app/
│   ├── api/            # Endpoints (Chat & Upload)
│   ├── core/           # Config & SECURITY GUARD (The Core Logic)
│   ├── services/       # RAG Logic, Ingestion, & Vector Interaction
│   ├── models/         # SQLAlchemy Database Models
│   └── schemas/        # Pydantic Data Validation
├── docker-compose.yml  # Container Orchestration
└── main.py             # Application Entrypoint