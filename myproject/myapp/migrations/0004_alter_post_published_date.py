# Generated by Django 4.2.5 on 2023-09-06 20:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="published_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]