import os
import numpy as np

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# Step 1 — Collect HR documents
# ============================================================

documents = []

files = os.listdir("hr_knowledge")

for file in files:
    if file.endswith(".txt"):
        with open("hr_knowledge/" + file, "r") as f:
            text = f.read()
            documents.append(text)


# ============================================================
# Step 2 — Chunk the documents
# ============================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", ". ", "\n", " ", ""]
)

document_chunks = []

for document in documents:
    document_chunks.extend(
        splitter.split_text(document)
    )


# ============================================================
# Step 3 — Create embeddings for chunks
# ============================================================

transformer = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = []

for chunk in document_chunks:
    vector = transformer.encode(chunk)
    embeddings.append(vector)


# ============================================================
# Step 4 — User question
# ============================================================

question = input("Ask HR Bot: ")

question_vector = transformer.encode(question)


# ============================================================
# Step 5 — Calculate similarity
# ============================================================

similarity_scores = cosine_similarity(
    [question_vector],
    embeddings
)

scores = similarity_scores[0]


# ============================================================
# Step 6 — Retrieve Top-K chunks
# ============================================================

sorted_indices = np.argsort(scores)[::-1]

top_k = 3

top_indices = sorted_indices[:top_k]

top_chunks = [
    document_chunks[i]
    for i in top_indices
]


# ============================================================
# Step 7 — Create context
# ============================================================

context = "\n\n".join(top_chunks)


# ============================================================
# Step 8 — Setup Groq
# ============================================================

load_dotenv()

myapi = os.getenv("GROQ_API_KEY")

if not myapi:
    raise ValueError("API key not found")

client = Groq(api_key=myapi)

model = "openai/gpt-oss-120b"


# ============================================================
# Step 9 — Send context + question to LLM
# ============================================================

prompt = f"""
You are an HR assistant.

Answer the user's question using ONLY the provided HR context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the available HR documents."

HR Context:
{context}

User Question:
{question}
"""

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# ============================================================
# Step 10 — Print final answer
# ============================================================

answer = response.choices[0].message.content

print("\n--- HR Bot Answer ---")
print(answer)