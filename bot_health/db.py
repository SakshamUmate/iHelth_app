from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.embeddings import HugginFaceEmbeddings
from langchain.vectorstores import FAISS

data_path = "data/"
db_faiss_path = "vector_db/db_faiss"

def create_vector_db():
    loader = DirectoryLoader(data_path,glob='*.pdf',loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    texts = text_splitter.split_documents(documents=documents)

    embeddings = HugginFaceEmbeddings(model = '',model_kwargs={'device':'cpu'})
    db = FAISS.from_documents(texts,embeddings)
    db.save_local(db_faiss_path)


if __name__ == '__main__':
    create_vector_db()

