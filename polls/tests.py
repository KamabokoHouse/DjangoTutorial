"""
テストクラス
"""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

def create_question(question_text, days):
    """
    新しいquestionを作成します
    @param question_text 質問文
    @param days 作成日付
    @return new_question 質問
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    """
    QuestionModelのテストケース
    """
    def test_was_published_recently_with_future_question(self):
        """
        AC : pub_dateが未来日付の場合はfalseを返すこと
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        AC : 昨日より前の場合はfalseを返すこと
        """
        older_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=older_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        AC : 今日の場合はtrueを返すこと
        """
        recent_time = timezone.now()
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionViewTests(TestCase):
    """
    QuestionViewのテストケース
    """
    def test_no_questions(self):
        """
        AC : 質問がないときメッセージが表示されること
             ステータスコードが200であること
             responceが空であること
        """
        responce = self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, "有効な質問ではありません")
        self.assertQuerysetEqual(responce.context['latest_question_list'], [])
        
    def test_past_questions(self):
        """
        AC : 過去の質問が表示されること
        """
        create_question(question_text="past question.",days=-30)
        responce = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            responce.context['latest_question_list'],
             ['<Question: past question.>']
        )

    def test_future_question(self):
        """
        AC : 未来の質問が表示されないこと
        """
        create_question(question_text="past question.",days=30)
        responce = self.client.get(reverse('polls:index'))
        self.assertContains(responce, "有効な質問ではありません")
        self.assertQuerysetEqual(responce.context['latest_question_list'], [])

class QuestionDetailViewTests(TestCase):
    """
    QuestionModelのテストケース
    """
    def test_future_question(self):
        """
        AC :  未来日付の場合404が返されること
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        AC :  過去日付の場合表示されること
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)



