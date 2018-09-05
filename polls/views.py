"""
contollerクラス
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

class IndexView(generic.ListView):
    """
    初期表示
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    """
    詳細画面
    """
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    """
    結果画面
    """
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    """
    投票処理
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"投票する答えを選んでください",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
