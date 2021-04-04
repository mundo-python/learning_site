from django import forms


from . import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            'title',
            'description',
            'teacher',
            'subject',
            'published'
        ]


class TextForm(forms.ModelForm):
    class Meta:
        model = models.Text
        fields = [
            'title',
            'description',
            'order',
            'content'

        ]


class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = [
            'title',
            'description',
            'order',
            'total_questions'
        ]


class QuestionForm(forms.ModelForm):
    class Media:
        css = {'all': ('courses/css/order.css',)}
        js = (
            'courses/js/vendor/jquery.fn.sortable.min.js',
            'courses/js/order.js'
        )


class TrueFalseQuestionForm(QuestionForm):
    class Meta:
        model = models.TrueFalseQuestion
        fields = [
            'order',
            'prompt'
        ]


class MultipleChoiceQuestionForm(QuestionForm):
    class Meta:
        model = models.MultipleChoiceQuestion
        fields = [
            'order',
            'prompt',
            'shuffle_answers'
        ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = [
            'order',
            'text',
            'correct'
        ]


CourseFormSet = forms.modelformset_factory(
    models.Course,
    form=CourseForm,
    min_num=1,
)

AnswerFormSet = forms.modelformset_factory(
    models.Answer,
    form=AnswerForm,
    extra=5
)

AnswerInlineFormSet = forms.inlineformset_factory(
    models.Question,
    models.Answer,
    extra=4,
    fields=('order', 'text', 'correct'),
    formset=AnswerFormSet,
    min_num=1,
)
