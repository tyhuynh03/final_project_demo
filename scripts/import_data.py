import csv
from users.models import User

def run():
    csv_file_path = r'.\scripts\User.csv'  # Đường dẫn tới file CSV của bạn

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Bỏ qua dòng đầu tiên nếu nó chứa tiêu đề

        for row in reader:
            # Trích xuất thông tin từ mỗi dòng của file CSV
            username, email, password = row

            # Tạo người dùng mới
            user = User.objects.create_user(username=username, email=email, password=password)
            # Lưu người dùng vào cơ sở dữ liệu
            user.save()

if __name__ == "__main__":
    run()
