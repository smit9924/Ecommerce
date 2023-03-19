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
        self.insertData(self, request)
        return JsonResponse({"success":"True"})
    
    def filenameGenerator(self):
        '''
        input: this function take no input
        output: unique string which never collied with each other
        '''
        cdt = datetime.now()
        return (str(cdt.year) + str(cdt.month) + str(cdt.day) + str(cdt.hour) + str(cdt.minute) + str(cdt.second))

    def uploadImage(self, request):
        '''
        input: request: Object or request
        output: return public url of firebase cloud where image is stored
        '''
        bucket = storage.bucket()
        blob = bucket.blob(self.filenameGenerator())
        blob.upload_from_string(base64.b64decode(base64.b64encode(request.FILES.get("image").read())), content_type='image/png')
        blob.make_public()
        return blob.public_url
    
    def insertData(self, request, imgUrl):
        '''
        input: request : object of request
               imgUrl: url of firebase storage where image is stored
        output: boolean(True or False)
        '''
        dataObj = itemData()
        dataObj.name = request.POST.get("name")
        dataObj.category = request.POST.get("category")
        dataObj.brand = request.POST.get("brand")
        dataObj.image = self.uploadImage(request)
        dataObj.save()

# Class to handle delete operation
class Delete(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")

# Class to handle update operation
class Update(View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        name = request.GET.get("name")
        category = request.GET.get("category")
        brand = request.GET.get("brand")



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