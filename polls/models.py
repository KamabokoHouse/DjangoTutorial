"""
モデルクラス
"""
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
# データベースのレイアウトです

# modelはmodels.Modelのサブクラスとして作成します
class Question(models.Model):
    """
    questionモデル
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        """
        昨日と今日の場合、trueを返す
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    """
    Choceモデル
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        """
        テキストを返します
        """
        return self.choice_text
