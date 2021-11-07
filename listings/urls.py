from django.conf.urls import url, include

urlpatterns = [
	url(r'^v1/', include(('listings.v1.urls', 'listings_v1'), namespace='listings_v1')),
]
