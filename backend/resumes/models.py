from django.db import models
from django.conf import settings


class ResumeEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    label = models.CharField(max_length=200)
    modified_date = models.DateField()
    pdf_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    class Meta:
        ordering = ['-modified_date']

    def __str__(self):
        return self.label
