from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Student(models.Model):
    '''客户信息表'''
    name = models.CharField(max_length=32,blank=True,null=True)
    qq = models.CharField(max_length=64,unique=True)
    phone = models.CharField(max_length=64,blank=True,null=True)
    source_choices = ((0,'夏令营'),
                      (1,'统考'),
                      (2,'考研群'),
                      )
    source = models.SmallIntegerField(choices=source_choices)
    school = models.ForeignKey("School",on_delete=models.CASCADE)
    examination = models.ManyToManyField("Exam",verbose_name="考试事项",)
    status_choices = ((0,'确认考试'),
                      (1,'待确认考试'),
                      )
    status = models.SmallIntegerField(choices=status_choices,default=1)
    memo = models.TextField(verbose_name='备注',blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name ="学生表"
        verbose_name_plural ="学生表"


class School(models.Model):
    name = models.CharField(max_length=128,blank=True,null=True)


    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = "学校表"
        verbose_name_plural = "学校表"

class Exam(models.Model):
    exam_name=models.CharField(max_length=128,blank=True,null=True)
    location_choice = ((0,"三教"),
                       (1,"科技楼"),
                       (2,"电二楼"),)
    location = models.SmallIntegerField(choices=location_choice,default=1)
    exam_content_choice= ((0,"上机考试"),
                          (1,"英语面试"),
                          (2,"专业面试"),
                            )
    exam_content = models.SmallIntegerField(choices=exam_content_choice,default=0)
    exam_time = models.DateTimeField()

    def __str__(self):
        return self.exam_name