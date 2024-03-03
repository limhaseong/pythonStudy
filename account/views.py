import json

from django.contrib import auth
from account.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse  
from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder
from .forms import RecoveryPwForm, CustomSetPasswordForm
from django.urls import reverse
from .helper import send_mail, email_auth_num
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from .forms import RecoveryIdForm
from django.contrib.auth import authenticate

# Create your views here.
def sign(request):
    # print(request.POST['user_id'])
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            userid = request.POST['user_id']
            user = User.objects.create_user(
                                            user_id=userid,
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],
                                            )
            user1 = auth.authenticate(request, user_id=userid, password=request.POST['password1'])
            auth.login(request, user1)
            return redirect('/')
        # return render(request, 'account/signup.html')
    return render(request, 'account/signup.html')

def login(request):
    if request.method == 'POST':
       user_id = request.POST['user_id']
       password = request.POST['password']
       user = auth.authenticate(request, user_id=user_id, password=password)
       if user is not None:
           auth.login(request, user)
           return redirect('bbs:index')
       else:
           return render(request, 'account/login.html', {'error': 'id or password is incorrect'})
    else:
        return render(request, 'account/login.html')

def logout(request):
    auth_logout(request)
    return redirect('bbs:index')

# @method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):   
    template_name = 'account/id_search.html'
    form1 = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form = self.form1(None)
            # pass
        return render(request, self.template_name, { 'form':form, })
        # return render(request, self.template_name)

def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(username=name, email=email)
       
    return HttpResponse(json.dumps({"result_user_id": result_id.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

class RecoveryPwView(View):
    template_name = 'account/pw_search.html'
    form1 = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form = self.form1(None)
        return render(request, self.template_name, { 'form':form, })

def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    target_user = User.objects.get(user_id=user_id, username=name, email=email)

    if target_user:
        auth_num = email_auth_num()
        target_user.auth = auth_num 
        target_user.save()

        send_mail(
            '비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('account/send_email.html', {
                'auth_num': auth_num,
            }),
        )
    return HttpResponse(json.dumps({"result": target_user.id}, cls=DjangoJSONEncoder), content_type = "application/json")

def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = User.objects.get(id=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.id  
    
    return HttpResponse(json.dumps({"result": target_user.id}, cls=DjangoJSONEncoder), content_type = "application/json")

def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied

    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(id=session_user)
        auth.login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)
        # print(reset_password_form)
        
        if reset_password_form.is_valid():
            user = reset_password_form.save()
            # target_user = User.objects.get(username=current_user)
            # target_user.password = ""
            # target_user.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            logout(request)
            return redirect('account:login')
        else:
            logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'account/pw_reset.html', {'form':reset_password_form})

def form_valid(self, form):
    self.object = form.save()

    send_mail(
        '{}님의 회원가입 인증메일 입니다.'.format(self.object.id),
        [self.object.email],
        html=render_to_string('account/send_email.html', {
            'user': self.object,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
            'domain': self.request.META['HTTP_HOST'],
            'token': default_token_generator.make_token(self.object),
        }),
    )
    return redirect(self.get_success_url())

def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('account:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('account:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('account:login')

def get_success_url(self):
    self.request.session['register_auth'] = True
    messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
    return reverse('account:register_success')

def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'account/register_success.html')
