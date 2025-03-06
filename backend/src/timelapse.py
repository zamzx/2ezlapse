import subprocess
import logging
from pathlib import Path
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimelapseProcessor:
    def __init__(self, captures_dir: Path, videos_dir: Path):
        self.captures_dir = captures_dir
        self.videos_dir = videos_dir
        
    def create_timelapse(self, fps: int = 30) -> str:
        """Create a timelapse video from the captured photos"""
        # Ensure output directory exists
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        
        # Get list of photos sorted by name (which includes timestamp)
        photos = sorted(self.captures_dir.glob("*.jpg"))
        if not photos:
            raise ValueError("No photos found in captures directory")
        
        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.videos_dir / f"timelapse_{timestamp}.mp4"
        
        # Create FFmpeg command
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if exists
            "-pattern_type", "glob",
            "-i", str(self.captures_dir / "*.jpg"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            str(output_file)
        ]
        
        try:
            # Run FFmpeg command
            logger.info(f"Creating timelapse with {len(photos)} photos at {fps} FPS")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(f"Timelapse created: {output_file.name}")
            return output_file.name
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise RuntimeError("Failed to create timelapse video")
    
    def get_videos(self):
        """Get list of all timelapse videos"""
        videos = []
        for video in self.videos_dir.glob("*.mp4"):
            videos.append({
                "name": video.name,
                "created": datetime.fromtimestamp(video.stat().st_ctime).isoformat(),
                "size": video.stat().st_size
            })
        return sorted(videos, key=lambda x: x["created"], reverse=True) 