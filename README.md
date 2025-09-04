🔑 API Endpoints chính
Auth

POST /api/register/ – Đăng ký

POST /api/login/ – Đăng nhập (JWT)

Pizza

GET /api/pizzas/ – Danh sách Pizza

GET /api/pizzas/<id>/ – Chi tiết Pizza

Cart

POST /api/cart/add/<id>/ – Thêm Pizza vào giỏ

POST /api/cart/remove/<id>/ – Xóa 1 Pizza khỏi giỏ

POST /api/cart/clear/ – Xóa toàn bộ giỏ

GET /api/cart/ – Xem giỏ hàng

Orders

POST /api/orders/place/ – Đặt hàng

GET /api/orders/ – (Admin) Danh sách đơn hàng

POST /api/orders/delete/<id>/ – (Admin) Xóa đơn hàng

🛠️ Ghi chú

File cấu hình DB nằm trong settings.py, mặc định dùng SQLite. Nếu muốn dùng PostgreSQL thì chỉnh lại DATABASES.

API có phân quyền bằng permission_classes:

AllowAny → ai cũng gọi được

IsAuthenticated → yêu cầu đăng nhập

IsAdminUser → chỉ admin được phép
