from django.shortcuts import render
from django.http import HttpResponse
from models import *
from datetime import datetime, timedelta


# Create your views here.
def index(request):
    # return HttpResponse('Welcome to DressCode!')
    # if request.user.is_authenticated():
    # return HttpResponseRedirect('/feed/')
    return render(request, 'dresscodeapp/base.html', {})


def post_question_page(request):
    return render(request, 'dresscodeapp/postquestion.html', {})


"""
def post_question(request):
    # check if user is eligible for a question
    fuser = Fuser.objects.get(user__username=request.user.username)
    if fuser.score < 10:
        # can't post a question - tell user to answer (10-score) more questions in order to post
        return HttpResponse('You are not eligible to post')
    fuser = Fuser.objects.get(user__username=request.user.username)
    question = Question(
        user=fuser,
        title='title',
        description='desc',
        photo_path='none',
        clothing_items=None
    )
    question.save()
    return HttpResponse('hooray!')
    """


# def post_question(request):
# check if user is eligible for a question
# fuser = Fuser.objects.get(user__username=request.user.username)
# if fuser.score < 10:
# can't post a question - tell user to answer (10-score) more questions in order to post
# pass
# else:

def filter_questions(request):
    clothingItems = [x[1] for x in ClothingItem.TYPES]
    colors = [x[1] for x in ClothingItem.COLORS]
    patterns = [x[1] for x in ClothingItem.PATTERN]
    genders = [x[1] for x in Fuser.GENDERS]
    return render(request, 'dresscodeapp/filterquestions.html',
                  {'clothingItems': clothingItems, 'colors': colors, 'patterns': patterns, 'genders': genders})


def question_page(request, q_pk):
    question = Question.objects.get(pk=q_pk)
    return render(request, 'dresscodeapp/question.html', {'question': question})


def post_answer(request):
    # check for spam: if user answered 10 questions in the past 10 seconds - kick his ass
    # spam_threshold = datetime.now() - timedelta(seconds=10)
    # recently_answered_by_user = Answer.objects.filter(published_date__gte=spam_threshold)
    # if len(recently_answered_by_user) > 9:
    # handle as spam (warning / log user out / kill user)
    # pass
    # continue as usual
    fuser = Fuser.objects.get(user__username=request.user.username)
    fuser.num_answers += 1
    fuser.score += 1
    vote = request.POST['vote']
    question_pk = request.POST['question_id']
    answer = Answer(vote=vote, question_id=question_pk, user=fuser)
    answer.save()
    fuser.save()
    return HttpResponse('succes')


def get_questions_feed(request):
    # get only questions from users who are not me, that i haven't answered to already, ordered from new to old, that are not overdue
    # maybe sort by increasing time from due date?
    curr_username = request.user.username
    answered_ids = [a.question_id for a in Answer.objects.filter(user__user__username=curr_username)]
    questions_feed = Question.objects.filter(due_date__gte=timezone.now()).exclude(user__user__username=curr_username)
    questions_feed = Question.objects.filter(pk__in=questions_feed).exclude(pk__in=answered_ids).order_by(
        '-published_date')[:2]
    return render(request, 'dresscodeapp/feed.html', {'questions': questions_feed})


def post_question(request):
    photo_path = request.POST.get('path')
    title = request.POST.get('title')
    description = request.POST.get('description')
    date = request.POST.get('date')#.join(" 23:59:59")
    date_time = (date+" 23:59:59").encode('ascii')
    date = datetime.strptime(date_time, '%m/%d/%Y %H:%M:%S')
    items_tmp = request.POST.get('items_lst')
    all_items = items_tmp.split("#")

    question = Question(
        user=Fuser.objects.get(user__username=request.user.username),
        title=title,
        description=description,
        photo_path=photo_path,
        due_date=date
    )
    question.save()
    q_id = Question.objects.filter(user__user__username=request.user.username).order_by('-published_date')[0].pk
    for item in all_items:
        sub_items = item.split(",")
        clothing_item = ClothingItem(color=sub_items[1].upper(), type=sub_items[0].upper(),
                                     pattern=sub_items[2].upper(), question_id=q_id)
        clothing_item.save()
        question.clothing_items.add(clothing_item)
        question.save()
    return HttpResponse('succes')
