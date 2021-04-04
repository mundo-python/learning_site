from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import DeleteView

from . import models, forms


def course_list(request):
    courses = models.Course.objects.filter(
        published=True
    ).annotate(
        total_steps=Count('text', distinct=True)+Count('quiz', distinct=True)
    )
    total = courses.aggregate(total=Sum('total_steps'))
    email = 'questsions@learning_site.com'
    return render(request, 'courses/course_list.html', {'courses': courses,
                                                        'email': email,
                                                        'total': total})


def course_detail(request, pk):
    try:
        course = models.Course.objects.prefetch_related(
            'quiz_set', 'text_set', 'quiz_set__question_set'
        ).get(pk=pk, published=True)
    except models.Course.DoesNotExist:
        raise Http404
    else:
        steps = sorted(chain(course.text_set.all(),
                             course.quiz_set.all()
                             ), key=lambda step: step.order)
    return render(request, 'courses/course_detail.html',
                  {'course': course,
                   'steps': steps})


def text_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk, course__published=True)
    return render(request, 'courses/text_detail.html', {'step': step})


def quiz_detail(request, course_pk, step_pk):
    try:
        step = models.Quiz.objects.select_related(
            'course'
        ).prefetch_related(
            'question_set',
            'question_set__answer_set'
        ).get(
            course_id=course_pk,
            pk=step_pk,
            course__published=True
        )
    except models.Quiz.DoesNotExist:
        raise Http404
    else:

        return render(request, 'courses/quiz_detail.html', {'step': step})


@login_required
def course_create(request):
    form = forms.CourseForm()

    if request.method == 'POST':
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            messages.success(request, 'New course created!')
            return HttpResponseRedirect(course.get_absolute_url())
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_edit(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.CourseForm(instance=course)

    if request.method == 'POST':
        form = forms.CourseForm(instance=course, data=request.POST)
        if 'course_save' in form.data:
            if form.is_valid():
                course = form.save(commit=False)
                form.save()
                messages.success(request, 'Updated {}'.format(form.cleaned_data['title']))
                return HttpResponseRedirect(course.get_absolute_url())
        elif 'course_delete' in form.data:
            messages.success(request, 'Deleted Course: {}'.format(course.title))
            course.delete()
            return HttpResponseRedirect(reverse('courses:course_list'))
    return render(request, 'courses/course_form.html', {'form': form, 'course': course})


@login_required
def text_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk, published=True)
    form = forms.TextForm()

    if request.method == 'POST':
        form = forms.TextForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            text.course = course
            text.save()
            messages.success(request, 'New Text Post Created!')
            return HttpResponseRedirect(text.get_absolute_url())
    return render(request, 'courses/text_form.html', {'form': form, 'course': course})


@login_required
def text_edit(request, course_pk, text_pk, ):
    text = get_object_or_404(models.Text, pk=text_pk, course_id=course_pk, course__published=True)
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.TextForm(instance=text)

    if request.method == 'POST':
        form = forms.TextForm(instance=text, data=request.POST)
        if 'text_save' in form.data:
            if form.is_valid():
                text = form.save(commit=False)
                form.save()
                messages.success(request, "Updated {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(text.get_absolute_url())
        elif 'text_delete' in form.data:
            messages.success(request, 'Deleted Text Post: {}'.format(text.title))
            text.delete()
            return HttpResponseRedirect(reverse('courses:detail', kwargs={'pk': course_pk}))
    return render(request, 'courses/text_form.html', {'form': form, 'course': text.course})


@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk, published=True)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, 'New quiz created!')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})


@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk, course__published=True)
    form = forms.QuizForm(instance=quiz)

    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if 'quiz_save' in form.data:
            if form.is_valid():
                quiz = form.save(commit=False)
                form.save()
                messages.success(request, "Updated {}".format(form.cleaned_data['title']))
                return HttpResponseRedirect(quiz.get_absolute_url())
        elif 'quiz_delete' in form.data:
            messages.success(request, 'Deleted quiz: {}'.format(quiz.title))
            quiz.delete()
            return HttpResponseRedirect(reverse('courses:detail', kwargs={'pk': course_pk}))
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': quiz.course})


@login_required
def question_create(request, quiz_pk, question_type, ):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
    if question_type == 'tf':
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = form_class()
    answer_forms = forms.AnswerInlineFormSet(
        queryset=models.Answer.objects.none()
    )

    if request.method == 'POST':
        form = form_class(request.POST)
        answer_forms = forms.AnswerInlineFormSet(
            request.POST,
            queryset=models.Answer.objects.none()
        )

        if form.is_valid() and answer_forms.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Added question")
            return HttpResponseRedirect(quiz.get_absolute_url())

    return render(request, 'courses/question_form.html', {
        'quiz': quiz,
        'form': form,
        'formset': answer_forms
    })


@login_required
def question_edit(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question,
                                 pk=question_pk, quiz_id=quiz_pk)
    if hasattr(question, 'truefalsequestion'):
        form_class = forms.TrueFalseQuestionForm
        question = question.truefalsequestion
    else:
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion
    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormSet(
        queryset=form.instance.answer_set.all()
    )

    if request.method == 'POST':
        form = form_class(request.POST, instance=question)
        answer_forms = forms.AnswerInlineFormSet(
            request.POST,
            queryset=form.instance.answer_set.all()
        )
        if form.is_valid() and answer_forms.is_valid():
            form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            for answer in answer_forms.deleted_objects:
                answer.delete()
            messages.success(request, "Updated question")
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {
        'form': form,
        'quiz': question.quiz,
        'formset': answer_forms
    })


@login_required
def answer_form(request, question_pk, answer_pk=None):
    question = get_object_or_404(models.Question, pk=question_pk)
    formset = forms.AnswerFormSet(queryset=question.answer_set.all())

    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST,
                                      queryset=question.answer_set.all())

        if formset.is_valid():
            answers = formset.save(commit=False)

            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Added answers")
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/answer_form.html', {
        'formset': formset,
        'question': question
    })


def courses_by_teacher(request, teacher, ):
    courses = models.Course.objects.filter(teacher__username=teacher, published=True)
    if not courses:
        return render(request, 'courses/no_teacher.html', {'teacher': teacher})
    return render(request, 'courses/course_list.html', {'courses': courses})


def search(request):
    term = request.GET.get('q')
    courses = models.Course.objects.filter(
        Q(title__icontains=term) | Q(description__icontains=term),
        published=True
    )
    return render(request, 'courses/course_list.html', {'courses': courses})
