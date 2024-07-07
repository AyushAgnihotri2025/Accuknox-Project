from django.db import models

from Accounts.models import User


# Create your models here.
class FriendRequest(models.Model):
    STATUS_CHOICES = [
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected')
    ]

    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def accept(self):
        self.status = 2
        self.save()
        # Create a Friendship relationship
        Friendship.objects.create(user=self.sender, friend=self.receiver)
        Friendship.objects.create(user=self.receiver, friend=self.sender)

    def reject(self):
        self.status = 3
        self.save()

    class Meta:
        unique_together = ('sender', 'receiver')


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends_with', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
