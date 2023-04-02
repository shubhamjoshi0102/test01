from django.shortcuts import render
from django.views import View
from .functions import (time_slot_validity, capacity_in_range,
                        check_availability, book_room, not_overlaps_with_buffer)


class BookRoom(View):
    '''Class to check the availability and book a room'''

    def get(self, request):
        '''Get request to get the welcome page'''
        return render(request, 'home.html')

    def post(self, request):
        '''Post request to post the input and return output'''
        term = request.POST.get('term')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        capacity = request.POST.get('capacity')

        if time_slot_validity(start_time, end_time):

            context_no_vacant = {"status" : "NO_VACANT_ROOM"}

            if not_overlaps_with_buffer(start_time, end_time):
                if capacity_in_range(capacity):
                    vacant_rooms = check_availability(start_time,end_time,capacity)

                    if vacant_rooms:

                        if term == "VACANCY":
                            vacant_rooms_names = " ".join(vacant_rooms)
                            context_vacant_rooms = {'status' : vacant_rooms_names}
                            return render(request, "home.html", context_vacant_rooms)

                        booked_room = book_room(vacant_rooms, start_time, end_time, capacity)
                        context_room_book = {"status" : booked_room}
                        return render(request, 'home.html', context_room_book)

                    return render(request, 'home.html', context_no_vacant)

                return render(request, "home.html", context_no_vacant)

            return render(request, 'home.html', context_no_vacant)

        context = {"status": "INCORRECT_INPUT"}
        return render(request, "home.html", context)
