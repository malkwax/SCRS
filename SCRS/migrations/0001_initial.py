# Generated by Django 2.0.5 on 2018-07-21 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(blank=True, max_length=128, null=True)),
                ('location', models.SmallIntegerField(choices=[(0, '三教'), (1, '科技楼'), (2, '电二楼')], default=1)),
                ('exam_content', models.SmallIntegerField(choices=[(0, '上机考试'), (1, '英语面试'), (2, '专业面试')], default=0)),
                ('exam_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'verbose_name': '学校表',
                'verbose_name_plural': '学校表',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('qq', models.CharField(max_length=64, unique=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('source', models.SmallIntegerField(choices=[(0, '夏令营'), (1, '统考'), (2, '考研群')])),
                ('status', models.SmallIntegerField(choices=[(0, '确认考试'), (1, '待确认考试')], default=1)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('examination', models.ManyToManyField(to='SCRS.Exam', verbose_name='考试事项')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SCRS.School')),
            ],
            options={
                'verbose_name': '学生表',
                'verbose_name_plural': '学生表',
            },
        ),
    ]