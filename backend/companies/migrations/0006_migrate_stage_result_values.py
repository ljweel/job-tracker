from django.db import migrations


def migrate_result_values(apps, schema_editor):
    CompanyStage = apps.get_model('companies', 'CompanyStage')
    mapping = {
        '대기중': '진행중',
        '합격': '통과',
    }
    for old_value, new_value in mapping.items():
        CompanyStage.objects.filter(result=old_value).update(result=new_value)


def reverse_result_values(apps, schema_editor):
    CompanyStage = apps.get_model('companies', 'CompanyStage')
    mapping = {
        '진행중': '대기중',
        '통과': '합격',
    }
    for old_value, new_value in mapping.items():
        CompanyStage.objects.filter(result=old_value).update(result=new_value)


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_remove_company_status_update_stage_result'),
    ]

    operations = [
        migrations.RunPython(migrate_result_values, reverse_result_values),
    ]
