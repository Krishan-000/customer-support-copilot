import streamlit as st

from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.chains import RetrievalQA

from langchain_groq import ChatGroq

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


db = FAISS.load_local(
    "vectordb",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)


qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)

st.set_page_config(
    page_title="Customer Support Copilot",
    page_icon="🤖"
)


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

    with st.spinner("Thinking..."):

        result = qa_chain.invoke(
            {
                "question": query
            }
        )

        answer = result["answer"]

    
    with st.chat_message("assistant"):
        st.markdown(answer)

        with st.expander("Sources Used"):

            for i, doc in enumerate(
                result["source_documents"],
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

    