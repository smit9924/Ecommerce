from django.shortcuts import render
from django.views import View
from dataApi.models import itemData
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime
import base64
import json

cred = credentials.Certificate('internshipEcommerceCredentials.json')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
firebase_admin.initialize_app(cred, {'storageBucket': 'internshipecommerce-1f7ed.appspot.com'}) 

# Class to handle insert operation 
class Insert(View):
    def post(self, request):
        try:
            self.insertData(self, request)
            response = {
                "success": True
            }
        except Exception:
            response = {
                "success":False,
                "error": Exception 
            }

        return JsonResponse({"Success":True})
    
    def filenameGenerator(self):
        '''
        input: this function take no input
        output: unique string which never collied with each other
        '''
        cdt = datetime.now()
        return (str(cdt.year) + str(cdt.month) + str(cdt.day) + str(cdt.hour) + str(cdt.minute) + str(cdt.second))

    def uploadImage(self, request):
        '''
        input: 
                request: Object of request
        output: 
                return PUBLIC URL of firebase cloud where image is stored
        '''
        bucket = storage.bucket()
        blob = bucket.blob(self.filenameGenerator())
        blob.upload_from_string(base64.b64decode(base64.b64encode(request.FILES.get("image").read())), content_type='image/png')
        blob.make_public()
        return blob.public_url
    
    def insertData(self, request):
        '''
        params: 
                request : object of request
                imgUrl: url of firebase storage where image is stored
        output: 
                boolean(True or False)
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
        try:
            Obj = itemData.objects.filter(id = request.GET.get('id'))

            if Obj == None:
                raise Exception("Bad request! Invalid ID!")
            else:
                bucket = storage.bucket()
                blob = bucket.blob(Obj.image)
                blob.delete
                response = {
                    "success":True
                }
        except Exception:
            response = {
                "success": False,
                "error": Exception
            }
        
        return JsonResponse(response)


# Class to handle update operation
# class Update(View):
#     def POST(self, request, *args, **kwargs):
#         dataObj = itemData.objects.filter(id=request.GET.get('id'))
#         try: 
#             if id == None:
#                 raise Exception("Bad request! Invalid ID!")
#             else:
#                 self.updateValues(dataObj, request)
#                 response = {
#                     "success": True
#                 }

#         except Exception:
#             response = {
#                 "success":False,
#                 "error": Exception
#             }
        
#         return JsonResponse(response)

#     def updateValues(self, dataObj, request):
#         '''
#         params:
#                 dataObj: Object of database
#                 request: object of POST request
#         output: 
#                 Boolean
#         '''
# Class to handle insert operation 
class Update(View):
    def post(self, request, *args, **kwargs):
        dataObj = itemData.objects.filter(id=request.POST.get('id'))
        try:
            if dataObj == None:
                raise Exception("Bad request! Invalid ID!!!")
            else:
                self.updateData(self, dataObj, request)
                response = {
                    "success": True
                }
        except Exception:
            response = {
                "success":False,
                "error": Exception 
            }

        return JsonResponse(response)
    
    def filenameGenerator(self):
        '''
        input: this function take no input
        output: unique string which never collied with each other
        '''
        cdt = datetime.now()
        return (str(cdt.year) + str(cdt.month) + str(cdt.day) + str(cdt.hour) + str(cdt.minute) + str(cdt.second))

    def uploadImage(self, request):
        '''
        input: 
                request: Object of request
        output: 
                return PUBLIC URL of firebase cloud where image is stored
        '''
        bucket = storage.bucket()
        blob = bucket.blob(self.filenameGenerator())
        blob.upload_from_string(base64.b64decode(base64.b64encode(request.FILES.get("image").read())), content_type='image/png')
        blob.make_public()
        return blob.public_url
    
    def updateData(self, dataObj, request):
        '''
        params: 
                dataObj: Object of database
                request : object of request
        output: 
                boolean(True or False)
        '''
        dataObj.name = request.POST.get("name")
        dataObj.category = request.POST.get("category")
        dataObj.brand = request.POST.get("brand")
        dataObj.image = self.uploadImage(request)
        dataObj.save()


# Class to render Display Data Pag
class displayData(View):
    template_name = 'dataApi/displayData.html'

    def get(self, request):
        return render(request, self.template_name)
    
# Class to render Insert Data Page
class inserPage(View):
    template_name = 'dataApi/Insert.html'

    def get(self, request):
        return render(request, self.template_name)