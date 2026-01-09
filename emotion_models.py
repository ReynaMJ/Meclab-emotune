"""
Emotion Detection Models
Backend-safe mock implementations.
Replace internals with real ML models later.
"""
import requests
import base64
from typing import Dict, Tuple

# Paste your Hugging Face Access Token here
HF_TOKEN = "your_huggingface_token_here"

# We use a state-of-the-art Vision Transformer model for Emotion Recognition
API_URL = "https://api-inference.huggingface.co/models/dima806/facial-emotion-recognition"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def detect_facial_emotion(image_data: str) -> Tuple[str, float, Dict[str, float]]:
    try:
        # 1. Prepare the image
        # Frontend sends 'data:image/jpeg;base64,...', we need just the base64 part
        img_str = image_data.split(",")[1]
        img_bytes = base64.b64decode(img_str)

        # 2. Call Hugging Face API
        response = requests.post(API_URL, headers=headers, data=img_bytes)
        results = response.json()

        # 3. Parse results (HF returns a list: [{'label': 'happy', 'score': 0.9}, ...])
        if isinstance(results, list) and len(results) > 0:
            primary_emotion = results[0]['label'].lower()
            confidence = results[0]['score']
            details = {item['label'].lower(): item['score'] for item in results}
            
            # Map 'neutral' to your JSON's 'emotionless' if necessary
            if primary_emotion == "neutral":
                primary_emotion = "emotionless"
                
            return primary_emotion, confidence, details
        
        return "emotionless", 0.0, {}
    except Exception as e:
        print(f"Hugging Face API Error: {e}")
        return "emotionless", 0.0, {}
from typing import Dict, Tuple

# ============================================================================
# TEXT EMOTION DETECTION
# ============================================================================

def detect_text_emotion(text: str) -> Tuple[str, float, Dict[str, float]]:
    text = text.lower()

    emotions = {
        "happy": 0.1,
        "sad": 0.1,
        "anxious": 0.1,
        "calm": 0.1,
        "angry": 0.1
    }

    if any(w in text for w in ["happy", "joy", "great", "love"]):
        emotions["happy"] = 0.85
    elif any(w in text for w in ["sad", "cry", "down"]):
        emotions["sad"] = 0.8
    elif any(w in text for w in ["anxious", "stress", "nervous"]):
        emotions["anxious"] = 0.9
    elif any(w in text for w in ["angry", "mad", "hate"]):
        emotions["angry"] = 0.8
    else:
        emotions["calm"] = 0.75

    primary = max(emotions, key=emotions.get)
    return primary, emotions[primary], emotions

# ============================================================================
# FACIAL EMOTION DETECTION (MOCK)
# ============================================================================
# ============================================================================
# VOICE EMOTION DETECTION (MOCK)
# ============================================================================

def detect_voice_emotion(audio_path: str) -> Tuple[str, float, Dict[str, float]]:
    emotions = {
        "happy": 0.1,
        "sad": 0.15,
        "anxious": 0.65,
        "calm": 0.05,
        "angry": 0.05
    }
    primary = "anxious"
    return primary, emotions[primary], emotions
