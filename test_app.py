import pytest
import json
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_home_page(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Task Manager API' in data['message']

def test_get_tasks_empty(client):
    """Test getting tasks when none exist"""
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 0

def test_create_task(client):
    """Test creating a new task"""
    response = client.post('/tasks', 
                          json={'title': 'Learn CI/CD'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Learn CI/CD'
    assert data['completed'] == False

def test_create_task_missing_title(client):
    """Test error when title missing"""
    response = client.post('/tasks', json={})
    assert response.status_code == 400

def test_delete_task(client):
    """Test deleting a task"""
    # First create a task
    create_response = client.post('/tasks', json={'title': 'Delete me'})
    task_id = json.loads(create_response.data)['id']
    
    # Then delete it
    delete_response = client.delete(f'/tasks/{task_id}')
    assert delete_response.status_code == 200

def test_delete_nonexistent_task(client):
    """Test deleting task that doesn't exist"""
    response = client.delete('/tasks/999')
    assert response.status_code == 404

def test_sample():
    assert 1 + 1 == 2