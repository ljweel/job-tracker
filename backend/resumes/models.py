from django.db import models


class ResumeEvent(models.Model):
    class DocType(models.TextChoices):
        RESUME = '이력서', '이력서'
        PORTFOLIO = '포트폴리오', '포트폴리오'
        COVER_LETTER = '자기소개서', '자기소개서'

    doc_type = models.CharField(max_length=20, choices=DocType.choices, default=DocType.RESUME)
    label = models.CharField(max_length=200, blank=True, default='')
    modified_date = models.DateField()
    pdf_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    class Meta:
        ordering = ['doc_type', '-modified_date']

    def __str__(self):
        return f'[{self.doc_type}] {self.label}'
