import os

from sentence_transformers import SentenceTransformer

from config import env

os.environ["HF_TOKEN"] = env.HFTOKEN
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


class TransformerModel:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            print(f"Loading embedding model: {env.MODEL}...")
            self.model = SentenceTransformer(env.MODEL)
            print("Model loaded!")
        return self.model

    def release_model(self):
        print("Shutting down model...")
        self.model = None

    def encode(self, text: str):  # ← Add this
        """Encode text to embedding"""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        return self.model.encode(text)


model_instance = TransformerModel()
