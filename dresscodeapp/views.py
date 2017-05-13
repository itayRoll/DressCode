import json
import os

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from models import *
from datetime import datetime, timedelta

SPAM_SECONDS_GAP = 10
SPAM_ANSWERS_GAP = 10
USER_SCORE_FOR_NEW_ANSWER = 1
USER_SCORE_FOR_NEW_QUESTION = 7
MIN_ANSWERS_TO_DETERMINE_SPAMMER = 3
MIN_ANSWERS_TO_DETERMINE_SIMILAR_USER = 3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def index(request):
    # passed validations
    if request.user.is_authenticated():
        return HttpResponseRedirect('/questionsfeed/')
    return render(request, 'dresscodeapp/base.html', {})


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['uname']
        password = request.POST['psw']
        next_page = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if Fuser.objects.get(user__username=user.username).spammer:
                    # logged in user is a spammer!
                    pass
                if next_page != '':
                    return HttpResponseRedirect(next_page)
                return HttpResponseRedirect('/questionsfeed/')
    return render(request, 'dresscodeapp/base.html')


def signup_user(request):
    logout(request)
    if request.POST:
        username = request.POST['uname']
        password = request.POST['psw']
        confirm_password = request.POST['confirm-psw']
        if not password == confirm_password:
            return HttpResponseRedirect('/home/')
        email = request.POST['email']
        gender = request.POST['gender']
        if gender == 'gender':
            gender = 'u'
        else:
            gender = gender[:1].lower()
        dob = request.POST['dob']
        try:
            # user is already in the system
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username=username, email=email, password=password)
            fuser = Fuser(user=user, gender=gender, dob=datetime.strptime(dob, "%m/%d/%Y").date())
            fuser.save()
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect('/initial-feed/')
    return HttpResponseRedirect('/questionsfeed/')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/home/')


@login_required(login_url='/home/')
def post_question_page(request):
    # passed validations
    fuser = Fuser.objects.get(user__username=request.user.username)
    return render(request, 'dresscodeapp/postquestion.html', {'score': fuser.score})


@login_required(login_url='/home/')
def filter_questions_page(request):
    # passed validations
    clothingItems = [x[1] for x in ClothingItem.TYPES]
    colors = [x[1] for x in ClothingItem.COLORS]
    patterns = [x[1] for x in ClothingItem.PATTERN]
    return render(request, 'dresscodeapp/filterquestions.html',
                  {'clothingItems': clothingItems, 'colors': colors, 'patterns': patterns})


@login_required(login_url='/home/')
def return_filtered_results(request):
    curr_username = request.user.username
    gender = request.POST.get('gender')
    all_items = request.POST.get('items_lst').split("#")
    items_lst = []
    if all_items != [u'']:
        for item_str in all_items:
            n, c, p = item_str.split(',')
            items_lst.append(ClothingItem(type=n, color=c, pattern=p))
    answered_ids = [a.question_id for a in
                    Answer.objects.filter(user__user__username=curr_username)]  # questions answered by user

    # retrieve questions answered by specified gender, from future, not asked by user nor answered by him
    questions_feed = [q for q in Question.objects.filter(user__gender=gender,
                                                         due_date__gte=timezone.now()).exclude(
        user__user__username=curr_username).order_by('-published_date')[:2] if q.pk not in answered_ids
                      and any([it in q.clothing_items.all() for it in items_lst])]
    return render(request, 'dresscodeapp/filteredresults.html', {'questions': questions_feed})


@login_required(login_url='/home/')
def question_page(request, q_pk):
    question = Question.objects.get(pk=q_pk)
    return render(request, 'dresscodeapp/question.html', {'question': question})


@login_required(login_url='/home/')
def post_answer(request):
    # check for spam: if user answered 10 questions in the past 10 seconds - kick his ass
    curr_username = request.user.username
    spam_threshold = datetime.now() - timedelta(seconds=SPAM_SECONDS_GAP)
    recently_answered_by_user = Answer.objects.filter(published_date__gte=spam_threshold,
                                                      user__user__username=curr_username)
    if len(recently_answered_by_user) > SPAM_ANSWERS_GAP:
        # handle as spam (warning / log user out / kill user)
        pass
    # continue as usual
    answerer = Fuser.objects.get(user__username=curr_username)
    answerer.num_answers += 1
    answerer.score += USER_SCORE_FOR_NEW_ANSWER
    vote = request.POST['vote']
    question_pk = request.POST['question_id']
    items_not_as_pic = request.POST.get('itemsNotAsPic') == u'true'
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

        if curr_vote_num / float(num_answers_items) < 0.1:  # less than 10% think tha same as the answerer
            update_spammer_credit(answerer_name)


