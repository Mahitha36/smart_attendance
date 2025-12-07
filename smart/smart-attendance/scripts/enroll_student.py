import os
import sys
import cv2
import numpy as np

# --- Make sure we can import from ../inference ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INF_DIR = os.path.abspath(os.path.join(BASE_DIR, "../inference"))
sys.path.append(INF_DIR)

try:
    from recognition.face_encoder import FaceEncoder
except ModuleNotFoundError as e:
    print("❌ Could not import FaceEncoder from inference/recognition.")
    print("Check your folder structure. Error:", e)
    sys.exit(1)


OUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data/enrollments"))


def capture_images(reg_no, name, n=30):
    """
    Capture n face images for a student by pressing 'c' to save each frame.
    Images stored in: data/enrollments/<reg_no>_<name>/
    """
    path = os.path.join(OUT_DIR, f"{reg_no}_{name}")
    os.makedirs(path, exist_ok=True)

    print("📁 Saving images to:", path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return None

    count = 0
    print("✅ Webcam opened.")
    print("👉 Press 'c' to capture a frame, 'q' to quit enrollment.")

    while count < n:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from webcam.")
            break

        cv2.imshow("Enroll - Press 'c' to capture", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            fname = os.path.join(path, f"{count:03d}.jpg")
            cv2.imwrite(fname, frame)
            print(f"💾 Saved {fname}")
            count += 1

        elif key == ord("q"):
            print("⛔ Enrollment cancelled by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

    if count == 0:
        print("⚠ No images captured.")
        return None

    print(f"✅ Captured {count} images.")
    return path


def generate_embeddings(folder_path, reg_no, name):
    """
    Generate a single averaged embedding from captured images.
    """
    print("🔁 Generating embeddings from captured images...")
    encoder = FaceEncoder()
    embeddings = []

    for fname in os.listdir(folder_path):
        img_path = os.path.join(folder_path, fname)
        img = cv2.imread(img_path)

        if img is None:
            continue

        emb = encoder.embed(img)
        embeddings.append(emb)

    if not embeddings:
        print("❌ No valid images found for embedding.")
        return None

    avg_emb = np.mean(embeddings, axis=0).astype("float32")

    print(f"✨ Generated embedding for {name} ({reg_no})")
    print("➡ Embedding length:", len(avg_emb))

    # TODO: here we should call DB logic like:
    # from backend.db_utils import add_face_embedding
    # add_face_embedding(name, reg_no, avg_emb)

    return avg_emb


if __name__ == "__main__":
    print("🔹 enroll_student.py started with args:", sys.argv)

    if len(sys.argv) < 3:
        print("❌ Usage: python enroll_student.py <REG_NO> <NAME>")
        sys.exit(1)

    reg_no = sys.argv[1]
    name = sys.argv[2]

    folder = capture_images(reg_no, name, n=30)

    if folder:
        generate_embeddings(folder, reg_no, name)
    else:
        print("❌ Enrollment failed (no folder created).")
