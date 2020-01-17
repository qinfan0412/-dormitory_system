from django.db import models


# 学生表
class Stu(models.Model):
    student_id = models.CharField(max_length=32, verbose_name='学号或者账号', unique=True)
    password = models.CharField(max_length=32, verbose_name='密码')
    name = models.CharField(max_length=32, verbose_name='姓名', default='佚名')
    email = models.CharField(max_length=32, verbose_name='邮箱')  # 用于忘记密码功能
    phone = models.CharField(max_length=32,verbose_name='电话', null=True)
    major_class = models.CharField(max_length=32, null=True, verbose_name='专业班级')
    birthday = models.CharField(verbose_name='出生日期',max_length=32, default='2000.01.01')
    location = models.CharField(max_length=32, verbose_name='住址', default='地球')
    remarks = models.CharField(max_length=256, verbose_name='备注', null=True)

    class Meta:
        db_table = 'Stu'
        verbose_name = '学生表'
        verbose_name_plural = verbose_name
