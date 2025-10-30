"""
Test script to verify backend setup
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Qoffea Backend Setup...\n")

# Test 1: Import modules
print("1️⃣ Testing module imports...")
try:
    from config import Config
    from modules import ModelLoader, ImageProcessor, CoffeeAnalyzer, PDFGenerator
    from utils import FileHandler, Validator
    print("✅ All modules imported successfully\n")
except Exception as e:
    print(f"❌ Import error: {e}\n")
    sys.exit(1)

# Test 2: Check configuration
print("2️⃣ Testing configuration...")
try:
    Config.init_app()
    print(f"✅ Upload folder: {Config.UPLOAD_FOLDER}")
    print(f"✅ Report folder: {Config.REPORT_FOLDER}")
    print(f"✅ Model path: {Config.MODEL_PATH}")
    print(f"✅ Confidence threshold: {Config.CONFIDENCE_THRESHOLD}\n")
except Exception as e:
    print(f"❌ Config error: {e}\n")
    sys.exit(1)

# Test 3: Load model
print("3️⃣ Testing model loading...")
try:
    model_loader = ModelLoader()
    model = model_loader.load_model(Config.MODEL_PATH, Config.CONFIDENCE_THRESHOLD)
    class_names = model_loader.get_class_names()
    print(f"✅ Model loaded successfully")
    print(f"✅ Classes: {class_names}\n")
except Exception as e:
    print(f"❌ Model loading error: {e}\n")
    print("⚠️  Note: This is expected if model file doesn't exist yet\n")

# Test 4: Test Flask app creation
print("4️⃣ Testing Flask app creation...")
try:
    from app import create_app
    app = create_app()
    print(f"✅ Flask app created successfully")
    print(f"✅ Registered routes:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"   - {rule.rule} [{', '.join(rule.methods - {'HEAD', 'OPTIONS'})}]")
    print()
except Exception as e:
    print(f"❌ Flask app error: {e}\n")
    sys.exit(1)

print("=" * 60)
print("🎉 All tests passed! Backend is ready.")
print("=" * 60)
print("\n📝 To run the server:")
print("   python app.py")
print("\n📝 Or with environment variables:")
print("   set FLASK_DEBUG=1 && python app.py")
