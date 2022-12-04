from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import (AskQuestionForm, AvatarForm, CreateAnswerForm,
                    SettingsForm, SignUpForm, TagForm)
from .library import popular_answers, popular_questions
# Create your views here.
from .models import (AnswerVote, Avatar, CreateAnswer, CreateQuestion,
                     QuestionVote)


def home(request):
    if request.user.is_authenticated and 'searchField' in request.GET.keys() \
            and request.GET['searchField']:
        return HttpResponseRedirect(
            f"/query?searchField={request.GET['searchField']}")

    else:
        questions = popular_questions()
        paginator = Paginator(questions, 20)  # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return search_html(request, "question/home.html",
                           {"page_obj": page_obj})


def search_html(request, template, context):
    try:
        avatar = Avatar.objects.get(user_id=request.user)
    except Exception:
        avatar = Avatar()
        avatar.image = 'profile-icon-empty.png'
    context["avatar"] = avatar
    question_list = popular_questions()
    context["trending"] = question_list
    context["is_trending"] = True
    if question_list.count() == 0:
        context["is_trending"] = False
    return render(request, template, context)


@login_required
def list_questions(request):
    questions = popular_questions()
    return render(request, "question/list.html", {"form": questions})


def show_question(request, question_id):
    question = CreateQuestion.objects.get(pk=question_id)
    list_answers = popular_answers(question)
    question_unlike = False
    question_like = False
    try:
        count_question_like = QuestionVote.objects.filter(
            question=question,
            type_id=QuestionVote.QuestionVoteType.APPROVE).count()
    except Exception:
        count_question_like = 0
    try:
        count_question_unlike = QuestionVote.objects.filter(
            question=question,
            type_id=QuestionVote.QuestionVoteType.CONDEMN).count()
    except Exception:
        count_question_unlike = 0
    if request.method == 'GET':
        try:
            question_vote = QuestionVote.objects.get(author=request.user,
                                                     question=question)
            if question_vote.type_id == QuestionVote.QuestionVoteType.CONDEMN:
                question_unlike = True
            elif question_vote.type_id == \
                    QuestionVote.QuestionVoteType.APPROVE:
                question_like = True
        except Exception:
            pass

    if request.method == 'POST':
        if 'question_like' in request.POST:
            try:
                question_vote = QuestionVote.objects.get(author=request.user,
                                                         question=question)
                question_vote.type_id = \
                    QuestionVote.QuestionVoteType.INDIFFERENCE
                if request.POST['question_like'] == 'unlike':
                    question_vote.type_id = \
                        QuestionVote.QuestionVoteType.CONDEMN
                    question_unlike = True
                if request.POST['question_like'] == 'like':
                    question_vote.type_id = \
                        QuestionVote.QuestionVoteType.APPROVE
                    question_like = True
                question_vote.save()
            except Exception:
                if request.method == 'POST':
                    if request.POST['question_like'] == 'unlike':
                        question_vote = QuestionVote(
                            author=request.user,
                            question=question,
                            type_id=QuestionVote.QuestionVoteType.CONDEMN
                        )
                        question_vote.save()
                    elif request.POST['question_like'] == 'like':
                        question_vote = QuestionVote(
                            author=request.user,
                            question=question,
                            type_id=QuestionVote.QuestionVoteType.APPROVE
                        )
                        question_vote.save()
        if "description" in request.POST:
            answer_form = CreateAnswerForm(request.POST)
            if answer_form.is_valid():
                answer = CreateAnswer(author=request.user,
                                      description=request.POST['description'],
                                      question=question)
                answer.save()
                subject = f"There is new answer for /question/ {question_id}"
                body = f"""
                author:{request.user.username}
        send new answer:
        {request.POST['description'][:120]}
        for your question:
        {question.title[:120]}
        {question.description[:120]}
        """
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=None,
                    recipient_list=[question.author.email], fail_silently=False
                )
        return HttpResponseRedirect(f"/question/{question_id}")
    answer_form = CreateAnswerForm()
    paginator = Paginator(list_answers, 30)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return search_html(request,
                       "question/show_question.html",
                       {"question": question,
                        "answer_form": answer_form,
                        "page_obj": page_obj,
                        "question_unlike": question_unlike,
                        "question_like": question_like,
                        "count_question_like": count_question_like,
                        "count_question_unlike": count_question_unlike
                        })


@login_required
def list_queried_tags(request):
    if 'name' in request.GET:
        questions = CreateQuestion.objects.filter(
            tag__tag=request.GET['name'])
        if questions.count() == 0:
            return render(request, "question/not_found.html",
                          {"query_word": request.GET['searchField']})
        return search_html(request, "question/list.html",
                           {"form": questions})
    return search_html(request, "question/not_found.html",
                       {"query_word": 'this'})


