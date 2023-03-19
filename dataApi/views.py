from django.shortcuts import render
from django.views import View
from dataApi.models import itemData
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime
import base64

cred = credentials.Certificate('internshipEcommerceCredentials.json')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
firebase_admin.initialize_app(cred, {'storageBucket': 'internshipecommerce-1f7ed.appspot.com'}) 

# Class to handle insert operation 
class Insert(View):
    def post(self, request, *args, **kwargs):

        # Uploading image to the firebase cloud storage
        bucket = storage.bucket()
        blob = bucket.blob(self.filenameGenerator())
        blob.upload_from_string(base64.b64decode(base64.b64encode(request.FILES.get("image").read())), content_type='image/png')
        blob.make_public()

        # Getting values from form
        name = request.POST.get("name")
        category = request.POST.get("category")
        brand = request.POST.get("brand")
        image_url = blob.public_url # url where image is stored

        # store data into database
        dataObj = itemData()
        dataObj.name = name
        dataObj.category = category
        dataObj.brand = brand
        dataObj.image = image_url
        dataObj.save()


        return JsonResponse({"success":"True"})
    
    def filenameGenerator(self):
        cdt = datetime.now()
        return (str(cdt.year) + str(cdt.month) + str(cdt.day) + str(cdt.hour) + str(cdt.minute) + str(cdt.second))

# Class to handle delete operation
class Delete(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")

# Class to handle update operation
class Update(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        id = request.GET.get("name")
        id = request.GET.get("category")
        id = request.GET.get("brand")
        id = request.GET.get("image")


# Class to render Display Data Page
class displayData(View):
    template_name = 'dataApi/displayData.html'

    def get(self, request):
        return render(request, self.template_name)
    
# Class to render Insert Data Page
class inserPage(View):
    template_name = 'dataApi/insert.html'

    def get(self, request):
        return render(request, self.template_name)