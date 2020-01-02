from django.db import models


# 学生表
class Stu(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')
    professional_class = models.CharField(max_length=32, null=True, verbose_name='专业班级')
    student_id = models.CharField(max_length=32, verbose_name='学号或者账号')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.CharField(max_length=32, verbose_name='邮箱')  # 用于忘记密码功能
    phone = models.IntegerField(verbose_name='电话', null=True)

    class Meta:
        db_table = 'Stu'
        verbose_name = '学生表'
        verbose_name_plural = verbose_name
