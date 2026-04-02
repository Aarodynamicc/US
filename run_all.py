import os
import subprocess

print("🚀 Starting pipeline...\n")

model_path = "model/sign_model.h5"

if not os.path.exists(model_path):
    print("🧠 Training model...\n")
    result = subprocess.run(["python", "model/train_model.py"])

    if result.returncode != 0:
        print("❌ Training failed. Fix errors first.")
        exit()
else:
    print("✅ Model exists, skipping training.\n")

print("🎥 Starting real-time detection...\n")
subprocess.run(["python", "inference/realtime.py"])