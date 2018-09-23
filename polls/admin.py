"""
管理画面のオブジェクト管理クラス
"""
from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """
    回答項目の構成を管理する
    model 表示するモデル
    extra 入力できる数
    """
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """
    質問入力画面の構成を管理する
    fieldsets 画面構成
    inlines　includeする設定
    list_display テーブルに表示するカラム
    list_filter　フィルターセットを出すカラム
    search_fields　検索対象のカラム
    """
    ## head, field
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
