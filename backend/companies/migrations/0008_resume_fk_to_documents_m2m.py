from django.db import migrations, models


def migrate_resume_to_documents(apps, schema_editor):
    CompanyStage = apps.get_model('companies', 'CompanyStage')
    for stage in CompanyStage.objects.filter(resume__isnull=False):
        stage.documents.add(stage.resume)


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_remove_user_fk'),
        ('resumes', '0004_add_doc_type_and_label_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='companystage',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='stages', to='resumes.resumeevent'),
        ),
        migrations.RunPython(migrate_resume_to_documents, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='companystage',
            name='resume',
        ),
    ]
