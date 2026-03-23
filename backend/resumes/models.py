from django.db import models


class ResumeEvent(models.Model):
    label = models.CharField(max_length=200)
    modified_date = models.DateField()
    pdf_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    class Meta:
        ordering = ['-modified_date']

    def __str__(self):
        return self.label
