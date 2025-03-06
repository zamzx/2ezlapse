from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from pathlib import Path
from camera import CameraManager
from timelapse import TimelapseProcessor

app = FastAPI(title="2ezlapse API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directories if they don't exist
CAPTURES_DIR = Path("../data/captures")
VIDEOS_DIR = Path("../data/videos")
CAPTURES_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# Initialize camera and timelapse managers
camera_manager = CameraManager(CAPTURES_DIR)
timelapse_processor = TimelapseProcessor(CAPTURES_DIR, VIDEOS_DIR)

# Mount static directories
app.mount("/captures", StaticFiles(directory=str(CAPTURES_DIR)), name="captures")
app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")

class TimelapseSettings(BaseModel):
    interval: int  # seconds between captures
    
@app.get("/")
async def root():
    return {"message": "2ezlapse API is running"}

@app.get("/status")
async def get_status():
    captures = len(list(CAPTURES_DIR.glob("*.jpg")))
    videos = len(list(VIDEOS_DIR.glob("*.mp4")))
    return {
        "captures_count": captures,
        "videos_count": videos,
        "is_capturing": camera_manager.is_capturing,
        "current_interval": camera_manager.interval if camera_manager.is_capturing else None
    }

@app.post("/timelapse/start")
async def start_timelapse(settings: TimelapseSettings):
    try:
        camera_manager.start_timelapse(settings.interval)
        return {"message": f"Started timelapse capture with {settings.interval}s interval"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/timelapse/stop")
async def stop_timelapse():
    try:
        camera_manager.stop_timelapse()
        return {"message": "Stopped timelapse capture"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/timelapse/create")
async def create_timelapse(fps: int = 30):
    try:
        video_name = timelapse_processor.create_timelapse(fps)
        return {
            "message": "Timelapse video created successfully",
            "video_name": video_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos")
async def list_videos():
    return timelapse_processor.get_videos()

@app.on_event("shutdown")
async def shutdown_event():
    camera_manager.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 