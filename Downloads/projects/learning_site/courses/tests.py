from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
import datetime

from .models import Course, Step

class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title='Python Regular Expressions',
            description='Learn to write good regex'
        )
        td = datetime.timedelta(microseconds = 1)
        now = timezone.now() + td
        self.assertLess(course.created_at,now)

class StepModelTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title = "Python Testing",
            description = "Learn to write python tests",
        )

    def test_step_creation(self):

        step = Step.objects.create(
            title='Step number one!',
            content='This is how you do step one',
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())

class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Python testing',
            description='Learn to write tests'
        )
        self.course2 = Course.objects.create(
            title='New course',
            description='A new course'
        )
        self.step = Step.objects.create(
            title='Intro to doc tests',
            description='Learn to write tests',
            course=self.course,
            id=1
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:course_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail',
                                       kwargs={'pk': self.course.pk}))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(self.course, resp.context['course'])

    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step',
                                       kwargs={'course_pk': self.course.pk,
                                               'step_pk': self.step.pk}))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(self.step, resp.context['step'])

