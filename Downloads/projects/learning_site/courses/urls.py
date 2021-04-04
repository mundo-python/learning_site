
from django.urls import path


from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_pk>/t<int:step_pk>/', views.text_detail, name='text'),
    path('<int:course_pk>/create_text/', views.text_create, name='text_create'),
    path('<int:course_pk>/edit_text/<int:text_pk>/', views.text_edit, name='text_edit'),
    path('<int:course_pk>/q<int:step_pk>/', views.quiz_detail, name='quiz'),
    path('<int:course_pk>/create_quiz/', views.quiz_create, name='quiz_create'),
    path('<int:course_pk>/edit_quiz/<int:quiz_pk>/', views.quiz_edit, name='quiz_edit'),
    path('<int:quiz_pk>/create_question/(?P<question_type>mc|tf)/$',
         views.question_create, name='question_create'),
    path('<int:quiz_pk>/edit_question/<int:question_pk>/', views.question_edit, name='question_edit'),
    path('<int:question_pk>/create_answer/', views.answer_form, name='answer_create'),
    path('by/<str:teacher>', views.courses_by_teacher, name='by_teacher'),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.course_detail, name='detail'),
    path('create_course/', views.course_create, name='course_create'),
    path('edit_course/<int:course_pk>/', views.course_edit, name='course_edit'),
]