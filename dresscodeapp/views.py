import json
import os

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpResponse

from models import *
from datetime import datetime

USER_SCORE_FOR_NEW_ANSWER = 1
USER_SCORE_FOR_NEW_QUESTION = 7
MIN_ANSWERS_TO_DETERMINE_SPAMMER = 3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def index(request):
    # return HttpResponse('Welcome to DressCode!')
    # if request.user.is_authenticated():
    # return HttpResponseRedirect('/feed/')
    return render(request, 'dresscodeapp/base.html', {})


def post_question_page(request):
    fuser = Fuser.objects.get(user__username=request.user.username)
    return render(request, 'dresscodeapp/postquestion.html', {'score': fuser.score})


def filter_questions_page(request):
    clothingItems = [x[1] for x in ClothingItem.TYPES]
    colors = [x[1] for x in ClothingItem.COLORS]
    patterns = [x[1] for x in ClothingItem.PATTERN]
    return render(request, 'dresscodeapp/filterquestions.html',
                  {'clothingItems': clothingItems, 'colors': colors, 'patterns': patterns})


def return_filtered_results(request):
    curr_username = request.user.username
    answered_ids = [a.question_id for a in Answer.objects.filter(user__user__username=curr_username)]
    questions_feed = Question.objects.filter(due_date__gte=timezone.now()).exclude(user__user__username=curr_username)
    questions_feed = Question.objects.filter(pk__in=questions_feed).exclude(pk__in=answered_ids)

    gender = request.POST.get('gender')
    list_by_gender = Fuser.objects.filter(gender=gender)
    questions_feed = Question.objects.filter(user__in=list_by_gender)
    items_tmp = request.POST.get('items_lst')
    all_items = items_tmp.split("#")

    for item in all_items:
        sub_items = item.split(",")
        # need to add filter by items
        for question in questions_feed:
            question_items = [val for val in question.clothing_items.all()]
            if sub_items not in question_items:
                questions_feed = Question.objects.exclude(pk=question.pk)
    questions_feed = Question.objects.order_by('-published_date')[:2]

    items_dict = {}
    for question in questions_feed:
        items_dict[question.pk] = []
    items_dict[question.pk] = [val for val in question.clothing_items.all()]
    return render(request, 'dresscodeapp/filteredresults.html', {'questions': questions_feed})


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
    answerer = Fuser.objects.get(user__username=request.user.username)
    answerer.num_answers += 1
    answerer.score += USER_SCORE_FOR_NEW_ANSWER
    vote = request.POST['vote']
    question_pk = request.POST['question_id']
    items_not_as_pic = request.POST.get('itemsNotAsPic')
    if items_not_as_pic == u'true':
        items_not_as_pic = True
    else:
        items_not_as_pic = False
    answer = Answer(vote=vote, question_id=question_pk, user=answerer, items_not_as_pic=items_not_as_pic)
    answer.save()
    answerer.save()
    find_spammer_by_answer(question_pk, answerer.id, vote)
    return HttpResponse('success')


def find_spammer_by_answer(question_id, answerer_name, vote):
    question = Question.objects.filter(pk=question_id)
    spammers = Fuser.objects.filter(spammer=True)
    answers_without_spammers = Answer.objects.filter(question_id=question_id).exclude(user__in=spammers)
    num_answers_items_not_as_pic = len(
        Answer.objects.filter(pk__in=answers_without_spammers).exclude(items_not_as_pic=False))
    num_answers_items = len(answers_without_spammers)
    if num_answers_items >= MIN_ANSWERS_TO_DETERMINE_SPAMMER:
        if num_answers_items / 2 + 1 < num_answers_items_not_as_pic:  # half the answerers think that question clothing items not as in pic
            # asker is spammer!
            update_spammer_credit(question[0].user.id)
            question.items_not_as_pic = True
        elif not question.items_not_as_pic:
            question.items_not_as_pic = False
        question[0].save()

        fit_vote = len(Answer.objects.filter(pk__in=answers_without_spammers, vote='1'))
        no_fit_vote = len(Answer.objects.filter(pk__in=answers_without_spammers, vote='2'))
        partial_fit_votes = num_answers_items - fit_vote - no_fit_vote

        curr_vote_num = partial_fit_votes
        if vote == '1':
            curr_vote_num = fit_vote
        elif vote == '2':
            curr_vote_num = no_fit_vote

        if curr_vote_num / float(num_answers_items) < 0.5:  # less than 10% think tha same as the answerer
            update_spammer_credit(answerer_name)


def update_spammer_credit(id):
    user = Fuser.objects.get(pk=id)
    user.spammer_credit += 1
    if user.spammer_credit >= 0.85 * (user.num_questions + user.num_answers):
        user.spammer = True
    user.save()


def get_questions_feed(request):
    curr_username = request.user.username
    answered_ids = [a.question_id for a in Answer.objects.filter(user__user__username=curr_username)]

    # user cant answer his own question, questions with past due date are irrelevant
    questions_feed = Question.objects.filter(due_date__gte=timezone.now()).exclude(user__user__username=curr_username)

    # we will not negotiate with terrorists!!
    questions_feed = Question.objects.filter(pk__in=questions_feed).exclude(user__spammer=True)
    questions_feed = Question.objects.filter(pk__in=questions_feed).exclude(items_not_as_pic=True)

    # user will not answer same question twice
    questions_feed = Question.objects.filter(pk__in=questions_feed).exclude(pk__in=answered_ids).order_by(
        '-published_date')[:2]
    return render(request, 'dresscodeapp/feed.html', {'questions': questions_feed})


