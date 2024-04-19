# final_project_demo
- Để sử dụng đầu tiên chúng ta cần cài đặt Django_extensions bằng lệnh: "pip install django_extensions"
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runscript import_data
- python manage.py runscript populate_data_from_csv
- Chạy 4 lệnh trên để tạo dữ liệu 
- Để sử dụng chức năng quản lý của admin thì mọi người tạo tài khoản admin bằng python manage.py createsuperuser 
sau đó đăng nhập bình thường sẽ vào được trang admin 
- Đã thêm file script.sql để khi người khác vào làm có thể làm trên database ban đầu. Để dùng thì cần cài extentions SQLite. Mở file và chọn run select query tùy vào câu lệnh người trước để lại để xóa data dùng để test

# Docker 
- Mọi người phải cài docker trước mới test được cái này nhé
- chạy lệnh docker-compose up --build
- web được chạy trên http://localhost:8000/
