from django.db import models


class Company(models.Model):
    class Source(models.TextChoices):
        SARAMIN = '사람인', '사람인'
        WANTED = '원티드', '원티드'
        OFFICIAL = '공식홈페이지', '공식홈페이지'
        REFERRAL = '추천', '추천'
        ETC = '기타', '기타'

    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.ETC)
    job_url = models.URLField(blank=True, default='')
    memo = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        results = list(self.stages.values_list('result', flat=True))
        if not results:
            return None
        if '불합격' in results:
            return '불합격'
        if '진행중' in results:
            return '진행중'
        return '최종통과'

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.company_name} - {self.position}'


class CompanyStage(models.Model):
    class Stage(models.TextChoices):
        DOCUMENT = '서류', '서류'
        CODING_TEST = '코테', '코테'
        COFFEE_CHAT = '커피챗', '커피챗'
        INTERVIEW = '면접', '면접'
        ASSIGNMENT = '과제', '과제'

    class Method(models.TextChoices):
        ONLINE = '온라인', '온라인'
        OFFLINE = '오프라인', '오프라인'

    class Result(models.TextChoices):
        FINAL_PASS = '최종통과', '최종통과'
        PASS = '통과', '통과'
        IN_PROGRESS = '진행중', '진행중'
        REJECTED = '불합격', '불합격'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='stages')
    resume = models.ForeignKey('resumes.ResumeEvent', on_delete=models.SET_NULL, null=True, blank=True, related_name='stages')
    stage = models.JSONField(default=list)
    method = models.CharField(max_length=10, choices=Method.choices)
    date = models.DateField()
    result = models.CharField(max_length=10, choices=Result.choices, default=Result.IN_PROGRESS)
    memo = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['date']

    def __str__(self):
        if isinstance(self.stage, list):
            stage_text = ', '.join(self.stage)
        else:
            stage_text = str(self.stage)
        return f'{self.company.company_name} - {stage_text}'
