# scaffold_empty_smart_attendance.py

import os

ROOT = "smart-attendance"

FILES = [
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/models.py",
    "backend/app/schemas.py",
    "backend/app/crud.py",
    "backend/app/deps.py",
    "backend/Dockerfile",
    "backend/requirements.txt",

    "inference/detector/yolov_wrapper.py",
    "inference/recognition/face_encoder.py",
    "inference/liveness/liveness_model.py",
    "inference/behavior/behavior_model.py",
    "inference/run_inference.py",

    "frontend/src/App.jsx",
    "frontend/src/index.jsx",
    "frontend/package.json",

    "scripts/enroll_student.py",
    "scripts/make_faiss_index.py",

    "data/enrollments/.gitkeep",
    "data/models/.gitkeep",

    "docker-compose.yml",
    "README.md",
    "requirements.txt"
]


def create_structure():
    for file in FILES:
        path = os.path.join(ROOT, file)
        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write("")  # EMPTY FILE

        print("Created:", path)


if __name__ == "__main__":
    create_structure()
    print("\n🎉 Empty Smart Attendance project scaffold created successfully!")
