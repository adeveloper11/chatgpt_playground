
from django.db import models

class ChatLog(models.Model):
    option = models.CharField(max_length=100)
    query = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f"Option: {self.option}, Query: {self.query},"


class QueryOption(models.Model):
    option_name = models.CharField(max_length=50)
    option_value = models.CharField(max_length=100)

    def __str__(self):
        return f"Query: {self.id, self.option_name}"
    
class Feedbackdata(models.Model):
    Name = models.CharField(max_length=50)
    Mobile = models.IntegerField()
    Email = models.EmailField(max_length=300)
    Feedback = models.TextField()

    def __str__(self):
        return f"feedback: {self.id, self.Name}"
    
class Login(models.Model):
    Email = models.EmailField(max_length=300)
    Password = models.CharField(max_length=100)

    def __str__(self):
        return f"loginInfo: {self.Email}"