import smtplib
import hashlib
import random
import time
from email.mime.text import MIMEText
from email.header import Header

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *


# -------------------------------------使用md5算法加密密码
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# ----------------------------------------注册账户
def register(request):
    content = '提示信息:无'
    if request.method == 'POST':
        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        # 首先输入的信息不为空
        if name and student_id and password1 and password2 and email:
            # 然后数据库中没有此账户存在
            stu = Stu.objects.filter(student_id=student_id).first()
            if not stu:
                # 不存在，可以注册,判断密码是否相同
                if password1 == password2:
                    Stu.objects.create(name=name, password=setPassword(password1), student_id=student_id,
                                       email=email)
                    content = '提示信息:恭喜账户【%s】注册成功!' % student_id
                else:
                    content = '提示信息:两次密码不一致！请确认'
            else:
                content = '提示信息:账户【%s】已存在！请重新选择新的账号' % student_id
        else:
            content = '提示信息:请填写完整以后再注册！'
    return render(request, 'register.html', locals())


# -----------------------------------------登陆账户
def login(request):
    content = '提示信息:无'
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        # 如果账户密码都不为空
        if student_id and password:
            # 判断账户是否存在
            has_student_id = Stu.objects.filter(student_id=student_id).first()
            if has_student_id:
                if setPassword(password) == has_student_id.password:
                    # 密码成功跳转网页，并且设置cookie和session
                    response = HttpResponseRedirect('/student/index/')
                    response.set_cookie('student_id', student_id)
                    request.session['student_id'] = student_id
                    return response
                else:
                    content = '提示信息：密码输入错误！'
            else:
                content = '提示信息:账户【%s】不存在！' % student_id
        else:
            content = '提示信息:请填写完整以后再登陆...'
    return render(request, 'login.html', locals())


# --------------------------------------发送邮件的类
class Mail(object):
    def __init__(self, receivers, content):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = "xswsxmcscqkjbegi"  # 刚才我们获取的授权码
        self.sender = '1039459472@qq.com'  # 你的邮箱地址
        self.receivers = receivers  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个
        self.content = content
        self.send()

    def send(self):
        message = MIMEText(self.content, 'plain', 'utf-8')
        message['From'] = Header("管理员", 'utf-8')
        message['To'] = Header("同学", 'utf-8')
        subject = '重要！忘记密码'  # 发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException:
            print('邮件发送失败')


# -----------------------------------------忘记密码页
def forget_password(request):
    content = '提示信息：无'
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        # 判断是否填写
        if student_id and email:
            # 判断账户是否存在
            has_student_id = Stu.objects.filter(student_id=student_id).first()
            if has_student_id:
                # 判断邮箱是否正确
                if has_student_id.email == email:
                    password = str(random.randint(10000000, 99999999))
                    has_student_id.password = setPassword(password)
                    has_student_id.save()
                    email_content = "亲爱的同学你好：由于你忘记密码，因此我们将重新设置你的密码，你的新密码为【%s】,请尽快登陆进入个人中心页进行修改密码！！ " % password
                    mail = Mail(receivers=email, content=email_content)
                    content = '提示信息:邮箱已发送！请去查收...'
                    print(content)
                else:
                    content = '提示信息:邮箱不正确！'
            else:
                content = '提示信息:账户不存在！'
        else:
            content = '提示信息:请填写完整以后再发送...'
    return render(request, 'forgot_password.html', locals())


# -------------------------------------------登出出页面
def logout(request):
    # 删除cookie和session
    response = HttpResponseRedirect('/student/login/')  # 返回登录页
    keys = request.COOKIES.keys()  # 删除多个cookie
    for i in keys:
        response.delete_cookie(i)
    del request.session['student_id']
    return response


# ----------------------登录装饰器，类似拦截器，不登录无法访问其他页面
def LoginDescribe(func):
    # 1.获取cookie中的email和session的信息
    # 2.判断email是不是相等，成功跳转，失败返回登录页
    def inner(request, *args, **kwargs):
        cookie_student_id = request.COOKIES.get('student_id')
        session_student_id = request.session.get('student_id')
        if cookie_student_id == session_student_id and cookie_student_id and session_student_id:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/student/login/')

    return inner


# ---------------------------------------------首页
@LoginDescribe
def index(request):
    student_id = request.COOKIES.get('student_id')
    name = Stu.objects.filter(student_id=student_id).first().name
    return render(request, 'index.html', locals())


# ----------------------------------------修改个人密码
@LoginDescribe
def update_password(request):
    student_id = request.COOKIES.get('student_id')
    name = Stu.objects.filter(student_id=student_id).first().name
    content = '提示信息：你正在修改个人密码...'
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        # 必须全部填写
        if old_password and new_password1 and new_password2:
            stu = Stu.objects.filter(student_id=student_id).first()
            password = stu.passwordM
            # 判断旧密码是否正确
            if setPassword(old_password) == password:
                # 判断两个新密码是否相同
                if new_password1 == new_password2:
                    # 判断新密码是否与旧密码相同
                    if setPassword(new_password1) != password:
                        stu.password = setPassword(new_password1)
                        stu.save()
                        content = '提示信息:恭喜！密码修改成功...'

                    else:
                        content = '提示信息:新密码不可与旧密码相同...'
                else:
                    content = '提示信息:两次新密码输入不一致'
            else:
                content = '提示信息:旧密码输入错误...'
        else:
            content = '提示信息:请填写完整以后再发送...'
    return render(request, 'upadate_password.html', locals())


# --------------------------------个人中心页面
def user_info(request):
    student_id = request.COOKIES.get('student_id')
    user = Stu.objects.filter(student_id=student_id).first()
    name = user.name
    phone = user.phone
    email = user.email
    major_class = user.major_class
    birthday = user.birthday
    location = user.location
    remarks = user.remarks
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.major_class = request.POST.get('major_class')
        user.birthday = request.POST.get('birthday')
        user.location = request.POST.get('location')
        user.remarks = request.POST.get('remarks')
        user.save()
        return HttpResponseRedirect('/student/user_info/')
    return render(request, 'user_info.html', locals())
