import os
import smtplib
import ssl
from email.message import EmailMessage
from itertools import chain

from django.db.models import Case, Count, Q, When

from .models import AnswerVote, CreateAnswer, CreateQuestion, QuestionVote


def popular_question_ids():
    """
    :return: question ids sorted count like and updated_at
    """
    voted_question = QuestionVote.objects.filter(
        Q(type_id=2) | Q(type_id=3)).values(
        'question').annotate(total=Count('author')).order_by(
        '-total').values_list('question', flat=True)
    unvoted_question = CreateQuestion.objects.filter(~Q(
        pk__in=voted_question)).order_by('-updated_at').values_list('pk',
                                                                    flat=True)
    return list(chain(voted_question, unvoted_question))


def popular_answers_ids(question):
    list_answers = CreateAnswer.objects.filter(question_id=question)
    best_answer = AnswerVote.objects.filter(Q(answer__in=list_answers) & Q(
        type_id=3)).values('answer').annotate(
        total=Count('author')).order_by(
        '-total').values_list('answer', flat=True)
    voted_answers = AnswerVote.objects.filter(Q(answer__in=list_answers) & Q(
        type_id=2)).values('answer').annotate(
        total=Count('author')).order_by(
        '-total').values_list('answer', flat=True)
    unvoted_answers = list_answers.filter(~Q(pk__in=voted_answers) & ~Q(
        pk__in=best_answer)).values_list("pk", flat=True)
    return list(chain(best_answer, voted_answers, unvoted_answers))


def popular_answers(question):
    _count = popular_answers_ids(question)
    ordering = []
    ordering.append(Case(*[When(pk=pk, then=pos) for pos, pk in
                           enumerate(_count)]))
    return CreateAnswer.objects.filter(
        question_id=question).order_by(*ordering)


def popular_questions():
    _count = popular_question_ids()
    ordering = []
    ordering.append(Case(*[When(pk=pk, then=pos) for pos, pk in
                           enumerate(_count)]))
    return CreateQuestion.objects.all().order_by(*ordering)


def lib_send_email(email, subject, body, port=587):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = os.environ.get('EMAIL_FROM')
        msg["To"] = email

        context = ssl.create_default_context()

        with smtplib.SMTP(os.environ.get('EMAIL_HOST'), port=port) as \
                smtp:
            smtp.starttls(context=context)
            smtp.login(msg["From"], os.environ.get('EMAIL_HOST_PASSWORD'))
            smtp.send_message(msg)
            print(f"send email to {email}")
    except Exception as e:
        print("Error: unable to send email")
        print(e)