def update_spammer_credit(name):
    fuser = Fuser.objects.get(user__username=name)
    fuser.spammer_credit += 1
    if fuser.spammer_credit >= 0.85 * (fuser.num_questions + fuser.num_answers):
        fuser.spammer = True
    fuser.save()


@login_required(login_url='/home/')
def get_questions_feed(request):
    curr_username = request.user.username
    answered_ids = [a.question_id for a in Answer.objects.filter(user__user__username=curr_username)]
    questions_feed = [q for q in
                      [q for q in Question.objects.filter(is_system_question=True)] if q.pk not in answered_ids]
    if len(questions_feed) != 0:
        return HttpResponseRedirect('/initial-feed/')


    # user cant answer his own question, questions with past due date are irrelevant, spammers are excluded
    questions_feed = [q for q in Question.objects.filter(due_date__gte=timezone.now()).exclude(
        user__user__username=curr_username).order_by(
        'due_date')[:5] if not q.user.spammer and not q.items_not_as_pic and not q.pk in answered_ids]
    return render(request, 'dresscodeapp/feed.html', {'questions': questions_feed})

@login_required(login_url='/home/')
def get_initial_feed(request):
    curr_username = request.user.username
    answered_ids = [a.question_id for a in Answer.objects.filter(user__user__username=curr_username)]

    # user cant answer his own question, questions with past due date are irrelevant, spammers are excluded
    questions_feed = [q for q in
                      [q for q in Question.objects.filter(is_system_question=True)] if q.pk not in answered_ids]
    if len(questions_feed) == 0:
        return HttpResponseRedirect('/questionsfeed/')
    else:
        return render(request, 'dresscodeapp/initial_feed.html', {'questions': questions_feed})


@login_required(login_url='/home/')
def post_question(request):
    # upload image from user
    folder = os.path.join('dresscodeapp', 'static', 'user_images', request.user.username)
    uploaded_filename = request.FILES['photos'].name

    # create the folder if it doesn't exist.
    try:
        os.makedirs(os.path.join(BASE_DIR, folder))
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
        due_date=date,
        is_system_question=False,
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
        else:
            db_item = db_item[0]
        question.clothing_items.add(db_item)
        question.save()

    user = Fuser.objects.get(user__username=request.user.username)
    user.score -= USER_SCORE_FOR_NEW_QUESTION
    user.save()
    return HttpResponse(json.dumps({'success': True}))


@login_required(login_url='/home/')
def get_results(request):
    curr_username = request.user.username
    # user cant answer his own question, questions with past due date are irrelevant
    questions_feed = Question.objects.filter(user__user__username=curr_username)

    return render(request, 'dresscodeapp/results.html', {'questions': questions_feed})

@login_required(login_url='/home/')
def get_profile(request):
    curr_username = request.user.username
    fuser = Fuser.objects.get(user__username=curr_username)
    return render(request, 'dresscodeapp/userprofile.html',{'user':fuser})


@login_required(login_url='/home/')
def view_result(request):
    question_pk = request.POST['question_id']
    gender = request.POST.get('gender')
    min_age = request.POST.get('minAge')
    max_age = request.POST.get('maxAge')
    if gender == "Female":
        gender = 'f'
    elif gender == "Male":
        gender = 'm'
    else:
        gender = 'u'

    return HttpResponse(
        json.dumps({'success': True, 'q_id': question_pk, 'gender': gender, 'minAge': min_age, 'maxAge': max_age}))


@login_required(login_url='/home/')
def view_question(request, q_pk):
    question = Question.objects.get(pk=q_pk)
    answers = Answer.objects.filter(question_id=q_pk)
    similar_users_answers = Answer.objects.filter(question_id=q_pk,
                                                  user__in=get_similar_users(list(Fuser.objects.all()),
                                                                             request.user.username))

    # we will not negotiate with terrorists!!
    answers = Answer.objects.filter(pk__in=answers).exclude(user__spammer=True)
    similar_users_answers = Answer.objects.filter(pk__in=similar_users_answers).exclude(user__spammer=True)
    fit, no_fit, partial_fit = get_answers_rate(answers)
    s_fit, s_no_fit, s_partial_fit = get_answers_rate(similar_users_answers)

    return render(request, 'dresscodeapp/question-result.html',
                  {'question': question, 'fit': fit, 'no_fit': no_fit, 'partial_fit': partial_fit,
                   's_fit': s_fit, 's_no_fit': s_no_fit, 's_partial_fit': s_partial_fit, 'filter': False})


