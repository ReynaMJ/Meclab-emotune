from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import uuid
import json
import os
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="EmoTune API",
    description="AI-Powered Emotion-Based Music Therapy System",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# ============================================================================
# DATA MODELS (Request/Response Schemas)
# ============================================================================

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class EmotionDetectionRequest(BaseModel):
    user_id: str
    input_type: str = Field(..., description="text, image, or audio")
    data: str = Field(..., description="Text content, base64 image, or audio file path")

class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    timestamp: str
    secondary_emotions: Optional[Dict[str, float]] = None

class MusicRecommendationRequest(BaseModel):
    user_id: str
    emotion: str
    session_id: Optional[str] = None

class Song(BaseModel):
    id: str
    title: str
    artist: str
    file_path: str
    duration: int
    emotion_tags: List[str]
    therapeutic_score: float

class MusicRecommendationResponse(BaseModel):
    emotion: str
    songs: List[Song]
    reasoning: str
    session_id: str

class FeedbackRequest(BaseModel):
    user_id: str
    song_id: str
    session_id: str
    rating: int = Field(..., ge=-1, le=1, description="-1: dislike, 0: neutral, 1: like")
    emotion_match: Optional[bool] = None

# ============================================================================
# DATA STORAGE (Simple JSON-based - Replace with DB in production)
# ============================================================================

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"
TOKENS_FILE = DATA_DIR / "tokens.json"

def load_json(file_path: Path, default=None):
    if default is None:
        default = {}
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return default

def save_json(file_path: Path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

# ============================================================================
# MOCK INTEGRATION POINTS (Replace with actual implementations)
# ============================================================================

def detect_emotion_from_text(text: str) -> EmotionResponse:
    """
    Integration point for Member 1's text emotion detection.
    Replace this with actual model call.
    """
    # Mock implementation
    emotions = {
        "happy": 0.7, "sad": 0.1, "anxious": 0.1, "calm": 0.05, "angry": 0.05
    }
    primary = "happy"
    
    # TODO: Call Member 1's emotion detection function here
    # from models.emotion_models import detect_text_emotion
    # result = detect_text_emotion(text)
    
    return EmotionResponse(
        emotion=primary,
        confidence=emotions[primary],
        timestamp=datetime.utcnow().isoformat(),
        secondary_emotions=emotions
    )

def detect_emotion_from_image(image_data: str) -> EmotionResponse:
    """
    Integration point for Member 1's facial emotion detection.
    Replace this with actual model call.
    """
    # TODO: Implement with Member 1's CNN model
    return EmotionResponse(
        emotion="calm",
        confidence=0.8,
        timestamp=datetime.utcnow().isoformat(),
        secondary_emotions={"calm": 0.8, "happy": 0.15, "sad": 0.05}
    )

def detect_emotion_from_audio(audio_path: str) -> EmotionResponse:
    """
    Integration point for Member 1's voice emotion detection.
    Replace this with actual model call.
    """
    # TODO: Implement with Member 1's speech analysis
    return EmotionResponse(
        emotion="anxious",
        confidence=0.75,
        timestamp=datetime.utcnow().isoformat(),
        secondary_emotions={"anxious": 0.75, "sad": 0.15, "angry": 0.1}
    )

def get_music_recommendations(emotion: str, user_id: str) -> List[Song]:
    """
    Integration point for Member 2's music recommendation logic.
    Replace this with actual recommendation engine.
    """
    # TODO: Call Member 2's recommendation function
    # from services.music_service import recommend_songs
    # return recommend_songs(emotion, user_id)
    
    # Mock implementation
    mock_songs = {
        "happy": [
            Song(id="s1", title="Sunshine Melody", artist="Happy Tunes", 
                 file_path="music/happy/sunshine.mp3", duration=180, 
                 emotion_tags=["happy", "energetic"], therapeutic_score=0.9),
        ],
        "sad": [
            Song(id="s2", title="Healing Rain", artist="Calm Sounds", 
                 file_path="music/sad/healing.mp3", duration=240, 
                 emotion_tags=["sad", "calming"], therapeutic_score=0.85),
        ],
        "anxious": [
            Song(id="s3", title="Peaceful Waters", artist="Meditation Masters", 
                 file_path="music/calm/peaceful.mp3", duration=300, 
                 emotion_tags=["calm", "meditation"], therapeutic_score=0.95),
        ]
    }
    
    return mock_songs.get(emotion, mock_songs["happy"])

# ============================================================================
# AUTHENTICATION HELPERS
# ============================================================================

def create_token(user_id: str) -> str:
    token = str(uuid.uuid4())
    tokens = load_json(TOKENS_FILE, {})
    tokens[token] = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }
    save_json(TOKENS_FILE, tokens)
    return token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    tokens = load_json(TOKENS_FILE, {})
    
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token_data = tokens[token]
    if datetime.fromisoformat(token_data["expires_at"]) < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")
    
    return token_data["user_id"]

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    return {
        "message": "EmoTune API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    users = load_json(USERS_FILE, {})
    
    # Check if username exists
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    if any(u["email"] == user.email for u in users.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user (In production, hash the password!)
    user_id = str(uuid.uuid4())
    users[user.username] = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password,  # TODO: Hash this with bcrypt
        "created_at": datetime.utcnow().isoformat(),
        "preferences": {
            "favorite_emotions": [],
            "music_history": []
        }
    }
    
    save_json(USERS_FILE, users)
    
    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "username": user.username
    }

