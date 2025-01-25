from django.contrib import admin
from .models import Question
from .models import Answer

class QuestionA(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionA)
admin.site.register(Answer)