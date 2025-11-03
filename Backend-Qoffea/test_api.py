"""
Test script untuk backend API
"""
import requests
import os

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /api/health...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_index():
    """Test index endpoint"""
    print("\n🔍 Testing /...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_upload(image_path):
    """Test upload endpoint"""
    print(f"\n🔍 Testing /api/upload with {image_path}...")
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'source': 'test'}
        response = requests.post(f"{BASE_URL}/api/upload", files=files, data=data)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Success: {result.get('success')}")
    
    if result.get('success'):
        analysis = result.get('analysis', {})
        print(f"Total beans: {analysis.get('total_beans')}")
        print(f"Good beans: {analysis.get('good_beans')} ({analysis.get('good_percentage')}%)")
        print(f"Defect beans: {analysis.get('defect_beans')} ({analysis.get('defect_percentage')}%)")
        print(f"Grade: {analysis.get('grade')}")
        print(f"Analysis ID: {result.get('analysis_id')}")
        return result.get('analysis_id')
    else:
        print(f"Error: {result.get('error')}")
        return None

def test_download_report(analysis_id):
    """Test PDF download endpoint"""
    print(f"\n🔍 Testing /api/report/{analysis_id}/download...")
    
    response = requests.get(f"{BASE_URL}/api/report/{analysis_id}/download")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        # Save PDF
        pdf_path = f"test_report_{analysis_id}.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ PDF saved: {pdf_path}")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False

def main():
    print("=" * 60)
    print("🧪 QOFFEA BACKEND API TESTS")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("❌ Health check failed!")
        return
    
    # Test 2: Index
    if not test_index():
        print("❌ Index endpoint failed!")
        return
    
    # Test 3: Upload (you need to provide a test image)
    test_image = r"E:\ACOOLLYEAHHH\Qoffea\Qoffea\Frontend-Qoffea\Assets\coffe_beans.jpg"
    
    if not os.path.exists(test_image):
        print(f"\n⚠️  Test image not found: {test_image}")
        print("Please provide a valid coffee bean image path")
        return
    
    analysis_id = test_upload(test_image)
    
    if not analysis_id:
        print("❌ Upload test failed!")
        return
    
    # Test 4: Download PDF report
    if not test_download_report(analysis_id):
        print("❌ PDF download failed!")
        return
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
