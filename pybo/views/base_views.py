from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question
from django.db.models import Q, Count

#import logging
#logger = logging.getLogger(__name__)

def index(request):
#   logger.info('INFO 레벨로 출력')
    page = request.GET.get('page','1')
    kw = request.GET.get('kw','');
    so = request.GET.get('so', 'recent');

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter = Count('voter')).order_by('-num_voter','-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer = Count('answer')).order_by('-num_answer','-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(question_list,10)
    page_obj = paginator.get_page(page)
    context = {'question_list' : page_obj, 'page':page, 'kw':kw, 'so':so}
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    #question = Question.objects.get(id=qid)
    question = get_object_or_404(Question, id =question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)