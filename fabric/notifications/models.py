from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=11, unique=True)
    client_operator_code = models.CharField(max_length=10)
    client_tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=50)

class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    start_datetime = models.DateTimeField()
    message_text = models.TextField()
    end_datetime = models.DateTimeField()
    client_tag = models.CharField(max_length=50, default='new')

class StatisticsNewletter(models.Model):
    tag = models.CharField(max_length=50, unique=True)
    total_messages_sent = models.IntegerField(default=0)

    def __str__(self):
        return f"Tag: {self.tag}, Total Messages Sent: {self.total_messages_sent}"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.id} to {self.client.phone_number} in {self.newsletter.start_datetime}"