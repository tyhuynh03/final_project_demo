# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy tệp requirements.txt vào thư mục làm việc của container
COPY requirements.txt .

# Install các gói thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ dự án vào thư mục làm việc của container
COPY . .
# reset db
RUN python manage.py flush --no-input

# Thực hiện migrations
RUN python manage.py makemigrations && \
    python manage.py migrate
#tạo tài khoản admin 
RUN echo "from users.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell


# Đảm bảo rằng tệp User.csv được sao chép vào đúng vị trí
COPY scripts/User.csv /app/scripts/User.csv
COPY scripts/Toiec.csv /app/scripts/Toiec.csv
# Đảm bảo rằng tệp User.csv được sao chép vào đúng vị trí trong container
# Thực thi script import_data
RUN python manage.py runscript import_data
RUN python manage.py runscript populate_data_from_csv



# Command để chạy ứng dụng của bạn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
