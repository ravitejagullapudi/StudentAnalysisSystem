# Generated by Django 2.0.6 on 2018-08-15 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faqs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('query', models.CharField(max_length=1000)),
                ('answer', models.CharField(default=' none ', max_length=1000)),
            ],
        ),
    ]
