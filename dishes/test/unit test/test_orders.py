import pytest
from unittest.mock import patch, MagicMock
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
    with patch("dishes.views.Orders.objects.create") as mock_create, \
         patch("dishes.views.Cart.objects.filter") as mock_cart_filter:
        mock_cart_item = MagicMock(product=product, quantity=2)
        mock_cart_qs = MagicMock()
        mock_cart_qs.__iter__.return_value = [mock_cart_item]  
        mock_cart_qs.delete = MagicMock()  
        mock_cart_filter.return_value = mock_cart_qs
        response = client.post("/api/order")
        assert response.status_code == 200
        assert response.data["status"] == "success"
        mock_create.assert_called() 
        mock_cart_filter.return_value.delete.assert_called_once()

@pytest.mark.django_db
def test_place_order_empty_cart():
    user = User.objects.create_user(username="emptyuser", password="12345")
    client = APIClient()
    client.force_authenticate(user=user)
    with patch("dishes.views.Cart.objects.filter") as mock_filter:
        mock_filter.return_value.exists.return_value = False
        response = client.post("/api/order")
        assert response.status_code == 400
        assert response.data["status"] == "error"