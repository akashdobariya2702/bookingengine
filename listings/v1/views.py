from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q, Min
# Create your views here.


from listings.models import BookingInfo, HotelRoom, Reservation
from .serializers import ListingSerializer


class Units(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # /api/v1/units/?max_price=100&check_in=2021-12-09&check_out=2021-12-12
        max_price = request.GET.get('max_price', None)
        check_in = request.GET.get('check_in', None)
        check_out = request.GET.get('check_out', None)

        queryset = BookingInfo.objects.all().order_by('price')
        if max_price:
            # price must be lower than max_price
            queryset = queryset.filter(price__lt=int(max_price))

        # if date range is given
        if check_in and check_out:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

            # get reserved objects
            blocked = Reservation.objects.filter(
                Q(check_in_date__range=[check_in_date, check_out_date])
                | Q(check_out_date__range=[check_in_date, check_out_date])
                | Q(check_in_date__lte=check_in_date, check_out_date__gte=check_out_date)
            )

            # get available hotel room types objects
            blocked_hotel_room = blocked.filter(
                hotel_room__isnull=False
            ).values_list('hotel_room__id', flat=True)
            show_hotel_room_type = HotelRoom.objects.all().exclude(
                id__in=blocked_hotel_room
            ).values_list('hotel_room_type', flat=True)

            # get available apartment listing objects
            blocked_apartment_listing = blocked.filter(
                hotel_room__isnull=True
            ).values_list('listing', flat=True)
            show_apartment_listing = queryset.filter(hotel_room_type__isnull=True).exclude(
                Q(listing__in=blocked_apartment_listing)
            ).values_list('listing', flat=True)

            # filter available BookingInfo queryset
            queryset = queryset.filter(
                Q(hotel_room_type__in=show_hotel_room_type)
                | Q(listing__in=show_apartment_listing)
            )

        listing_completed = []
        items = []

        for bi in queryset:
            listing = None

            # if Hotel
            if bi.hotel_room_type:
                listing = bi.hotel_room_type.hotel

            # if Apartment
            elif bi.listing.listing_type == 'apartment':
                listing = bi.listing

            if not listing or listing.id in listing_completed:
                # no listing object found
                # or already added (hotels should display the price of the cheapest HotelRoomType with available HotelRoom.)
                # This the price of the first Hotel Room Type with a Room without blocked days in the range
                continue

            # build json
            json_data = ListingSerializer(listing).data
            json_data['price'] = str(int(bi.price))

            items.append(json_data)
            listing_completed.append(listing.id)

        return Response({'items': items})
