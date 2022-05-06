import pytest
from django.urls import reverse
from faker import Faker

from umbrella.conftest import reverse_with_params
from umbrella.tasks.models import Task
from umbrella.tasks.tests.factories import TaskFactory

fake = Faker()
pytestmark = pytest.mark.django_db


def test_task_list(client, task):
    url = reverse('task-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count']
    response_contract_data = response.data['results'][0]
    assert response_contract_data['id'] == str(task.id)


def test__task_list_ordering(client, task):
    another_task = TaskFactory()
    url = reverse_with_params('task-list', query_kwargs={"ordering": "-title"})
    response = client.get(url, format='json')
    assert response.status_code == 200
    response_contract_data = response.data['results'][0]
    assert response_contract_data['title'] == another_task.title


def test_task_detail(client, task):
    url = reverse('task-detail', args=[task.id])
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data["id"] == str(task.id)


def test_task_create(client, contract):
    url = reverse('task-list')
    data = {
        "contract": contract.id,
        "contract_clause_type": "Created task Test clause",
        "contract_business_intelligence_type": "Created task Test BI type",
        "link_to_contract_text": "created_task_test_link",
        "title": "Created Test task"
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 201
    assert Task.objects.count() == 1


def test_task_update(client, task):
    url = reverse('task-detail', args=[task.id])
    new_title = "Task New Title"
    data = {
        "title": new_title
    }
    response = client.patch(url, data=data, format='json')
    assert response.status_code == 200
    assert response.data["title"] == new_title


def test_task_delete(client, task):
    url = reverse('task-detail', args=[task.id])
    response = client.delete(url, format='json')
    assert response.status_code == 204
    assert Task.objects.count() == 0


def test_task_comment_create(client, task):
    url = reverse('tasks-comment-list', args=[task.id])
    message = "Test comment"
    data = {
        "message": message
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data["message"] == message
    assert response.data["task"] == task.id


def test_task_comment_delete(client, task, comment):
    url = reverse('tasks-comment-detail', args=[task.id, comment.id])
    response = client.delete(url, format='json')
    assert response.status_code == 204
