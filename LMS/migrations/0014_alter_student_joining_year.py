# Generated by Django 5.0.1 on 2024-02-24 17:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LMS", "0013_alter_student_joining_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="Joining_Year",
            field=models.IntegerField(
                max_length=4,
                validators=[
                    django.core.validators.MinValueValidator(2000),
                    django.core.validators.MaxValueValidator(2050),
                ],
            ),
        ),
    ]
