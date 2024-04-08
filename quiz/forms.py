from django import forms
from .models import Question, Choice, Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class QuestionForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    
    class Meta:
        model = Question
        fields = ['text', 'topic']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

CHOICE_COUNT = 4  # Số lượng đáp án cho mỗi câu hỏi

class BaseChoiceFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseChoiceFormSet, self).__init__(*args, **kwargs)
        self.extra = CHOICE_COUNT

ChoiceFormSet = forms.inlineformset_factory(Question, Choice, form=ChoiceForm, extra=CHOICE_COUNT, can_delete=False, formset=BaseChoiceFormSet)
