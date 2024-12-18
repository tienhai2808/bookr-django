# Generated by Django 5.1 on 2024-11-01 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_book_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='bookcontributor',
            name='role',
            field=models.CharField(choices=[('AUTHOR', 'Author'), ('CO-AUTHOR', 'Co-Author'), ('EDITOR', 'Editor')], max_length=20, verbose_name='The role this contributor had in the book.'),
        ),
    ]
