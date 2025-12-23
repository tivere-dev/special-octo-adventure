from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    remember_me = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def verify_email(self):
        self.email_verified = True
        self.email_verified_at = timezone.now()
        self.save()

    def update_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)
    consumed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Email verification token for {self.user.email}"

    def is_valid(self):
        if self.consumed:
            return False
        expiry_time = self.created_at + timezone.timedelta(minutes=30)
        return timezone.now() < expiry_time

    def consume(self):
        self.consumed = True
        self.consumed_at = timezone.now()
        self.save()


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)
    consumed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Password reset token for {self.user.email}"

    def is_valid(self):
        if self.consumed:
            return False
        expiry_time = self.created_at + timezone.timedelta(minutes=30)
        return timezone.now() < expiry_time

    def consume(self):
        self.consumed = True
        self.consumed_at = timezone.now()
        self.save()


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    invalidated = models.BooleanField(default=False)
    invalidated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Refresh token for {self.user.email}"

    def is_valid(self):
        if self.invalidated:
            return False
        return timezone.now() < self.expires_at

    def invalidate(self):
        self.invalidated = True
        self.invalidated_at = timezone.now()
        self.save()

    @classmethod
    def invalidate_all_for_user(cls, user):
        cls.objects.filter(user=user, invalidated=False).update(
            invalidated=True,
            invalidated_at=timezone.now()
        )
