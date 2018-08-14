from django.db import models

# Create your models here.
# データベースのレイアウトです

# modelはmodels.Modelのサブクラスとして作成します
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # 第一引数には人間用の説明を含められる（省略可能）
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    # 外部キーでリレーションしてる。Question : Choice 多対１
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)