from sentence_transformers import SentenceTransformer
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def gen_embeddings(file_path, output_file_path):
    """
    Generate embeddings for chunks of text in a file and save them to a pickle file
    :param file_path: The path to the file containing the text chunks
    :param output_file_path: The path to save the embeddings to
    :return: None
    """
    chunks = []
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    with open(file_path, 'r', encoding='utf-8') as file:
        current_chunk = []
        for line in file:
            if line.strip():
                current_chunk.append(line.strip())
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
        if current_chunk:
            chunks.append(" ".join(current_chunk))

    embeddings = model.encode(chunks, convert_to_tensor=True)

    with open(output_file_path, "wb") as f:
        pickle.dump({"chunks": chunks, "embeddings": embeddings}, f)


def load_chunks(file_path):
    """
    Load chunks and embeddings from a pickle file
    :param file_path: The path to the pickle file
    :return: The chunks and embeddings
    """
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]
    embeddings = data["embeddings"]

    return chunks, embeddings


'''
def retrieve(query, chunks, embeddings, top_n=3):
    """
    Retrieve the top N chunks based on the similarity of their embeddings to the query
    :param query: The prompt of the user
    :param chunks: The list of text chunks
    :param embeddings: The embeddings of the text chunks
    :param top_n: The number of chunks to retrieve
    :return: The top N chunks and their similarity scores
    """
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = []

    for chunk, embedding in zip(chunks, embeddings):
        # Move tensors to CPU and convert to numpy arrays for sklearn compatibility
        similarity = cosine_similarity(
            query_embedding.cpu().unsqueeze(0).numpy(),
            embedding.cpu().unsqueeze(0).numpy()
        )[0][0]

        similarities.append((chunk, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]
'''


def retrieve(query, chunks, embeddings, top_n=3):
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = []
    # Pair chunks with their corresponding embeddings
    for chunk, embedding in zip(chunks, embeddings):
        embedding = embedding.cpu()
        query_embedding = query_embedding.cpu()
        similarity = cosine_similarity(query_embedding.unsqueeze(0), embedding.unsqueeze(0))[0][0]
        similarities.append((chunk, similarity))
    # Sort by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]