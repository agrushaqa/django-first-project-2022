
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .library import popular_answers, popular_questions
from .models import CreateQuestion
from .serializers import (ListAnswersSerializer, QuestionListSerializer,
                          UserSerializer)


@api_view()
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def list_questions(request: Request):
    questions = popular_questions()
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(questions, request)
    serializer = QuestionListSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view()
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def user(request: Request):
    return Response({
        'data': UserSerializer(request.user).data
    })


@api_view()
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def search(request: Request, text):
    questions = CreateQuestion.objects.filter(
        title__contains=text)
    return Response({
        'data': QuestionListSerializer(questions, many=True).data
    })


@api_view()
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def question_by_id(request: Request, question_id):
    questions = CreateQuestion.objects.filter(
        pk=question_id)
    return Response({
        'data': QuestionListSerializer(questions, many=True).data
    })


@api_view()
@csrf_exempt
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def get_answers_for_question(request: Request, question_id):
    question = CreateQuestion.objects.get(pk=question_id)
    list_answers = popular_answers(question)
    return Response({
        'data': ListAnswersSerializer(list_answers, many=True).data
    })
