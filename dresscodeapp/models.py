from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Fuser(models.Model):
	"""
	Model represents a user in our system
	"""
	GENDERS = (
		('m', 'MALE'),
		('f', 'FEMALE'),
		('u', 'UNKOWN'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	dob = models.DateField(null=True, verbose_name='Date Of Birth')
	date_joined = models.DateTimeField(default=timezone.now(), editable=False)
	score = models.IntegerField(default=10)		# first question is on the house
	gender = models.CharField(max_length=1, choices=GENDERS)
	num_questions = models.IntegerField(default=0)
	num_answers = models.IntegerField(default=0)

	def __str__(self):
		return '{0}'.format(self.user)


class Question(models.Model):
	"""
	Model represents a question from a user
	"""
	user = models.ForeignKey('Fuser', null=True)
	photo_path = models.CharField(max_length=200)
	published_date = models.DateTimeField(default=timezone.now)
	title = models.CharField(max_length=80)
	description = models.TextField()
	due_date = models.DateTimeField(null=True)
	clothing_items = models.ManyToManyField('ClothingItem')

	def __str__(self):
		return self.title


class Answer(models.Model):
	"""
	Model represents an answer from a user to another user's quiestion
	"""
	VOTES = (
		('1','YES'),
		('0', 'MAYBE'),
		('2', 'NO'),
	)
	user = models.ForeignKey('Fuser', null=True)
	published_date = models.DateTimeField(default=timezone.now)
	vote = models.CharField(max_length=1, choices=VOTES)
	question_id = models.IntegerField()


class ClothingItem(models.Model):
	COLORS = (
		('1', 'BLUE'),
		('2', 'RED'),
		('3', 'BLACK'),
		('4', 'WHITE'),
		('5', 'PURPLE'),
		('6', 'GREEN'),
		('7', 'YELLOW'),
		('8', 'BROWN'),
		('9', 'GREY'),
	)
	TYPES = (
		('1','TSHIRT'),
		('2','SHIRT'),
		('3','SHORT PANTS'),
		('4','HAT'),
		('5','SHOES'),
		('6','HOODIE'),
		('7','DRESS'),
		('8','LONG PANTS'),
		('9','SWIM SUIT'),
		('10','SUIT'),
		('11', 'PANTS'),
		('12', 'SKIRT'),
	)

	PTTERN = (
		('1', 'NONE'),
		('2', 'STRIPES'),
		('3', 'DOTS'),
		('4', 'CHECKED'),
	)

	color = models.CharField(max_length=2, choices=COLORS, null=True)
	type = models.CharField(max_length=2, choices=TYPES, null=True)
	pattern = models.CharField(max_length=2, choices=PTTERN, null=True)
	question_id = models.IntegerField()

	def __str__(self):
		return '{0} {1}'.format(self.color[1], self.type[1])


