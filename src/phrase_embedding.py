import torch.nn as nn
import os
    
class PhraseEmbeddingEncoder(nn.Module):
    def forward(self, phrase_texts):
        """
        Encodes phrases (text) into embeddings.
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses must implement the forward method.")

    def save(self, save_path):
        """
        Saves the encoder state to a file.
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses must implement the save method.")

    @staticmethod
    def load(load_path):
        """
        Loads the encoder state from a file.
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses must implement the load method.")


class PhraseEmbeddingDecoder(nn.Module):
    def forward(self, phrase_embeddings):
        """
        Decodes embeddings into phrases (text).
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses must implement the forward method.")

    def save(self, save_path):
        """
        Saves the decoder state to a file.
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses must implement the save method.")

    @staticmethod
    def load(load_path):
        """
        Loads the decoder state from a file.
        Subclasses should implement this method.
        """
        raise NotImplementedError("Subclasses must implement the load method.")

class PhraseEmbeddingModel(nn.Module):
    def __init__(self, phrase_encoder: PhraseEmbeddingEncoder, phrase_decoder: PhraseEmbeddingDecoder):
        super().__init__()
        self.phrase_encoder = phrase_encoder
        self.phrase_decoder = phrase_decoder

    def encode(self, phrase_text):
        return self.phrase_encoder(phrase_text)
    
    def decode(self, phrase_embedding):
        return self.phrase_decoder(phrase_embedding)
    
    def forward(self, phrase_texts):
        phrase_embeddings = self.encoder(phrase_texts)
        return self.decoder(phrase_embeddings)
    
    def save(self, save_dir_path):
        os.makedirs(save_dir_path, exist_ok=True)

        encoder_path = os.path.join(save_dir_path, 'encoder.pth')
        decoder_path = os.path.join(save_dir_path, 'decoder.pth')
        
        self.phrase_encoder.save(encoder_path)
        self.phrase_decoder.save(decoder_path)

    @staticmethod
    def load(load_dir_path):
        encoder_path = os.path.join(load_dir_path, 'encoder.pth')
        decoder_path = os.path.join(load_dir_path, 'decoder.pth')
        
        if not os.path.exists(encoder_path):
            raise FileNotFoundError(f"Encoder file not found: {encoder_path}")
        if not os.path.exists(decoder_path):
            raise FileNotFoundError(f"Decoder file not found: {decoder_path}")
        
        phrase_encoder = PhraseEmbeddingEncoder.load(encoder_path)
        phrase_decoder = PhraseEmbeddingDecoder.load(decoder_path)
        
        return PhraseEmbeddingModel(phrase_encoder, phrase_decoder)
    
from gensim.models import KeyedVectors
import torch
import torch.nn as nn
import os


class Word2VecAveragerPhraseEmbeddingEncoder(PhraseEmbeddingEncoder):
    def __init__(self, word2idx, weights, embedding_dim, fine_tunable=False):
        super().__init__()
        self.fine_tunable = fine_tunable
        self.word2idx = word2idx
        self.embedding_dim = embedding_dim

        # Create the embedding layer
        self.embedding = nn.Embedding.from_pretrained(weights, freeze=not fine_tunable)

    def forward(self, phrase_texts):
        """
        Encode a list of phrases into embeddings by averaging word embeddings.
        """
        embeddings = []
        for phrase in phrase_texts:
            word_indices = [
                self.word2idx[word]
                for word in phrase.split()
                if word in self.word2idx
            ]
            if not word_indices:
                raise ValueError(f"No valid words found in the phrase: {phrase}")
            word_embeddings = self.embedding(torch.tensor(word_indices))
            phrase_embedding = word_embeddings.mean(dim=0)
            embeddings.append(phrase_embedding)
        return torch.stack(embeddings)

    def save(self, save_path):
        """
        Save the encoder state.
        """
        torch.save({
            'word2idx': self.word2idx,
            'embedding_state_dict': self.embedding.state_dict(),
            'embedding_dim': self.embedding_dim,
            'fine_tunable': self.fine_tunable,
        }, save_path)

    @staticmethod
    def load(load_path):
        """
        Load the encoder state.
        """
        checkpoint = torch.load(load_path)
        word2idx = checkpoint['word2idx']
        embedding_dim = checkpoint['embedding_dim']
        fine_tunable = checkpoint['fine_tunable']

        # Create the embedding layer
        weights = torch.zeros(len(word2idx), embedding_dim)
        encoder = Word2VecPhraseEmbeddingEncoder(word2idx, weights, embedding_dim, fine_tunable)
        encoder.embedding.load_state_dict(checkpoint['embedding_state_dict'])
        return encoder
    
    @staticmethod
    def from_pretrained_gensim_keyed_vectors(keyed_vectors, fine_tunable=False):
        """
        Initialize from a Gensim KeyedVectors object.
        """
        word2idx = {word: i for i, word in enumerate(keyed_vectors.index_to_key)}
        weights = torch.tensor(keyed_vectors.vectors, dtype=torch.float32)
        embedding_dim = keyed_vectors.vector_size
        return Word2VecPhraseEmbeddingEncoder(word2idx, weights, embedding_dim, fine_tunable)
    
    @staticmethod
    def load_from_pretrained_gensim_keyed_vectors(model_path, binary=False, fine_tunable=False):
        """
        Load from a Gensim KeyedVectors file.
        """
        keyed_vectors = KeyedVectors.load_word2vec_format(model_path, binary=binary)
        return Word2VecPhraseEmbeddingEncoder.from_pretrained_gensim_keyed_vectors(keyed_vectors)
    
import tensorflow_hub as hub
import torch
import torch.nn as nn
import numpy as np

class UniversalSentenceEncoder(PhraseEmbeddingEncoder):
    def __init__(self, model_url="https://tfhub.dev/google/universal-sentence-encoder/4", fine_tunable=False):
        super().__init__()
        self.fine_tunable = fine_tunable
        self.model = hub.load(model_url)
        
        # Since USE embeddings are not fine-tunable by default, warn if fine-tunable is requested
        if fine_tunable:
            print("Warning: Universal Sentence Encoder does not support fine-tuning directly.")
    
    def forward(self, phrase_texts):
        """
        Encodes a list of phrases into embeddings using USE.
        """
        embeddings = self.model(phrase_texts).numpy()  # Convert TensorFlow tensor to NumPy array
        return torch.tensor(embeddings, dtype=torch.float32)  # Convert to PyTorch tensor

    def save(self, save_path):
        """
        Save the state of the encoder.
        """
        torch.save({'model_url': "https://tfhub.dev/google/universal-sentence-encoder/4",
                    'fine_tunable': self.fine_tunable}, save_path)

    @staticmethod
    def load(load_path):
        """
        Load the encoder from a saved state.
        """
        checkpoint = torch.load(load_path)
        return UniversalSentenceEncoder(
            model_url=checkpoint['model_url'],
            fine_tunable=checkpoint['fine_tunable']
        )
    
from sentence_transformers import SentenceTransformer
import torch

class SBERTPhraseEmbeddingEncoder(PhraseEmbeddingEncoder):
    def __init__(self, model_name='all-MiniLM-L6-v2', fine_tunable=False):
        super().__init__()
        self.fine_tunable = fine_tunable
        self.model_name = model_name

        # Load SBERT model
        self.model = SentenceTransformer(model_name)

        # Configure fine-tuning
        if fine_tunable:
            for param in self.model.parameters():
                param.requires_grad = True

    def forward(self, phrase_texts):
        """
        Encodes a list of phrases into embeddings using SBERT.
        """
        embeddings = self.model.encode(phrase_texts, convert_to_tensor=True)
        return embeddings

    def save(self, save_path):
        """
        Save the state of the encoder.
        """
        torch.save({
            'model_name': self.model_name,
            'fine_tunable': self.fine_tunable,
            'model_state_dict': self.model.state_dict() if self.fine_tunable else None
        }, save_path)

    @staticmethod
    def load(load_path):
        """
        Load the encoder from a saved state.
        """
        checkpoint = torch.load(load_path)
        encoder = SBERTPhraseEmbeddingEncoder(
            model_name=checkpoint['model_name'],
            fine_tunable=checkpoint['fine_tunable']
        )
        if checkpoint['fine_tunable']:
            encoder.model.load_state_dict(checkpoint['model_state_dict'])
        return encoder