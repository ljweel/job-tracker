from django.contrib import admin
from .models import ResumeEvent


@admin.register(ResumeEvent)
class ResumeEventAdmin(admin.ModelAdmin):
    list_display = ['label', 'modified_date']
