from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_alter_companystage_stage'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE companies_companystage "
                        "ALTER COLUMN stage TYPE jsonb "
                        "USING CASE "
                        "WHEN stage IS NULL OR btrim(stage) = '' THEN '[]'::jsonb "
                        "ELSE jsonb_build_array(stage) "
                        "END;"
                    ),
                    reverse_sql=(
                        "ALTER TABLE companies_companystage "
                        "ALTER COLUMN stage TYPE varchar(50) "
                        "USING COALESCE(stage->>0, '');"
                    ),
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='companystage',
                    name='stage',
                    field=models.JSONField(default=list),
                ),
            ],
        ),
    ]
