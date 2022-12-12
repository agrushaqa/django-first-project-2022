from django import template

from ..models import AnswerVote

register = template.Library()


@register.filter(name='vote')
def get_vote(answer_id, type_id):
    return AnswerVote.objects.filter(answer=answer_id, type_id=type_id).count()


@register.filter
def split(value, key=','):
    return value.split(key)
