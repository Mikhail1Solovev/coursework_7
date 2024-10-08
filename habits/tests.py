import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username, password):
        return User.objects.create_user(username=username, password=password)
    return _create_user

@pytest.fixture
def create_habit(create_user):
    def _create_habit(user, action, place, time):
        return Habit.objects.create(user=user, action=action, place=place, time=time)
    return _create_habit

# Test for habit creation
def test_create_habit(api_client, create_user):
    user = create_user("testuser", "password123")
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/habits/", {
        "action": "Read a book",
        "place": "Home",
        "time": "18:00:00"
    })
    assert response.status_code == 201
    assert response.data["action"] == "Read a book"

# Test for habit list pagination
def test_habit_pagination(api_client, create_user, create_habit):
    user = create_user("testuser", "password123")
    api_client.force_authenticate(user=user)
    for i in range(10):
        create_habit(user, f"Habit {i}", "Home", "18:00:00")
    response = api_client.get("/api/habits/?page=1")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5