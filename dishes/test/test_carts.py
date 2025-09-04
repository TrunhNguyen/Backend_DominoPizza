import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from dishes.models import Products, Cart

@pytest.mark.django_db
def test_carting_add_item():
    user = User.objects.create_user(username="testuser", password="12345")
    product = Products.objects.create(name="Pepperoni", price=100)
    client = APIClient()
    client.force_authenticate(user=user)  
    response = client.post(f"/api/carting/{product.id}")
    assert response.status_code == 200
    assert response.data["status"] == "success"
    assert response.data["cart"][0]["product"] == product.id

@pytest.mark.django_db
def test_uncarting_remove_item():
    user = User.objects.create_user(username="testuser2", password="12345")
    product = Products.objects.create(name="Cheese", price=80)
    cart_item = Cart.objects.create(user=user, product=product, quantity=2)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(f"/api/uncarting/{product.id}")
    assert response.status_code == 200
    assert response.data["cart"][0]["quantity"] == 1  

@pytest.mark.django_db
def test_deleteall_cart():
    user = User.objects.create_user(username="testuser3", password="12345")
    Products.objects.create(name="Veggie", price=90)
    Cart.objects.create(user=user, product_id=1, quantity=2)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete("/api/deletecart")
    assert response.status_code == 200
    assert Cart.objects.filter(user=user).count() == 0