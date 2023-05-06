# Generated by Django 4.1.7 on 2023-05-06 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OauthQQUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('openid', models.CharField(db_index=True, max_length=64, verbose_name='openid')),
            ],
            options={
                'verbose_name': 'qq用户登录数据',
                'verbose_name_plural': 'qq用户登录数据',
                'db_table': 'tb_oauth_qq',
            },
        ),
    ]
