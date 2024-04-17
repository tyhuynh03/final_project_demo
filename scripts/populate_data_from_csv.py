# populate_data_from_csv.py

import csv
import os
import django

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project_demo.auth.settings")
django.setup()

from quiz.models import Topic, Question, Choice

def run():
    csv_file_path ="./scripts/Toiec.csv"   # Đường dẫn tới file CSV của bạn


    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            topic_name = row[0]
            question_text = row[1]
            choices = row[2:]

            # Kiểm tra xem chủ đề đã tồn tại chưa, nếu không thì tạo mới
            topic, created = Topic.objects.get_or_create(name=topic_name)

            # Tạo câu hỏi và liên kết với chủ đề tương ứng
            question = Question.objects.create(text=question_text, topic=topic)

            # Tạo các lựa chọn cho câu hỏi
            for i in range(0, len(choices), 2):
                choice_text = choices[i]
            # Kiểm tra xem còn đủ phần tử trong danh sách choices để truy cập
                if i + 1 < len(choices):
                    is_correct = choices[i + 1].lower() == 'true'
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
                else:
        # Xử lý trường hợp không đủ phần tử trong choices
                    print("Lỗi: Không đủ phần tử trong danh sách choices")

    print('Dữ liệu đã được nhập thành công từ file CSV.')

if __name__ == '__main__':
    run()
