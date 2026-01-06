# 📄 Chat with Documents — RAG System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented--Generation-green)
![LLM](https://img.shields.io/badge/LLM-Ollama%20(Local)-orange)
![Embeddings](https://img.shields.io/badge/Embeddings-Gemini-purple)
![VectorDB](https://img.shields.io/badge/VectorDB-ChromaDB-red)
![UI](https://img.shields.io/badge/UI-Streamlit-brightgreen)
![Evaluation](https://img.shields.io/badge/Evaluation-Retrieval%20%7C%20Generation-yellow)

---

## 🔍 Project Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for **question answering over PDF documents**.

The focus is on:
- **Correctness**
- **Grounded answers**
- **Explicit evaluation**

rather than open-ended conversational behavior.

The system:
- Retrieves relevant document chunks using **vector similarity**
- Generates answers **strictly grounded in retrieved content**
- Uses **local LLMs** for generation and evaluation
- Provides an **interactive Streamlit interface**
- Includes **retrieval and generation evaluation pipelines**

---

## 📚 PDF Dataset

The system operates on a curated set of **PDF rulebooks**, chosen for their factual density and well-defined rules.

### Included Documents

#### 📘 monopoly.pdf
Official Monopoly rulebook containing:

#### 📕 ticket_to_ride.pdf
Official Ticket to Ride rulebook containing:

---

## 🧠 System Architecture (RAG Pipeline)

The system follows a modular Retrieval-Augmented Generation architecture, designed to ensure factual grounding, traceability, and evaluability.
---
## 📊 Evaluation Pipeline

The system includes an explicit evaluation layer that separately assesses:

- **Retrieval quality** using objective, retrieval-based metrics
- **Answer generation quality** using the **LLM-as-a-Judge** paradigm

This separation ensures clarity, reproducibility, and methodological correctness.

---

### 🔍 Retrieval Evaluation (Metric-Based)

**Objective:** Measure whether the retrieval step successfully selects document chunks that contain the information required to answer the user question.

#### Evaluation Process
1. A set of reference (expected) document chunks is defined per question
2. The retriever returns the top-*k* chunks
3. Retrieved chunks are compared against the reference set

#### Metrics
- **Recall@k**: Measures whether at least one relevant chunk appears in the top-*k*
- **Precision@k**: Measures the proportion of relevant chunks among retrieved ones

#### Rationale
Retrieval evaluation is:
- **Deterministic**
- **Model-agnostic**
- **Independent of generation quality**

This avoids bias introduced by generative models during retrieval assessment.

---

### ✍️ Generation Evaluation (LLM as Judge)

**Objective:** Evaluate the quality of the generated answer given the retrieved context.

#### Evaluation Process
1. The user question, retrieved chunks, and generated answer are provided to a **judge LLM**
2. The judge compares the answer against the retrieved context
3. A structured verdict is produced

#### Evaluation Criteria
- **Faithfulness**: Answer uses only information present in retrieved chunks
- **Completeness**: Answer fully addresses the question
- **Hallucination Check**: No unsupported facts are introduced

#### Judge Model
- Local LLM executed via **Ollama**
- Same or separate model from the generator
- Fully offline and reproducible

---

### 🧠 Design Choice: Why LLM as Judge Only for Generation?

- Retrieval quality can be evaluated using **objective metrics**
- Generation quality requires **semantic and factual reasoning**
- LLM-based judgment aligns better with **human evaluation** of answers
- Clear separation improves experimental validity