@login_required
def list_queried_questions(request):
    questions = CreateQuestion.objects.filter(
        title__contains=request.GET['searchField'])
    if questions.count() == 0:
        return search_html(request, "question/not_found.html",
                           {"query_word": request.GET['searchField']})
    return search_html(request, "question/list.html",
                       {"form": questions})


@login_required
def ask_question(request):
    if request.method == 'GET':
        form = AskQuestionForm()
        tag_form = TagForm()
        template_name = "question/ask_question.html"
        questions = popular_questions()
        paginator = Paginator(questions, 20)  # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return search_html(request, template_name,
                           {'form': form, 'tag_form': tag_form,
                            "page_obj": page_obj})
    if request.method == 'POST':
        ask_form = AskQuestionForm(request.POST)
        tag_form = TagForm(request.POST)
        template_name = "question/ask_question.html"
        if ask_form.is_valid() and tag_form.is_valid():
            tag = tag_form.save()
            question = CreateQuestion(author=request.user,  # , tag=tag
                                      title=request.POST['title'],
                                      description=request.POST['description'])
            question.save()
            for i_tag in tag:
                question.tag.add(i_tag)
            return HttpResponseRedirect("/ask")
        questions = popular_questions()
        paginator = Paginator(questions, 20)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return search_html(request, template_name,
                           {'form': ask_form, 'tag_form': tag_form,
                            "page_obj": page_obj})


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        avatar_form = AvatarForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.save()
            if avatar_form.is_valid() and 'image' in request.FILES:
                storage_file(request.FILES['image'])
                new_image = Avatar(image=str(request.FILES['image']),
                                   user=user)
                new_image.save()
            else:
                new_image = Avatar(image="profile-icon-empty.png", user=user)
                new_image.save()
            raw_password = user_form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
        if avatar_form.is_valid():
            # redirect user to home page
            return HttpResponseRedirect('/')
    else:
        user_form = SignUpForm()
        avatar_form = AvatarForm()
    return render(request, r'question/registration.html',
                  {'form': user_form, 'avatar_form': avatar_form})


@login_required(login_url='/')
def test_auth(request):
    return render(request, r'question/test.html')


def storage_file(file):
    with open(f'uploads/{file.name}', 'wb+') as new_file:
        for chunk in file.chunks():
            new_file.write(chunk)


@login_required(login_url='/')
def likepost(request):
    if request.method == 'GET':
        answer_id = request.GET['post_id']
        answer = CreateAnswer.objects.get(pk=answer_id)
        author = request.user
        type_id = request.GET['type_id']
        vote_type = AnswerVote.AnswerVoteType.INDIFFERENCE
        if int(type_id) == 2:
            vote_type = AnswerVote.AnswerVoteType.APPROVE
        elif int(type_id) == 1:
            vote_type = AnswerVote.AnswerVoteType.CONDEMN
        elif int(type_id) == 3:
            right_answers = AnswerVote.objects.filter(
                author=request.user,
                type_id=AnswerVote.AnswerVoteType.RIGHT)
            count_right_answers = right_answers.count()
            if count_right_answers > 0:
                for i_answer in right_answers:
                    i_answer.type_id = AnswerVote.AnswerVoteType.APPROVE
                    i_answer.save()
            vote_type = AnswerVote.AnswerVoteType.RIGHT
        try:
            answer_vote = AnswerVote.objects.get(answer=answer)
            answer_vote.author = author
            answer_vote.type_id = vote_type
        except Exception:
            answer_vote = AnswerVote(author=author, answer=answer,
                                     type_id=vote_type)
        answer_vote.save()
        return HttpResponse("Success!")
    return HttpResponse("Request method is not a GET")


@login_required(login_url='/')
def settings(request):
    if request.method == 'GET' and "searchField" in request.GET and \
            request.GET['searchField']:
        return HttpResponseRedirect("/query")
    else:
        try:
            avatar = Avatar.objects.get(user_id=request.user)
            if request.FILES:
                storage_file(request.FILES['image'])
                avatar.image = str(request.FILES['image'])
                avatar.save()
        except Exception:
            pass
        user_form = SettingsForm(data=request.POST or None,
                                 instance=request.user)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.save()

        avatar_form = AvatarForm(request)

        return render(request, "question/settings.html",
                      {"user_form": user_form, 'avatar_form': avatar_form,
                       "avatar": avatar})
