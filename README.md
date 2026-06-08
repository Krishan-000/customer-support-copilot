# Customer Support Copilot (LLM + RAG)

An AI-powered Customer Support Assistant built using Retrieval-Augmented Generation (RAG) to answer customer queries from FAQ and knowledge-base documents.

## Features

* Retrieval-Augmented Generation (RAG)
* Semantic Search using HuggingFace Embeddings
* FAISS Vector Database for efficient retrieval
* Llama 3 integration via Groq API
* Streamlit-based interactive user interface
* Real-time question answering

## Tech Stack

* Python
* LangChain
* FAISS
* HuggingFace Embeddings
* Groq API
* Llama 3
* Streamlit
* Sentence Transformers

## Project Architecture

User Query
→ Embedding Search
→ FAISS Vector Database
→ Retrieve Relevant Context
→ Llama 3 (Groq)
→ Generated Response

## Folder Structure

customer-support-copilot/

├── chatbot.py

├── create_data.py

├── .env

├── .gitignore

├── data/

│ └── faq.txt
│ └── return_policy.txt
│ └── shipping_policy.txt
│ └── warranty_policy.txt
│ └── product_manuel.pdf
│ └── user_guide.pdf 

├── vectordb/

└── README.md

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd customer-support-copilot
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install streamlit
pip install langchain==0.2.16
pip install langchain-community==0.2.16
pip install langchain-openai==0.1.25
pip install langchain-groq
pip install faiss-cpu
pip install sentence-transformers
pip install pypdf
pip install python-dotenv
```

## Environment Variables

Create a .env file:

```env
GROQ_API_KEY=your_api_key_here
```

## Create Vector Database

```bash
python create_data.py
```

## Run Application

```bash
streamlit run chatbot.py
```

## Sample Questions

* How long does shipping take?
* Can customers return products?
* How can I track my order?
* How to reset password?

## Future Enhancements

* Multi-PDF Support
* Source Citations
* Chat Memory
* Sentiment Analysis
* Ticket Classification
* Analytics Dashboard
* Cloud Deployment



