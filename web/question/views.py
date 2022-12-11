from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from .forms import (AskQuestionForm, CreateAnswerForm, TagForm)
from common.library import popular_answers, popular_questions, \
    generate_trading, search_html
# Create your views here.

from .models import (AnswerVote, CreateAnswer, CreateQuestion,
                     QuestionVote)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from askme.settings import EMAIL_FROM


class HomeRedirectView(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'home'

    def get(self, request):
        if 'searchField' in request.GET.keys() and request.GET['searchField']:
            return HttpResponseRedirect(
                f"/query?searchField={request.GET['searchField']}")
        else:
            questions = popular_questions()
            paginator = Paginator(questions, 20)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return search_html(request, "question/home.html",
                               {"page_obj": page_obj})


class TradingMixin(object):
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except Exception:
            context = {}
        return generate_trading(self.request, context)


class QListView(TradingMixin, LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'list_all_questions'
    # queryset = popular_questions() # из-за этой строки makemigrations падала
    # с ошибкой. В качестве решения создал get_queryset
    context_object_name = 'form'
    template_name = "question/list.html"

    def get_queryset(self, *args, **kwargs):
        return popular_questions()


class ShowQuestionView(View):
    def get(self, request, question_id):
        question = CreateQuestion.objects.get(pk=question_id)
        question_unlike = False
        question_like = False
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
        answer_form = CreateAnswerForm()
        paginator = Paginator(popular_answers(question), 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return search_html(request,
                           "question/show_question.html",
                           {"question": question,
                            "answer_form": answer_form,
                            "page_obj": page_obj,
                            "question_unlike": question_unlike,
                            "question_like": question_like,
                            "count_question_like": self.get_count_like(
                                question),
                            "count_question_unlike": self.get_count_unlike(
                                question)
                            })

    def get_count_like(self, question):
        try:
            count_question_like = QuestionVote.objects.filter(
                question=question,
                type_id=QuestionVote.QuestionVoteType.APPROVE).count()
        except Exception:
            count_question_like = 0
        return count_question_like

    def get_count_unlike(self, question):
        try:
            count_question_unlike = QuestionVote.objects.filter(
                question=question,
                type_id=QuestionVote.QuestionVoteType.CONDEMN).count()
        except Exception:
            count_question_unlike = 0
        return count_question_unlike

    def post(self, request, question_id):
        question = CreateQuestion.objects.get(pk=question_id)
        if 'question_like' in request.POST:
            try:
                question_vote = QuestionVote.objects.get(author=request.user,
                                                         question=question)
                question_vote.type_id = \
                    QuestionVote.QuestionVoteType.INDIFFERENCE
                if request.POST['question_like'] == 'unlike':
                    question_vote.type_id = \
                        QuestionVote.QuestionVoteType.CONDEMN
                if request.POST['question_like'] == 'like':
                    question_vote.type_id = \
                        QuestionVote.QuestionVoteType.APPROVE
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
                    from_email=EMAIL_FROM,
                    recipient_list=[question.author.email], fail_silently=False
                )
        return HttpResponseRedirect(f"/question/{question_id}")


class QueryTagListView(TradingMixin, LoginRequiredMixin, SingleObjectMixin,
                       ListView):
    login_url = '/login'
    redirect_field_name = 'list_questions_by_tag'
    template_name = "question/list.html"
    model = CreateQuestion
    paginate_by = 20
    context_object_name = 'form'

    def get(self, request, *args, **kwargs):
        self.object = CreateQuestion.objects.filter(
            tag__tag=request.GET['name'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            tag__tag=self.request.GET['name']
        )


class QueryRequestListView(TradingMixin, LoginRequiredMixin, SingleObjectMixin,
                           ListView):
    login_url = '/login'
    redirect_field_name = 'list_queried_questions'
    template_name = "question/list.html"
    model = CreateQuestion
    paginate_by = 20
    context_object_name = 'form'

    def get(self, request, *args, **kwargs):
        self.object = CreateQuestion.objects.filter(
            title__contains=self.request.GET['searchField'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            title__contains=self.request.GET['searchField']
        )


class AskMeListView(TradingMixin, LoginRequiredMixin, ListView):
    # login_url = '/login'
    # redirect_field_name = 'ask'
    # paginate_by = 20
    # template_name = "question/ask_question.html"
    # form_class = AskQuestionForm
    # success_url = "/ask"
    # tag_form_class = TagForm
    #
    # def post(self, request):
    #     post_data = request.POST or None
    #     ask_form = self.form_class(post_data)
    #     tag_form = self.tag_form_class(post_data)
    #
    #     if ask_form.is_valid():
    #         self.form_save(ask_form)
    #     if tag_form.is_valid():
    #         tag = self.form_save(tag_form)
    #         question = CreateQuestion(author=self.request.user,  # , tag=tag
    #                                   title=self.request.POST['title'],
    #                                   description=self.request.POST[
    #                                       'description'])
    #         question.save()
    #         for i_tag in tag:
    #             question.tag.add(i_tag)
    #         questions = popular_questions()
    #         paginator = Paginator(questions, 20)
    #
    #         page_number = request.GET.get('page')
    #         page_obj = paginator.get_page(page_number)
    #         return search_html(request, self.template_name,
    #                            {'form': self.form_class,
    #                             'tag_form': tag_form,
    #                             "page_obj": page_obj})
    #
    # def form_save(self, form):
    #     obj = form.save()
    #     messages.success(self.request, "{} saved successfully".format(obj))
    #     return obj
    #
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)

    # def form_valid(self, tag_form):
    #     tag = tag_form.save()
    #     question = CreateQuestion(
    #                   author=self.request.user,  # , tag=tag
    #                   title=self.request.POST['title'],
    #                   description=self.request.POST['description'])
    #     question.save()
    #     for i_tag in tag:
    #         question.tag.add(i_tag)

    def get(self, request):
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

    def post(self, request):
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


class LikePostView(LoginRequiredMixin, SingleObjectMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'likepost'

    def get(self, request):
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
