from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_legal_consultation():
    response = client.post('/api/legal/consult', json={
        "text": "劳动合同纠纷",
        "case_type": "民事"
    })
    assert response.status_code == 200
    assert 'event' in response.text