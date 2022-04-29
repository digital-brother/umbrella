import pytest
from django.urls import reverse
from faker import Faker

from umbrella.tasks.models import Task

fake = Faker()
pytestmark = pytest.mark.django_db


def test_task_list(client, task):
    url = reverse('task-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count']
    response_contract_data = response.data['results'][0]
    assert response_contract_data['id'] == str(task.id)


def test_task_create(client, contract):
    url = reverse('task-list')
    data = {
        "contract": contract.id,
        "contract_clause_type": "Test Clause",
        "contract_business_intelligence_type": "Test BI Type",
        "link_to_contract_text": "test_link",
        "title": "Test Task"
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
