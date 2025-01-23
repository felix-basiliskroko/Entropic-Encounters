import json
import requests

from logic.llm.rag import load_chunks, retrieve


def prompt_llm(user_prompt, top_chunks=3):
    """
    Function to generate a response from the LLM model on Hugging Face
    :param user_prompt: Question asked by the user
    :param top_chunks: Number of top chunks to retrieve
    :return: The generated response from the LLM model
    """

    with open("logic/llm/misc.json") as f:
        misc = json.load(f)
        api_key = misc.get("hugging_face_api_token")
        global_system_prompt = misc.get("global_sys_prompt")

    embeddings_file = "logic/RAG_files/chunk_embeddings_mac.pkl"
    chunks, embeddings = load_chunks(embeddings_file)
    retrieved_knowledge = retrieve(user_prompt, chunks, embeddings, top_n=top_chunks)
    similarity_threshold = 1.0
    rag_info = ""

    if any(similarity < similarity_threshold for _, similarity in retrieved_knowledge):
        chunks_combined = ("The prompt didn't provide additional context, relating sufficiently to the game."
                           "Respond as you seem fit, and remember to always steer the conversation back"
                           " to Entropic Encounters if the question is off-topic.")
    else:
        rag_info = " ".join([chunk for chunk, similarity in retrieved_knowledge])

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
    headers = {"Authorization": f"Bearer {api_key}"}

    full_prompt = f"<s>[INST] {user_prompt} [/INST] {global_system_prompt} </s>[INST] {rag_info} [/INST]"

    payload = {
        "inputs": full_prompt,
        "options": {"use_cache": False},
        "parameters": {"return_full_text": True, "repetition_penalty": 1.0, "max_length": 3_000}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response = response.json()
    gen_response = response[0]["generated_text"].split("[/INST]")[-1]
    return gen_response

