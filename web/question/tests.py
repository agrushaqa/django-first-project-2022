from datetime import datetime

from django.test import TestCase

from .models import CreateQuestion, User

# Create your tests here.


class CreateQuestionTestCase(TestCase):
    def setUp(self):
        self.current_dateTime = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        user = User(username="autotest", first_name="auto", last_name="test")
        user.save()
        question = CreateQuestion(author=user,
                                  title=f"autotest {self.current_dateTime}",
                                  description="autotest-body")
        question.save()

    def test_creation(self):
        test_question = CreateQuestion.objects.get(
            title=f"autotest {self.current_dateTime}")
        self.assertEqual(test_question.title,
                         f"autotest {self.current_dateTime}")
        self.assertEqual(test_question.description, "autotest-body")
        self.assertEqual(test_question.author.username, "autotest")
