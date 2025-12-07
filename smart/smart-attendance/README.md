1. Create a Python venv and install dependencies:
python-m venv venv
source venv/bin/activate
pip install-r backend/requirements.txt
pip install-r ../requirements.txt # or umbrella file

1. Start backend API:
cd backend
uvicorn app.main:app--reload--host 0.0.0.0--port 8000

1.(Optional) Start frontend dev server:
cd frontend
npm install
npm run dev

1.Enroll a sample student (capture images):
python scripts/enroll_student.py REG001 "Alice"
# press 'c' to capture frames until required count

1. Run inference locally:
python inference/run_inference.py
# a window will show webcam with boxes; backend will receive /api/events