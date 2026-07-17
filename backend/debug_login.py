import traceback
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

try:
    response = client.post('/api/auth/login', json={'email':'test@example.com','password':'secret123'})
    print('STATUS', response.status_code)
    print(response.text)
except Exception:
    traceback.print_exc()
