from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl

db_faiss_path = "vector_db/db_faiss"
custom_prompt_template = """Use the following pieces of informatiion to answer the user's questions.
If you don't know the answer , please just say that i do not know, don't try to make it up to answer.

context: {}
Question: {question}
Only returs the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompts():
    """ 
        template for qa retriaval for each vector stores.
    """
    prompt = PromptTemplate(template = custom_prompt_template,input_variable=['context','question'])
    return prompt


def load_llm():

    llm = CTransformers(
        model = '',
        model_type= "llama",
        max_new_tokens = 512,
        temperature = 0.5

    )

    return llm


def retriaval_qa_chain(llm,prompt,db):

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={'k':2}),
        return_source_document = True,
        chain_type_kwargs={'prompt':prompt}
    )
    return qa_chain

def qa_bot():
    embeddings = HugginFaceEmbeddings(model = '',model_kwargs={'device':'cpu'})
    db = FAISS.load(db_faiss_path,embeddings)
    llm = load_llm()
    qa_prompt = set_custom_prompts()
    qa = retriaval_qa_chain(llm.qa_chain,db)
    return qa

def final_result(query):

    qa_result = qa_bot()
    response = qa_result({'query':query})
    return response

 














