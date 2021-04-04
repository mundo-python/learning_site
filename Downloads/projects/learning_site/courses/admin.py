from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Course)
admin.site.register(models.Text)
admin.site.register(models.Quiz)
admin.site.register(models.MultipleChoiceQuestion)
admin.site.register(models.TrueFalseQuestion)
admin.site.register(models.Answer)
