import os
import tempfile

fd, path = tempfile.mkstemp(suffix='.db')
os.close(fd)
os.environ['DATABASE_URL'] = f'sqlite:///{path}'

from fastapi.testclient import TestClient
from app.main import app


def test_task_lifecycle():
    with TestClient(app) as client:
        assert client.get('/health').json() == {'status': 'ok'}
        created = client.post('/api/tasks', json={'title': 'Learn Docker'})
        assert created.status_code == 201
        task = created.json()
        assert task['title'] == 'Learn Docker'
        assert client.get('/api/tasks').json()[0]['id'] == task['id']
        updated = client.patch(f"/api/tasks/{task['id']}", json={'completed': True})
        assert updated.json()['completed'] is True
        assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
        assert client.get('/api/tasks').json() == []
