from django.db import models


class RoomDescription(models.Model):
    '''Creates a table to store room types'''

    name = models.CharField(max_length=50)
    capacity = models.IntegerField()


class BookingChart(models.Model):
    '''Creates a table to store room booking inputs'''

    room = models.ForeignKey(RoomDescription, on_delete=models.CASCADE)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
