from django.contrib import admin
from .models import Company, CompanyStage


class CompanyStageInline(admin.TabularInline):
    model = CompanyStage
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'position', 'source', 'updated_at']
    list_filter = ['source']
    inlines = [CompanyStageInline]
