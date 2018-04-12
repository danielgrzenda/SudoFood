from django.db import models


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
 
    LOSE_WEIGHT = 'LW'
    MAINTAIN_WEIGHT = 'MW'
    GAIN_WEIGHT = 'GW'
    GOALS = (
        (LOSE_WEIGHT, 'Lose Weight'),
        (MAINTAIN_WEIGHT, 'Maintain Weight'),
        (GAIN_WEIGHT, 'Gain Weight'),
    )
    goal = models.CharField(max_length=2, choices=GOALS,
			default=MAINTAIN_WEIGHT)
    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default=FEMALE)

    date_of_birth = models.DateField()

    SEDENTARY = 'S'
    LIGHTLY_ACTIVE = 'LA'
    ACTIVE = 'A'
    VERY_ACTIVE = 'VA'
    LEVELS = (
        (SEDENTARY, 'Sedentary'),
        (LIGHTLY_ACTIVE, 'Lightly Active'),
        (ACTIVE, 'Active'),
        (VERY_ACTIVE, 'Very Active'),
    )
    activity_level = models.CharField(max_length=2, choices=LEVELS,
				default=LIGHTLY_ACTIVE)

    workouts_per_week = models.PositiveSmallIntegerField()
    workout_minutes = models.PositiveSmallIntegerField()
    date_signed_up = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
