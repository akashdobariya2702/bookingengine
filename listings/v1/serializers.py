# python library

# django library
from rest_framework import serializers

# plugin library

# project library
from listings.models import *


class ListingSerializer(serializers.ModelSerializer):
    listing_type = serializers.CharField(
        source='get_listing_type_display'
    )

    class Meta:
        model = Listing
        exclude = ('id', )
