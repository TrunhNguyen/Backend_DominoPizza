import pytest
from unittest.mock import patch
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from dishes.models import Products, Cart, Orders

@pytest.mark.django_db
def test_place_order_success():
    user = User.objects.create_user(username="orderuser", password="12345")
    product = Products.objects.create(name="Hawaiian", price=120)
    Cart.objects.create(user=user, product=product, quantity=2)
    client = APIClient()
    client.force_authenticate(user=user)
    with patch("dishes.views.Orders.objects.create") as mock_create:
        response = client.post("/api/order")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert mock_create.call_count == 1
@pytest.mark.django_db
def test_place_order_empty_cart():
    user = User.objects.create_user(username="emptyuser", password="12345")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post("/api/order")
    assert response.status_code == 400
    assert response.data["status"] == "error"