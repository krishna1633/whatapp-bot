import spacy
import torch
from sentence_transformers import SentenceTransformer, util
import docx

class ChatBot:
    def __init__(self, doc_path):
        self.nlp = spacy.load("en_core_web_sm")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.knowledge_base = self.load_document(doc_path)
        self.knowledge_texts = list(self.knowledge_base.values())
        self.knowledge_embeddings = self.model.encode(self.knowledge_texts, convert_to_tensor=True)

    def load_document(self, doc_path):
        """Extracts text from the docx file and stores meaningful chunks."""
        doc = docx.Document(doc_path)
        text = "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
        
        # Split text into meaningful sentences or paragraphs
        doc_nlp = self.nlp(text)
        knowledge_base = {}

        chunks = [sent.text.strip() for sent in doc_nlp.sents if len(sent.text.strip()) > 10]  # Filter short texts
        for i, chunk in enumerate(chunks):
            knowledge_base[f"Chunk {i+1}"] = chunk
        
        return knowledge_base

    def get_answer(self, query):
        """Finds the best-matching answer from the document chunks, prioritizing relevant keywords."""
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.knowledge_embeddings)[0]
        best_match_idx = scores.argmax().item()
        best_match_text = self.knowledge_texts[best_match_idx]
        
        # Prioritize chunks containing relevant words
        keywords = ["time", "timings", "schedule", "hours", "open", "close"]
        for chunk in self.knowledge_texts:
            if any(keyword in chunk.lower() for keyword in keywords):
                return chunk  # Return this instead if it contains relevant words

        # If no keyword match, return best semantic match
        if scores[best_match_idx] > 0.5:
            return best_match_text
        else:
            return "I'm sorry, I don't have an answer for that."

# Initialize chatbot with document path
chatbot = ChatBot("business_doc.docx")

# Example Query
# query = "What are the class timings for Earthen Hues?"
# response = chatbot.get_answer(query)
# print("Query:", query)
# print("Response:", response)
