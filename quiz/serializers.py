from rest_framework import serializers
from .models import Question, Choice, Topic
from users.serializers import UserSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)  # Sử dụng ChoiceSerializer cho field 'choices'

    class Meta:
        model = Question
        fields = ['id', 'text', 'topic', 'choices']
class TopicSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.SerializerMethodField()  # Định nghĩa trường question_count
    username = serializers.SerializerMethodField()
    class Meta:
        model = Topic
        fields = ['id', 'name', 'questions' , 'question_count','username']
    def get_question_count(self, obj):
        # Trả về số lượng câu hỏi của chủ đề
        return obj.questions.count() 
    def get_username(self,obj):
        return obj.user.username
