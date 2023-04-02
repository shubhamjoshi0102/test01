from datetime import datetime
from .models import RoomDescription, BookingChart


def time_slot_validity(start_time, end_time):
    '''Check the time format logically'''
    acceptable_values = ['00', '15', '30', '45']

    try:
        time_obj1 = datetime.strptime(start_time, "%H:%M")
        time_obj2 = datetime.strptime(end_time, "%H:%M")

        # Convert the datetime object to a string in HH:MM format
        output_time1 = time_obj1.strftime("%H:%M")
        output_time2 = time_obj2.strftime("%H:%M")

        if output_time2 > "23:45" or output_time1 >= output_time2:
            return False
        if output_time1[3:] in acceptable_values and output_time2[3:] in acceptable_values:
            return True
        return False

    except ValueError:
        return False


def capacity_in_range(capacity):
    '''Check the validity of the capacity size input'''
    if int(capacity) in range(2,21):
        return True
    return False


def check_availability(start_time, end_time, capacity):
    '''Check whether the room is availble for the time period'''
    available_rooms = []
    rooms = RoomDescription.objects.filter(capacity__gte=int(capacity)).order_by('capacity')

    for room in rooms:

        slots_booked = BookingChart.objects.filter(
            room = room,
            start_time__lte = end_time,
            end_time__gt = start_time
        )
        # The logic is such,
        # a requested event cannot start before a booked event and
        # a requested event cannot end after a booked event

        if not slots_booked.exists():
            available_rooms.append(room.name)

    return available_rooms


def book_room(vacant_rooms, start_time, end_time, capacity):
    '''Book room from a list of vacant rooms'''
    for room in vacant_rooms:
        query_set = RoomDescription.objects.filter(name=room).first()
        if query_set.capacity >= int(capacity):
            booking = BookingChart.objects.create(
                room = query_set,
                start_time = start_time,
                end_time = end_time
            )
            booking.save()
            return room


def not_overlaps_with_buffer(start_time, end_time):
    '''Check whether the requested time period overlaps with the buffer time period'''
    buffer_time = [["09:00","09:15"], ["13:15","13:45"], ["18:45","19:00"]]

    for time in buffer_time:
        if start_time <= time[0]:
            if end_time >= time[1]:
                return False
            if end_time > time[0] and end_time <= time[1]:
                return False
        if start_time > time[0]:
            if end_time <= time[1]:
                return False
            if start_time < time[1]:
                return False

    return True
