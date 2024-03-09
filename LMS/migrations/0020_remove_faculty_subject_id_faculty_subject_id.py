# Generated by Django 5.0.1 on 2024-03-09 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LMS", "0019_remove_faculty_subject_id_faculty_subject_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="faculty",
            name="Subject_ID",
        ),
        migrations.AddField(
            model_name="faculty",
            name="Subject_ID",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="LMS.course"
            ),
        ),
    ]
