---
name: pytest-testing
description: Generates production-grade pytest tests in Python with fixtures, parametrize, markers, mocking, and conftest patterns
---

# Pytest Testing Skill

## Overview

Use this skill when designing, writing, or refactoring unit and integration tests for Python and Django applications.

## Core Patterns

### 1. Pytest with Django
```python
import pytest
from django.urls import reverse
from destinations.models import Destination

@pytest.mark.django_db
class TestDestinations:
    def test_destination_list_view(self, client):
        url = reverse('destinations:list')
        response = client.get(url)
        assert response.status_code == 200

    def test_destination_creation(self):
        destination = Destination.objects.create(
            name="Ganpatipule Beach",
            category="Beach"
        )
        assert destination.name == "Ganpatipule Beach"
```

### 2. Parametrization
```python
@pytest.mark.parametrize("input_val,expected", [
    ("valid_slug", True),
    ("", False),
    ("invalid slug!", False),
])
def test_slug_validation(input_val, expected):
    assert validate_slug(input_val) == expected
```

### 3. Fixtures and Mocking
```python
@pytest.fixture
def sample_user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="secretpassword"
    )

def test_authenticated_review(client, sample_user):
    client.force_login(sample_user)
    response = client.post('/reviews/add/', {'rating': 5, 'comment': 'Great place!'})
    assert response.status_code in [200, 302]
```
