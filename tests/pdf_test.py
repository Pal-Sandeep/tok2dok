from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_upload_pdf_api():
    with open(r"C:\Users\Rentit\Downloads\Report.pdf", "rb") as f:
        response = client.post("/pdf/upload/", files={"file": ("Report.pdf", f, "application/pdf")})
    print(response.text)
    assert response.status_code == 200
    print(response.json())
