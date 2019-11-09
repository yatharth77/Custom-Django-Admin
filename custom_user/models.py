from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")

		user_obj	= self.model(email=self.normalize_email(email))

		user_obj.set_password(password)
		user_obj.staff	= is_staff
		user_obj.admin	= is_admin

		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, password=None):
		user = self.create_user(email, password=password, is_staff=True)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(email, password=password, is_admin=True, is_staff=True)
		return user	



class User(AbstractBaseUser):
	email 		= models.EmailField(max_length=100, unique=True)
	staff		= models.BooleanField(default=True)
	admin		= models.BooleanField(default=True)
	active		= models.BooleanField(default=True)

	USERNAME_FIELD	= 'email'
	REQUIRED_FIELDS = []

	objects 	= UserManager()
	def __str__(self):
		return self.email

	def is_staff(self):
		return self.staff

	def is_admin(self):
		return self.admin

	def is_active(self):
		return self.active

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

class Profile(models.Model):
	user 		= models.OneToOneField(User)

