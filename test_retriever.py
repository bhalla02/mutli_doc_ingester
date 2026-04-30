import os
from pathlib import Path
from dotenv import load_dotenv
from multi_Doc_chat.utils.model_loader import ModelLoader
from langchain_community.vectorstores import FAISS

load_dotenv()

# Find the latest FAISS index
faiss_base = Path("faiss_index")
if faiss_base.exists():
    sessions = sorted([d for d in faiss_base.iterdir() if d.is_dir()])
    if sessions:
        latest_session = sessions[-1]
        index_path = latest_session
        
        print(f"Loading FAISS index from: {index_path}")
        
        embeddings = ModelLoader().load_embeddings()
        vectorstore = FAISS.load_local(
            str(index_path),
            embeddings,
            index_name="index",
            allow_dangerous_deserialization=True
        )
        
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
        )
        
        # Test queries
        queries = [
            "what is attention?",
            "attention mechanism",
            "transformer architecture",
            "self-attention",
            "attention is all you need"
        ]
        
        for query in queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}")
            docs = retriever.invoke(query)
            print(f"Retrieved {len(docs)} documents:")
            for i, doc in enumerate(docs, 1):
                content = doc.page_content[:200]
                print(f"\n[Doc {i}]")
                print(f"{content}...")
    else:
        print("No FAISS sessions found")
else:
    print("faiss_index directory not found")
