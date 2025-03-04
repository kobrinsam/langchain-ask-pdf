from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback



def main():
    load_dotenv()
    st.set_page_config(page_title="ChatFSA")
    st.title("Chat FSA")
    st.header("A chatbot trained on USDA Farm Service Agency handbooks")
    
    # upload file
    pdf_files = ["FLP_general_handbook.pdf","flp_g_direct.pdf", "direct_loanmaking.pdf"]
    
    # extract the text
    if pdf_files is not None:
      for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
          text += page.extract_text()   
      # split into chunks
        text_splitter = CharacterTextSplitter(
          separator="\n",
          chunk_size=1000,
          chunk_overlap=200,
          length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        # create embeddings
        embeddings = OpenAIEmbeddings(openai_api_key= st.secrets["openai"])
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        
      # show user input
      user_question = st.text_input("Ask a question about USDA Farm Service Agency policy:")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        llm = OpenAI(openai_api_key= st.secrets["openai"])
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          print(cb)
           
        st.write(response)


  

if __name__ == '__main__':
    main()
st.write("By Sam Kobrin, REE Analytics Team")
st.write("Data for prototype from USDA Farm Loan Program handbooks")