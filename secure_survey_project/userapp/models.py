from django.db import models


class PersonalEmail(models.Model):

    email = models.EmailField(max_length=254)