@app.post("/api/auth/login")
def login_user(credentials: UserLogin):
    users = load_json(USERS_FILE, {})
    
    if credentials.username not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users[credentials.username]
    
    # TODO: Use bcrypt to compare hashed passwords
    if user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["id"])
    
    return {
        "token": token,
        "user_id": user["id"],
        "username": user["username"]
    }

# ============================================================================
# EMOTION DETECTION ENDPOINTS
# ============================================================================

@app.post("/api/emotion/detect", response_model=EmotionResponse)
def detect_emotion(request: EmotionDetectionRequest, user_id: str = Depends(verify_token)):
    # Verify user_id matches token
    if request.user_id != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    try:
        if request.input_type == "text":
            result = detect_emotion_from_text(request.data)
        elif request.input_type == "image":
            result = detect_emotion_from_image(request.data)
        elif request.input_type == "audio":
            result = detect_emotion_from_audio(request.data)
        else:
            raise HTTPException(status_code=400, detail="Invalid input_type")
        
        # Store in session history
        sessions = load_json(SESSIONS_FILE, {})
        if user_id not in sessions:
            sessions[user_id] = []
        
        sessions[user_id].append({
            "timestamp": result.timestamp,
            "emotion": result.emotion,
            "confidence": result.confidence,
            "input_type": request.input_type
        })
        save_json(SESSIONS_FILE, sessions)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotion detection failed: {str(e)}")

# ============================================================================
# MUSIC RECOMMENDATION ENDPOINTS
# ============================================================================

@app.post("/api/music/recommend", response_model=MusicRecommendationResponse)
def recommend_music(request: MusicRecommendationRequest, user_id: str = Depends(verify_token)):
    if request.user_id != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    try:
        songs = get_music_recommendations(request.emotion, user_id)
        session_id = request.session_id or str(uuid.uuid4())
        
        # Psychological reasoning for the recommendation
        reasoning_map = {
            "happy": "Uplifting music to maintain and enhance positive emotions",
            "sad": "Calming music to provide comfort and emotional support",
            "anxious": "Soothing melodies to reduce stress and promote relaxation",
            "angry": "Gradual tempo reduction to calm intense emotions",
            "calm": "Peaceful music to maintain your tranquil state"
        }
        
        return MusicRecommendationResponse(
            emotion=request.emotion,
            songs=songs,
            reasoning=reasoning_map.get(request.emotion, "Music selected to improve your emotional state"),
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

# ============================================================================
# FEEDBACK ENDPOINTS
# ============================================================================

@app.post("/api/feedback/submit")
def submit_feedback(feedback: FeedbackRequest, user_id: str = Depends(verify_token)):
    if feedback.user_id != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    feedbacks = load_json(FEEDBACK_FILE, [])
    
    feedback_entry = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "song_id": feedback.song_id,
        "session_id": feedback.session_id,
        "rating": feedback.rating,
        "emotion_match": feedback.emotion_match,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    feedbacks.append(feedback_entry)
    save_json(FEEDBACK_FILE, feedbacks)
    
    # TODO: Trigger recommendation model update if needed
    
    return {
        "message": "Feedback recorded successfully",
        "feedback_id": feedback_entry["id"]
    }

@app.get("/api/feedback/user/{user_id}")
def get_user_feedback(user_id: str, authenticated_user: str = Depends(verify_token)):
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Cannot access other users' feedback")
    
    feedbacks = load_json(FEEDBACK_FILE, [])
    user_feedbacks = [f for f in feedbacks if f["user_id"] == user_id]
    
    return {
        "user_id": user_id,
        "total_feedback": len(user_feedbacks),
        "feedbacks": user_feedbacks
    }

# ============================================================================
# SESSION & HISTORY ENDPOINTS
# ============================================================================

@app.get("/api/session/history/{user_id}")
def get_session_history(user_id: str, authenticated_user: str = Depends(verify_token)):
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Cannot access other users' history")
    
    sessions = load_json(SESSIONS_FILE, {})
    user_history = sessions.get(user_id, [])
    
    return {
        "user_id": user_id,
        "total_detections": len(user_history),
        "history": user_history
    }

@app.get("/api/user/profile/{user_id}")
def get_user_profile(user_id: str, authenticated_user: str = Depends(verify_token)):
    if user_id != authenticated_user:
        raise HTTPException(status_code=403, detail="Cannot access other users' profile")
    
    users = load_json(USERS_FILE, {})
    user = next((u for u in users.values() if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove sensitive data
    safe_user = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"],
        "preferences": user["preferences"]
    }
    
    return safe_user

# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)