"""
管理画面のオブジェクト管理クラス
"""
from django.contrib import admin

from .models import Question
# Register your models here.

admin.site.register(Question)