from django.urls import path
from .views import Insert, Delete, Update, displayData, inserPage


urlpatterns = [
    path('', displayData.as_view(), name="display data"), # render displayData.html page
    path('insertPage/', inserPage.as_view(), name="insertpage"), # render insert.html page
    
    path('insertData', Insert.as_view(), name="insert"), # insert Data into database
    path('updateData/', Update.as_view(), name="update"), # delete Data into database
    path('deleteData/', Delete.as_view(), name="delete"), # update Data into database
]
