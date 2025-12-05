from django.db import migrations

TABLE = "appPUC_Planner_course"
INDEX_NAME = "appPUC_Planner_course_program_d5acf7a0"


def drop_program_column(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({TABLE})")
        columns = [row[1] for row in cursor.fetchall()]
        if "program" not in columns:
            return

        cursor.execute(f"PRAGMA index_list({TABLE})")
        indexes = [row[1] for row in cursor.fetchall()]
        if INDEX_NAME in indexes:
            cursor.execute(f'DROP INDEX IF EXISTS "{INDEX_NAME}"')

        cursor.execute(f"ALTER TABLE {TABLE} DROP COLUMN program")


def restore_program_column(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({TABLE})")
        columns = [row[1] for row in cursor.fetchall()]
        if "program" in columns:
            return

        cursor.execute(
            f"ALTER TABLE {TABLE} ADD COLUMN program varchar(200) NOT NULL DEFAULT ''"
        )
        cursor.execute(f'CREATE INDEX IF NOT EXISTS "{INDEX_NAME}" ON {TABLE} ("program")')

class Migration(migrations.Migration):
    dependencies = [
        ("appPUC_Planner", "0008_delete_requisito"),
    ]

    operations = [
        migrations.RunPython(drop_program_column, restore_program_column),
    ]
