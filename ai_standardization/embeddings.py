from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(text_list):
    return model.encode(text_list, show_progress_bar=False)
