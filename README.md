# 2ezlapse

A simple and efficient web-based timelapse 

<img width="872" alt="Screenshot 2025-03-07 at 8 53 45 AM" src="https://github.com/user-attachments/assets/3a714bf6-39a6-4675-9d00-6c04e252246d" />
application that uses your system camera to create beautiful timelapses with configurable intervals.

## Features

- 📸 Capture photos using system camera at configurable intervals
- 🎥 Automatically generate timelapse videos using FFmpeg
- 🌐 Modern web interface for:
  - Starting/stopping timelapse capture
  - Configuring capture intervals
  - Viewing capture statistics
  - Generating and viewing timelapse videos
  - Browsing capture history

## Prerequisites

- Python 3.8+
- Node.js 16+
- FFmpeg
- Web camera connected to your system

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zamzx/2ezlapse.git
   cd 2ezlapse
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend/src
   python app.py
   ```
   The backend server will run on http://localhost:8000

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Configure the capture interval (in seconds)
3. Click "Start Capture" to begin the timelapse
4. Monitor the capture progress and preview the latest photo
5. When ready, click "Stop Capture"
6. Click "Generate Timelapse" to create a video from the captured photos
7. View and download your timelapse video

## Project Structure

```
2ezlapse/
├── backend/              # Python FastAPI backend
│   ├── requirements.txt  # Python dependencies
│   └── src/
│       ├── app.py       # Main FastAPI application
│       ├── camera.py    # Camera handling module
│       └── timelapse.py # Timelapse processing module
├── frontend/            # Next.js frontend
│   ├── package.json    # Node dependencies
│   └── src/           # Frontend source code
└── data/              # Data storage
    ├── captures/     # Captured photos
    └── videos/       # Generated timelapses
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
