from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Question

class QuestionModelTests(TestCase):
  def test_was_published_recently_with_future_question(self):
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    self.assertIs(future_question.was_published_recently(), False)

def create_question(question_text, days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    response = self.client.get(reverse("polls:index"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_past_question(self):
    create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerysetEqual(response.context["latest_question_list"], ['<Question: Past question.>'])