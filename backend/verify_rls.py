import requests
import os

BASE_URL = "http://localhost:8000"
TEST_PDF_PATH = "test.pdf"
USER_ID = "123e4567-e89b-12d3-a456-426614174000"  # Valid UUID

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Health check passed")
        else:
            print(f"Health check failed: {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_upload_book():
    if not os.path.exists(TEST_PDF_PATH):
        print(f"Test file {TEST_PDF_PATH} not found")
        return

    files = {'file': open(TEST_PDF_PATH, 'rb')}
    headers = {'X-User-ID': USER_ID}
    
    try:
        response = requests.post(f"{BASE_URL}/books", files=files, headers=headers)
        if response.status_code == 200:
            book = response.json()
            print(f"Book upload successful. Book ID: {book['id']}")
            print(f"Book Title: {book['title']}")
            # We can't verify owner_id in response because we didn't add it to the response model
            # But if this succeeds, it means the DB insert worked (or at least didn't crash on unknown column)
        else:
            print(f"Book upload failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Book upload failed: {e}")

if __name__ == "__main__":
    test_health()
    test_upload_book()
