import streamlit as st

from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

st.set_page_config(
    page_title="Customer Support Copilot",
    page_icon="🤖"
)

load_dotenv()

answer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a customer support assistant. Answer using the retrieved "
        "context as the source of truth. If the context does not contain the "
        "answer, say you do not know and suggest contacting support. Be concise.\n\n"
        "Retrieved context:\n{context}"
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])


@st.cache_resource(show_spinner="Loading support resources...")
def load_resources():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.load_local(
        "vectordb",
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )
    return retriever, llm


st.title("🤖 Customer Support Copilot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input(
    "Ask a question about shipping, refunds, payments..."
)

if query:

    
    st.chat_message("user").markdown(query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    retriever, llm = load_resources()
    with st.spinner("Searching support resources..."):
        source_documents = retriever.invoke(query)

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'knowledge base')}\n{doc.page_content}"
        for doc in source_documents
    )
    chat_history = [
        HumanMessage(content=message["content"])
        if message["role"] == "user"
        else AIMessage(content=message["content"])
        for message in st.session_state.messages[:-1][-6:]
    ]
    prompt_messages = answer_prompt.format_messages(
        context=context,
        chat_history=chat_history,
        question=query
    )

    with st.chat_message("assistant"):
        answer = st.write_stream(
            chunk.content
            for chunk in llm.stream(prompt_messages)
            if chunk.content
        )

        with st.expander("Sources Used"):

            for i, doc in enumerate(
                source_documents,
                start=1
            ):
                st.markdown(f"### Source {i}")
                st.write(doc.page_content)

    st.session_state.messages.append(

        {
          "role": "assistant",
          "content": answer
        }

       
    )

    