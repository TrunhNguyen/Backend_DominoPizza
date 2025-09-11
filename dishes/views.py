from .models import Products, Orders, Cart
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status
from .serializer import PizzaSerializers, OrderSerializers, CartSerializers, CartDetailSerializers, RegisterSerializers, CustomLoginSerializers
from django.contrib.auth.models import User  #model user có sẵn của django

"""
- Api_view: Biến hàm python thành REST API Endpoint
- Permission_classes: Check quyền
    AllowAny: ai cũng gọi được (không cần token)
    IsAuthenticated: chỉ user đăng nhập (token còn hạn)
    IsAdminUser: chỉ admin (user.is_staff = True)
    IsAuthenticatedOrReadOnly: GET cho ai cũng được, POST/PUT/DELETE thì cần đăng nhập
- Serializer: biến dữ liệu từ Model sang JSON
"""

#api thêm vào giỏ hàng
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def carting(request, id):
    dish = get_object_or_404(Products, id=id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=dish)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    mycart = Cart.objects.filter(user=request.user)
    serializer = CartSerializers(mycart, many=True)
    return Response({
        "status": "success",
        "message": f"Thêm {dish.name} to cart",
        "cart": serializer.data
    }, status=status.HTTP_200_OK)

#api xóa khỏi giỏ hàng
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def uncarting(request, id):
    dish = get_object_or_404(Products, id=id)
    try:
        cart_item = Cart.objects.get(user=request.user, product=dish)
    except Cart.DoesNotExist:
        return Response({
            "status": "error",
            "message": f"{dish.name} không có trong giỏ hàng"
        }, status=status.HTTP_400_BAD_REQUEST)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    mycart = Cart.objects.filter(user=request.user)
    serializer = CartSerializers(mycart, many=True)
    return Response({
        "status": "success",
        "message": f"Đã xoá {dish.name} khỏi giỏ hàng",
        "cart": serializer.data
    }, status=status.HTTP_200_OK)

#api xóa toàn bộ giỏ hàng
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteall(request):
    Cart.objects.filter(user=request.user).delete()
    return Response({
        "status": "success",
        "message": f"Đã xóa toàn bộ giỏ hàng của bạn"
    }, status=status.HTTP_200_OK)

#api đăng ký
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    serializer = RegisterSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#custom lại response của simplejwt trong login
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializers

#api đặt hàng
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return Response({
            "status": "error",
            "message": "Giỏ hàng của bạn đang trống"
        }, status=status.HTTP_400_BAD_REQUEST)
    for item in cart_items:
        Orders.objects.create(
            product=item.product,
            customer=request.user,
            quantity=item.quantity
        )
    cart_items.delete()
    myorders = Orders.objects.filter(customer=request.user).order_by('id')
    serializer = OrderSerializers(myorders, many=True)
    return Response({
        "status": "success",
        "message": "Món của bạn đang được chuẩn bị",
        "orders": serializer.data
    }, status=status.HTTP_200_OK)

#api xem giỏ hàng
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request, version):
    mycart = Cart.objects.filter(user=request.user) 
    if request.version == 'v1':
        serializer = CartSerializers(mycart, many=True) 
    elif request.version == 'v2':
        serializer = CartDetailSerializers(mycart, many=True)  #hiển thị product chi tiết
    else:
        return Response({"error": "API version này chưa được hỗ trợ"}, status=status.HTTP_400_BAD_REQUEST)
    cart_total = sum([item.quantity * item.product.price for item in mycart])
    return Response({
        "status": "success",
        "message": "Giỏ hàng của bạn:",
        "cart": serializer.data,
        "cart_total": cart_total
    }, status=status.HTTP_200_OK)

#api lấy thông tin sản phẩm với id
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def pizza_detail(request, id):
    try:
        pizza = Products.objects.get(id=id)
    except Products.DoesNotExist:
        return Response({'error': 'Không tìm thấy'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = PizzaSerializers(pizza)
    return Response(
        {"status": "success",
        "detail": serializer.data
    }, status=status.HTTP_200_OK)

#api lấy danh sách toàn bộ sản phẩm
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def pizza_list(request):
    pizza = Products.objects.all()
    serializer = PizzaSerializers(pizza, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#api lấy danh sách tất cả đơn hàng
@api_view(['GET'])
@permission_classes([IsAdminUser])
def order_list(request):
    orderlist = Orders.objects.all().order_by('order_time')
    paginator = PageNumberPagination()
    paginator.page_size = 2
    result_page = paginator.paginate_queryset(orderlist, request)
    serializer = OrderSerializers(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

#api xóa khỏi đơn hàng
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_order(request, id):
    order = get_object_or_404(Orders, id=id)
    order_id = order.id
    order.delete()
    return Response(
        {"status": "success", 
        "message": f"Order {order_id} đã bị xóa."
        }, status=status.HTTP_200_OK)

#api xóa hết đơn hàng
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_order_all(request):
    Orders.objects.all().delete()
    return Response (
        {"status": "success",
        "message": "Đã xóa tất cả đơn hàng hiện có"
        }, status=status.HTTP_200_OK)

#api thêm món vào list
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_dish(request):
    serializer = PizzaSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Thêm món thành công!", "dish": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#api xóa món khỏi list
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_dish(request, id):
    try:
        dish = Products.objects.get(id=id)
    except Products.DoesNotExist:
        return Response({"error": "Món không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    dish.delete()
    return Response({"message": "Xóa món thành công!"}, status=status.HTTP_200_OK)