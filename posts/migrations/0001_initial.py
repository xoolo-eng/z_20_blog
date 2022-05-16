# Generated by Django 4.0.4 on 2022-05-05 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='#tag')),
                ('slug', models.SlugField(max_length=24)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=posts.models.Post.file_path)),
                ('thumbnail', models.ImageField(upload_to=posts.models.Post.file_path)),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_updated', models.BooleanField(default=False)),
                ('is_moderated', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0)),
                ('rating', models.SmallIntegerField()),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='posts', to='posts.tags')),
            ],
            options={
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Message')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_updated', models.BooleanField(default=False)),
                ('is_moderated', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=posts.models.Comment.file_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]
