import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from dishes.models import Products, Cart

@pytest.mark.django_db
def test_carting_add_item():
    user = User.objects.create_user(username="testuser", password="12345")
    product = Products.objects.create(name="Pepperoni", price=100)
    client = APIClient()
    client.force_authenticate(user=user)  
    with patch("dishes.views.Cart.objects.get_or_create") as mock_get_or_create:
        mock_cart_item = MagicMock(quantity=1)
        mock_get_or_create.return_value = (mock_cart_item, True)
        response = client.post(f"/api/carting/{product.id}")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        mock_get_or_create.assert_called_once()

@pytest.mark.django_db
def test_uncarting_remove_item():
    user = User.objects.create_user(username="testuser2", password="12345")
    product = Products.objects.create(name="Cheese", price=80)
    cart_item = Cart.objects.create(user=user, product=product, quantity=2)
    client = APIClient()
    client.force_authenticate(user=user)
    with patch("dishes.views.Cart.objects.get") as mock_get:
        mock_cart_item = MagicMock(quantity=2)
        mock_get.return_value = mock_cart_item
        response = client.delete(f"/api/uncarting/{product.id}")
        assert response.status_code == 200
        mock_get.assert_called_once()
        assert mock_cart_item.quantity == 1 or mock_cart_item.delete.called

@pytest.mark.django_db
def test_deleteall_cart():
    user = User.objects.create_user(username="testuser3", password="12345")
    product = Products.objects.create(name="Veggie", price=90)
    Cart.objects.create(user=user, product=product, quantity=2)
    client = APIClient()
    client.force_authenticate(user=user)
    with patch("dishes.views.Cart.objects.filter") as mock_filter:
        mock_filter.return_value.delete.return_value = None
        response = client.delete("/api/deletecart")
        assert response.status_code == 200
        mock_filter.assert_called_once_with(user=user)
        mock_filter.return_value.delete.assert_called_once()

@pytest.mark.django_db
def test_view_cart_with_total():
    user = User.objects.create_user(username="testuser4", password="12345")
    p1 = Products.objects.create(name="Pepperoni", price=100)
    p2 = Products.objects.create(name="Cheese", price=80)
    Cart.objects.create(user=user, product=p1, quantity=2)  # 200
    Cart.objects.create(user=user, product=p2, quantity=1)  # 80
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/v2/cart")
    assert response.status_code == 200
    assert response.data["cart_total"] == 280
    assert len(response.data["cart"]) == 2