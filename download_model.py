from huggingface_hub import hf_hub_download
from tensorflow.keras.models import load_model

def load_pretrained_emotion_model():
    model_path = hf_hub_download(repo_id="shivampr1001/Emo0.1", filename="Emo0.1.h5")
    model = load_model(model_path)
    return model

if __name__ == "__main__":
    model = load_pretrained_emotion_model()
    print("Model loaded from:", model)
