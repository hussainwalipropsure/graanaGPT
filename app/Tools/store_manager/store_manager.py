from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
import pickle
from Tools.store_manager.utils import embeddings_dir

from langchain.vectorstores import FAISS

def store_embeddings(docs, embeddings, store_name="instructEmbeddings", path="embeddings"):
    vectorStore = FAISS.from_documents(docs, embeddings)

    with open(f"{path}/faiss_{store_name}.pkl", "wb") as f:
        pickle.dump(vectorStore,f)
        
def load_embeddings(store_name, path):
    with open(f"{path}/faiss_{store_name}.pkl","rb") as f:
        vector_store = pickle.load(f)
    return vector_store

def create_vector_store():
    root_dir = "docs"
    loader = DirectoryLoader(f'{root_dir}', glob='./Graana.pdf', loader_cls=PyPDFLoader)
    documents=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    from langchain.embeddings import HuggingFaceInstructEmbeddings

    instruct_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large", model_kwargs={"device":"cuda"})

    print("storing embeddings to: ", embeddings_dir)
    store_embeddings(texts, 
                    instruct_embeddings, 
                    store_name='instructEmbeddings', 
                    path=embeddings_dir)
    print("Done!")