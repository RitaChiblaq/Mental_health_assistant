from transformers import AutoTokenizer, AutoModel
import torch

# Load the pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Generates a text embedding using a pre-trained model.

    Args:
        text (str): The text to be embedded.

    Returns:
        List[float]: The generated text embedding.
    """
    # Tokenize the text. Convert the text to input IDs and attention masks.
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)

    # Generate the embeddings without computing gradients (inference mode).
    with torch.no_grad():
        outputs = model(**inputs)  # Pass inputs through the model
        # Average the token embeddings to get the sentence embedding
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    return embeddings