@login_required(login_url='/home/')
def view_question_with_filters(request, q_pk, gender, minage, maxage):
    filter_text = get_filter_text(gender, minage, maxage)
    relevant_users = None
    question = Question.objects.get(pk=q_pk)

    if gender == 'u' and minage == '0' and maxage == '0':
        return view_question(request, q_pk)

    if gender != 'u':
        relevant_users = Fuser.objects.filter(gender=gender)

    this_year = datetime.now().year
    minage = int(minage)
    maxage = int(maxage)
    max_year = this_year

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
    if minage != 0 or maxage != 0:
        if relevant_users is None:
            relevant_users = Fuser.objects.filter(dob__gte=min_date, dob__lte=max_date)
        else:
            relevant_users = Fuser.objects.filter(pk__in=relevant_users, dob__gte=min_date, dob__lte=max_date)

    answers = Answer.objects.filter(question_id=q_pk, user__in=relevant_users)
    similar_users_answers = Answer.objects.filter(question_id=q_pk, user__in=get_similar_users(relevant_users, request.user.username))

    # we will not negotiate with terrorists!!
    answers = Answer.objects.filter(pk__in=answers).exclude(user__spammer=True)
    similar_users_answers = Answer.objects.filter(pk__in=similar_users_answers).exclude(user__spammer=True)
    fit, no_fit, partial_fit = get_answers_rate(answers)
    s_fit, s_no_fit, s_partial_fit = get_answers_rate(similar_users_answers)

    return render(request, 'dresscodeapp/question-result.html',
                  {'question': question, 'fit': fit, 'no_fit': no_fit, 'partial_fit': partial_fit,
                   's_fit': s_fit, 's_no_fit': s_no_fit, 's_partial_fit': s_partial_fit,
                   'filter': True, 'filter_text': filter_text})


def get_filter_text(gender, minage, maxage):
    filter_text = ""
    minage = int(minage)
    maxage = int(maxage)

    if gender != 'u':
        if gender == 'f':
            filter_text = "Female"
        else:
            filter_text = "Male"

    if minage != 0 and maxage != 0 and minage > maxage:
        if filter_text == "":
            filter_text = "Minimum age: " + str(maxage) + ", Maximum age: " + str(minage)
        else:
            filter_text = filter_text + "Minimum age: " + str(maxage) + ", Maximum age: " + str(minage)
    else:
        if minage != 0:
            if filter_text == "":
                filter_text = "Minimum age: " + str(minage)
            else:
                filter_text = filter_text + ", Minimum age: " + str(minage)

        if maxage != 0:
            if filter_text == "":
                filter_text = "Maximum age: " + str(maxage)
            else:
                filter_text = filter_text + ", Maximum age: " + str(maxage)

    return filter_text


def get_answers_rate(answers):
    answers_fit = Answer.objects.filter(pk__in=answers, vote='1')
    answers_no_fit = Answer.objects.filter(pk__in=answers, vote='2')
    answers_partial_fit = Answer.objects.filter(pk__in=answers, vote='0')

    return len(answers_fit), len(answers_no_fit), len(answers_partial_fit)


def get_similar_users(users, curr_username):
    similar_users = []
    akser_answers = dict((a.question_id, int(a.vote)) for a in Answer.objects.filter(user__user__username=curr_username))
    for user in users:
        if user.user.username == curr_username:
            continue
        user_answers = dict((a.question_id, int(a.vote)) for a in Answer.objects.filter(user=user))
        similar_questions = list(set(akser_answers.keys()).intersection(user_answers.keys()))
        same_rate = 0
        similar_rate = 0
        total_questions = float(len(similar_questions))
        if total_questions >= MIN_ANSWERS_TO_DETERMINE_SIMILAR_USER:
            for question_id in similar_questions:
                if akser_answers[question_id] == user_answers[question_id]:
                    same_rate += 1
                # means someone vote maybe and the other voted yes or no
                elif akser_answers[question_id] == 0 or user_answers[question_id] == 0:
                    similar_rate += 1

            if ((same_rate / total_questions) + 0.5 * (similar_rate / total_questions)) >= 0.51:
                similar_users.append(user)

    return similar_users
