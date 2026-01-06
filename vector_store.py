from langchain_chroma import Chroma
from ingestion import load_documents, split_documents, get_embeddings
import os

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        # concatenate the source and the page number to make an id for each chunk
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # example of an id : data/monopoly.pdf:6
        # to see if this particular chunk exists in the database already,
        # and if it's not, then we can add it

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # the chunks id looks like :
        # data/monopoly.pdf:0:0
        # data/monopoly.pdf:0:1
        # data/monopoly.pdf:1:0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

        # Update last page id
        last_page_id = current_page_id

    return chunks



def build_or_update_chroma_db(chunks, embeddings, chroma_path="chroma_db"):
    # 🔒 SI DB EXISTE → ON LA CHARGE SEULEMENT
    if os.path.exists(chroma_path) and os.listdir(chroma_path):
        print("✅ Loading existing Chroma DB (read-only)")
        return Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )

    # 🆕 CRÉATION UNE SEULE FOIS
    print("Creating Chroma DB (first time)")

    chunks = calculate_chunk_ids(chunks)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path
    )
    db.persist()
    return db

