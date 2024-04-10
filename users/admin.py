# Register your models here.
from django.contrib import admin

from .models import User
from quiz.models import Topic



admin.site.register(User)
admin.site.register(Topic)