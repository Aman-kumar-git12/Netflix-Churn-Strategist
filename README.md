<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" alt="Netflix Logo" width="180"/>
  <br>
  <h1>🎬 Netflix Customer Churn Strategist</h1>
  <p><strong>The Ultimate Agentic Marketing Operations (MarOps) Ecosystem</strong></p>

  [![Python 3.14+](https://img.shields.io/badge/Python-3.14+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
  [![Agentic AI](https://img.shields.io/badge/Agentic-AI-orange.svg?style=for-the-badge)](#)
  [![RAG Enabled](https://img.shields.io/badge/RAG-Enabled-brightgreen.svg?style=for-the-badge)](#)
  [![Enterprise Architecture](https://img.shields.io/badge/Architecture-Enterprise-blueviolet.svg?style=for-the-badge)](#)
  
  <br>
  
  **[Live Demo](https://netflix-churn-ai.streamlit.app/)** • **[Logic Tier Code](./logic/)** • **[UI Pages Code](./pages/)**
</div>

---

## 📖 1. Overview
The **Netflix Customer Churn Strategist** is an end-to-end intelligence ecosystem designed to solve the "Retention Gap" in digital streaming platforms.
While traditional churn systems stop at predicting risk, this project acts as an **Agentic Co-pilot**. It uses predictive machine learning to flag high-risk customers, and Generative AI (LLaMA 3.3) paired with RAG to autonomously draft personalized, corporate-aligned retention strategies in milliseconds. Our solution transforms passive analytics into active, revenue-saving business operations.

## 🎯 2. Problem Statement
**The Retention Flaw in Modern Enterprises:**
Most churn management systems are purely **Passive**. They provide a risk score (e.g., "Customer X is 80% likely to churn") but leave the human manager to guess the remedy. This manual intervention delays action, relies on guesswork, and leads to generic marketing that fails. 

This project automates the entire pipeline: from diagnosing the exact mathematical cause of churn to executing a highly personalized, targeted retention campaign.

## 🚀 3. Features
- **Deterministic Churn Prediction:** Path-tracing decision trees to find the exact factor driving a user away.
- **RAG-Powered Knowledge Base:** Prevents generic AI responses by grounding strategies in corporate playbooks (PDFs via ChromaDB).
- **Self-Refining Multi-Agent Team:** LangGraph orchestrates a Researcher, Architect, and Critic agent to draft, review, and perfect executive-level emails.
- **Enterprise Dashboard:** A reactive, professional UI built on Streamlit with tabs for Batch Orchestration and AI Auditing.
- **Reinforcement Learning Feedback:** Learns from campaign failures via historical logs to constantly improve success rates.

## 🧠 4. Tech Stack
- **Languages / Core:** Python 3
- **Predictive ML:** Scikit-Learn, Pandas, NumPy
- **Generative AI Engine:** LLaMA-3.3 70B (via Groq API for near-zero latency)
- **Agentic Orchestration:** LangChain, LangGraph
- **Vector Database (RAG):** ChromaDB, HuggingFace Embeddings (`all-MiniLM-L6-v2`)
- **Frontend / UI:** Streamlit

## 📊 5. Dataset
- **Source:** Simulated Enterprise Netflix Telemetry Data
- **Size:** 5,000+ Customer Records
- **Features:** 12 High-Impact Attributes (e.g., `subscription_type`, `monthly_fee`, `watch_hours`, `last_login_days`, `favorite_genre`)
- **Preprocessing steps:**
  - Dynamic removal of strict identifiers (`customer_id`).
  - Categorical Variable Encoding (One-Hot Encoding via `pd.get_dummies`).
  - Strict formatting for ML pipeline consistency preventing test-set leakage.

## ⚙️ 6. Model & Approach
- **Algorithms used:**
  - Regularized Decision Tree Classifier
- **Why this model?**
  While Neural Networks are powerful, Marketing teams require **Explainability**. Decision Trees offer absolute transparency. We use programmatic Path Tracing to calculate Probability Deltas at each node, giving our AI agents the exact mathematical reason a user is leaving, rather than having the LLM "hallucinate" a reason.
- **Training process:**
  - 80/20 Train-Test Stratified Split.
  - Hyperparameter tuning (`max_depth=10`, `min_samples_leaf=2`) for generalization.

## 📈 7. Results & Metrics
*Evaluated on the 20% holdout test set.*

| Model | Accuracy | Precision | Recall | F1 Score |
|------|----------|----------|--------|----------|
| Decision Tree Classifier | 97.9% | 98.2% | 97.5% | 97.8% |

**Business Impact:** High precision ensures we do not waste aggressive discounts on users who were never going to churn (minimizing false positives), saving critical revenue.

## 📷 8. Demo
*Add screenshots of your dashboard here to impress recruiters.*
- ✅ **Model Dashboard:** Displays real-time feature distributions and probability scores.
- ✅ **AI Strategist View:** Generating personalized, non-cliché emails via Multi-Agent logic.

## 🛠️ 9. Installation & Setup

```bash
git clone https://github.com/samaysamrat/Netflix-Churn-Strategist.git
cd Netflix-Churn-Strategist
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Security Setup (.env)
You must set your Groq API key to run the Large Language Models.
```env
GROQ_API_KEY=your_groq_api_key_here
```

## ▶️ 10. How to Run

Launch the Enterprise Application:
```bash
streamlit run app.py
```

## 📂 11. Project Structure

```text
Netflix-Churn-Strategist/
│── data/                     # CSV datasets and PDF Playbooks
│── logic/                    # Core Engine
│   ├── ai_agent.py           # LangGraph Multi-Agent Team
│   ├── churn_model.py        # Scikit-Learn Path Tracing
│   └── rag_system.py         # ChromaDB Vector Store
│── notebooks/                # EDA and ML Experiments
│── pages/                    # Streamlit Dashboard Views
│── utils/                    # Helper Functions
│── app.py                    # Application Entry Point
│── requirements.txt          # Dependencies
```

## 👥 12. Team Members

- **Vipul Sharma** – Chief ML Architect & Optimization Lead
- **Lokendra Singh** – Data Systems & Operations Engineering
- **Samay Samrat** – Infrastructure Deployment & DevOps
- **Aman Kumar** – Data Engineering & Acquisition

## 🔮 13. Future Improvements
- **Real-Time RL:** Continually fine-tuning the Decision Tree based on which strategies the Manager actually approves in the Auditor page.
- **Global Scaling:** Moving from local ChromaDB to a cloud-native vector store like Pinecone for multi-region deployment.
- **Multi-Modal Agents:** Generating personalized video previews directly within emails for at-risk users.

## 📜 14. License
MIT License
