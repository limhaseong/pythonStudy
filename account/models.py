from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, user_id, password, email, username, **extra_fields):
        if not user_id:
            raise ValueError('user_id Required!')

        user = self.model(
            user_id = user_id,
            email = email,
            username = username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, email=None, auth=None):

        user = self.create_user(user_id, password, email, auth)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    seq = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True, null=False)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    email = models.EmailField(max_length=100, verbose_name="이메일",null=True)  #, unique=True
    username = models.CharField(max_length=8, verbose_name="이름", null=True)
    auth = models.CharField(max_length=10, verbose_name="인증번호", null=True, default='')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "User"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"
