import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_employee():
    response = client.post(
        "/employees",
        json={
            "employee_id": "EMP001",
            "full_name": "Akshay Kumar",
            "email": "akshay@test.com",
            "department": "IT"
        }
    )

    assert response.status_code in [201, 400]

def test_get_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert isinstance(response.json(), list)