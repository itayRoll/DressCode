from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta

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
	spammer_credit = models.IntegerField(default=0)
	spammer = models.BooleanField(default=False)
	last_ban_timestamp = models.DateTimeField(default=datetime.now()-timedelta(days=200))

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
	items_not_as_pic = models.BooleanField(default=False)
	is_system_question = models.BooleanField(default=False)
	# items_not_as_pic = models.IntegerField(default=0)

	def __str__(self):
		return '{0}: {1}'.format(self.pk, self.title)

	class Meta:
		ordering = ["-due_date", "-user__score"]


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
	items_not_as_pic = models.BooleanField(default=False)
	question_id = models.IntegerField()

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.question_id, self.user.user.username, self.vote)


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
		('9','SWIM SUIT'),
		('10','SUIT'),
		('11', 'PANTS'),
		('12', 'SKIRT'),
		('13', 'JEANS'),
		('14', 'TIE'),
		('15', 'SCARF'),
		('16', 'JACKET'),
	)

	PATTERN = (
		('1', 'NONE'),
		('2', 'STRIPES'),
		('3', 'DOTS'),
		('4', 'CHECKED'),
	)


	color = models.CharField(max_length=2, choices=COLORS, null=True)
	type = models.CharField(max_length=2, choices=TYPES, null=True)
	pattern = models.CharField(max_length=2, choices=PATTERN, null=True)
	question_id = models.IntegerField(null=True)

	# def __str__(self):
	# 	col_val = 0
	# 	typ_val = 0
	# 	pat_val = 0
	# 	for tup in self.COLORS:
	# 		if self.color == str(tup[1]):
	# 			col_val = str(tup[1])
	# 			break
	# 	for tup2 in self.TYPES:
	# 		if self.type.replace('-', '') == str(tup2[1]):
	# 			typ_val = str(tup2[1])
	# 			break
	# 	for tup3 in self.PATTERN:
	# 		if self.pattern == str(tup3[1]):
	# 			pat_val = str(tup3[1])
	# 			break
	# 	return '{0}- Color: {1}, Pattern: {2}'.format(typ_val, col_val, pat_val)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.type, self.color, self.pattern)


class NegativeReport(models.Model):
	user = models.ForeignKey('Fuser', null=True)
	report_time = models.DateTimeField(default=timezone.now)
	question = models.ForeignKey('Question', null=True)