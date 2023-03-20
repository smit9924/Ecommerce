from django.urls import path
from .views import Insert, Delete, Update, GetCSRFToken,Filter

urlpatterns = [
    path('getToken/', GetCSRFToken.as_view(), name="token"), # get CSRF token

    path('insertData', Insert.as_view(), name="insert"), # insert Data into database
    path('updateData', Update.as_view(), name="update"), # delete Data into database
    path('deleteData/', Delete.as_view(), name="delete"), # update Data into database
    path('filterData', Filter.as_view(), name="filter"), # Retrive Data By Filtering
]