def post_question(request):
    # upload image from user
    folder = os.path.join('dresscodeapp', 'static', 'user_images', request.user.username)
    uploaded_filename = request.FILES['photos'].name

    # create the folder if it doesn't exist.
    try:
        os.mkdir(os.path.join(BASE_DIR, folder))
    except:
        pass

    # save the uploaded file inside that folder.
    full_filename = os.path.join(BASE_DIR, folder, uploaded_filename)
    fout = open(full_filename, 'wb+')

    file_content = ContentFile(request.FILES['photos'].read())

    # Iterate through the chunks.
    for chunk in file_content.chunks():
        fout.write(chunk)
    fout.close()

    photo_path = os.path.join('user_images', request.user.username, uploaded_filename)
    title = request.POST.get('title')
    description = request.POST.get('description')
    date = request.POST.get('date')
    date_time = (date + " 23:59:59").encode('ascii')
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
    for item in all_items:
        sub_items = item.split(",")
        db_item = ClothingItem.objects.filter(color=sub_items[1].upper(), type=sub_items[0].upper(),
                                              pattern=sub_items[2].upper())
        if not db_item:
            db_item = ClothingItem(color=sub_items[1].upper(), type=sub_items[0].upper(),
                                   pattern=sub_items[2].upper())
            db_item.save()
            question.clothing_items.add(db_item)
        else:
            question.clothing_items.add(db_item[0].pk)
        question.save()

    user = Fuser.objects.get(user__username=request.user.username)
    user.score -= USER_SCORE_FOR_NEW_QUESTION
    user.save()
    return HttpResponse(json.dumps({'success': True}))


def get_results(request):
    curr_username = request.user.username
    # user cant answer his own question, questions with past due date are irrelevant
    questions_feed = Question.objects.filter(user__user__username=curr_username)

    return render(request, 'dresscodeapp/results.html', {'questions': questions_feed})


def view_result(request):
    question_pk = request.POST['question_id']
    gender = request.POST.get('gender')
    min = request.POST.get('minAge')
    max = request.POST.get('maxAge')
    if gender == "Female":
        gender = 'f'
    elif gender == "Male":
        gender = 'm'
    else:
        gender = 'u'

    return HttpResponse(
        json.dumps({'success': True, 'q_id': question_pk, 'gender': gender, 'minAge': min, 'maxAge': max}))


def view_question(request, q_pk):
    question = Question.objects.get(pk=q_pk)
    answers = Answer.objects.filter(question_id=q_pk)

    # we will not negotiate with terrorists!!
    answers = Answer.objects.filter(pk__in=answers).exclude(user__spammer=True)
    fit, no_fit, partial_fit = get_answers_rate(answers)

    return render(request, 'dresscodeapp/question-result.html',
                  {'question': question, 'fit': fit, 'no_fit': no_fit, 'partial_fit': partial_fit, 'filter': False})


def view_question_with_filters(request, q_pk, gender, minage, maxage):
    question = Question.objects.get(pk=q_pk)

    if gender == 'u' and minage == '0' and maxage == '0':
        return view_question(request, q_pk)

    if gender != 'u':
        relevant_users = Fuser.objects.filter(gender=gender)

    this_year = datetime.now().year
    minage = int(minage)
    maxage = int(maxage)
    max_year = this_year
    min_year = this_year

    if minage != 0:
        max_year = this_year - minage

    if maxage != 0:
        min_year = this_year - maxage
    else:
        min_year = 1900

    if minage != 0 and maxage != 0 and max_year < min_year:  # swap years, user got confused...
        tmp = min_year
        min_year = max_year
        max_year = tmp

    min_date = datetime(year=min_year, month=1, day=1)
    max_date = datetime(year=max_year, month=12, day=31)

    """
        exclude users from relevant_users by birthdate..
        can't find this field of user...
    """
    #if minage != 0:
       #relevant_users = Fuser.objects.filter(pk__in=relevant_users, gender=gender)

    answers = Answer.objects.filter(question_id=q_pk, user__in=relevant_users)

    # we will not negotiate with terrorists!!
    answers = Answer.objects.filter(pk__in=answers).exclude(user__spammer=True)
    fit, no_fit, partial_fit = get_answers_rate(answers)

    return render(request, 'dresscodeapp/question-result.html',
                  {'question': question, 'fit': fit, 'no_fit': no_fit, 'partial_fit': partial_fit, 'filter': True,
                   'gender': gender})


def get_answers_rate(answers):
    answers_fit = Answer.objects.filter(pk__in=answers, vote='1')
    answers_no_fit = Answer.objects.filter(pk__in=answers, vote='2')
    answers_partial_fit = Answer.objects.filter(pk__in=answers, vote='0')

    return len(answers_fit), len(answers_no_fit), len(answers_partial_fit)
