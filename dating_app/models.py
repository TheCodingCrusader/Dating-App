from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, User
from dating_project import settings



class ProfileManager(BaseUserManager):



	def create_user(self, username, email,description,photo, password=None):
		if not email:
			raise ValueError("You must creat an email")
		if not username:
			raise ValueError("You must create a username!")
		if not description:
			raise ValueError("You must write a description")
		if not photo:
			raise ValueError("You must upload a photo")

		user = self.model(
				email=self.normalize_email(email),
				username = username, 
				description= description,
				photo= photo,
			
			)

		user.set_password(password)
		user.save(using=self._db)
		return user 


	def create_superuser(self, username, email,description,photo, password):
		user = self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,
				description=description,
				photo=photo,
				
			)

		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user
	



class Profile(AbstractBaseUser):

	email 						= models.EmailField(verbose_name="email")
	username					= models.CharField(max_length=30, unique=True)
	date_joined					= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login					= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin					= models.BooleanField(default=False)
	is_active					= models.BooleanField(default=True)
	is_staff					= models.BooleanField(default=False)
	is_superuser				= models.BooleanField(default=False)
	#what I added
	description 				= models.TextField()
	photo 						= models.ImageField(upload_to='profile_photo',blank=False, height_field=None, width_field=None, max_length=100)
	#owner 						= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) (not working, for tracking owner of profile)


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['description','photo','email']


	objects = ProfileManager()


	def __str__(self):
		return self.username


	def has_perm(self, perm, obj=None):
		return self.is_admin


	def has_module_perms(self,app_label):
		return True






