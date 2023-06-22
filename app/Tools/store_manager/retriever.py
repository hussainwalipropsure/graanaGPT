
from Tools.store_manager.store_manager import load_embeddings

embeddings_dir = "embeddings"
store_name='instructEmbeddings'

def get_retriever():
    db_instruct_embeddings = load_embeddings(store_name=store_name,path=embeddings_dir)
    retriever = db_instruct_embeddings.as_retriever(search_kwargs={"k":2})
    return retriever

def get_relevant_docs(query):
    db_instruct_embeddings = load_embeddings(store_name=store_name,path=embeddings_dir)
    retriever = db_instruct_embeddings.as_retriever(search_kwargs={"k":2})
    docs = retriever.get_relevant_documents(query)
    return docs

import re
def get_relevant_text(query):
    print(f"\n\n in get_relevant_text: {query=}\n")
    
    x = get_relevant_docs(query=query)
    st = ""
    for doc in x:
        clean_str = re.sub(' ','', doc.page_content)
        st+=re.sub(r'\n',' ', clean_str)
    return st    

