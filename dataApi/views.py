from django.shortcuts import render, HttpResponse
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
    '''
    <API Name>: Add New Item

    Dependencies:
    - firebase_admin
    - base64
    - datetime
    - itemData model (custom)

    Params:
    - name (string): name of the item
    - brand (string): brand of the item
    - category (string): category of the item
    - image (binary): binary representation of the image to be uploaded

    Response:
    - success (boolean): indicates whether the data was successfully inserted into the database or not
    - error (string): contains the error message in case of failure
    '''
    def post(self, request, *args, **kwargs):
        try:
            self.insertData(request)
            response = {
                "success": True
            }
        except Exception as e:
            response = {
                "success":False,
                "error": e 
            }

        return JsonResponse(response)
    
    def filenameGenerator(self):
        '''
        Params: None
        Output: unique string
        '''
        cdt = datetime.now()
        return (str(cdt.year) + str(cdt.month) + str(cdt.day) + str(cdt.hour) + str(cdt.minute) + str(cdt.second))

    def uploadImage(self, request):
        '''
        Params:
        - request: Object of request

        Output: The public URL of the uploaded image in Firebase Storage.
        '''
        bucket = storage.bucket()
        blob = bucket.blob(self.filenameGenerator())
        blob.upload_from_string(base64.b64decode(base64.b64encode(request.FILES.get("image").read())), content_type='image/png')
        blob.make_public()
        print(blob.public_url)
        return blob.public_url
    
    def insertData(self, request):
        '''
        Params:
        - request: Object of request

        Output: None
        '''
        dataObj = itemData()
        dataObj.name = request.POST.get("name")
        dataObj.category = request.POST.get("category")
        dataObj.brand = request.POST.get("brand")
        dataObj.image = self.uploadImage(request)
        dataObj.save()

# Class to handle delete operation
class Delete(View):
    '''
    <API Name>: Delete Item

    Dependencies:
    - firebase_admin
    - itemData model (custom)

    Request Method: GET

    Request Parameters:
    - id (integer): the id of the item to be deleted

    Response:
    - success (boolean): indicates whether the item was successfully deleted from the database or not
    - error (string): contains the error message in case of failure
    '''
    def get(self, request, *args, **kwargs):
        Obj = itemData.objects.filter(id = request.GET.get('id'))
        response = self.deleteData(Obj)
        return JsonResponse(response)
    
    def deleteData(self, Obj):
        '''
        Params:
        - Obj: Object of itemData model to be deleted from the database.

        Output:
        - response: a dictionary containing two parameters:
            - success (boolean): indicates whether the data was successfully deleted or not.
            - error (string): contains the error message in case of failure.

        '''
        try:
            if Obj.exists():
                try:
                    bucket = storage.bucket()
                    public_url = Obj.values('image').get()['image'] 
                    blob = bucket.blob(public_url.split('?')[0].split('/')[-1])
                    if blob.exists():
                        blob.delete()
                    Obj.delete()
                    response = {
                        "success":True
                    }
                except Exception as e:
                    return JsonResponse({"success": False, "error": str(e)})
            else:
                raise Exception("Bad request! Item with specified ID doesn't exist!!!")
                
        except Exception as e:
            response = {
                "success": False,
                "error": str(e)
            }
        
        return response


# Class to handle insert operation 
class Update(View):
    '''
    <API Name>: Update Item Data

    Dependencies:
    - Firebase Admin
    - Firebase Cloud Storage
    - itemData model from database

    Params:
    - id (int): ID of the item to be updated
    - name (str, optional): Name of the item
    - category (str, optional): Category of the item
    - brand (str, optional): Brand of the item
    - image (file, optional): Image of the item to be updated

    Response:
    - success (bool): True if the data is updated successfully, False otherwise
    - error (str, optional): Error message if the data update fails
    '''
    def post(self, request, *args, **kwargs):
        dataObj = itemData.objects.get(id=request.POST.get('id'))
        try:
            if dataObj != None:
                self.updateData(dataObj, request)
                response = {
                    "success": True
                }

            else:
                raise Exception("Bad request! Item with specified ID doesn't exist!!!")
        except Exception as e:
            response = {
                "success":False,
                "error": str(e) 
            }

        return JsonResponse(response)
    
    def filenameGenerator(self):
        '''
        Params: None
        Output: unique string
        '''
        cdt = datetime.now()
        return (str(cdt.year) + str(cdt.month) + str(cdt.day) + str(cdt.hour) + str(cdt.minute) + str(cdt.second))

    def uploadImage(self, request):
        '''
        Params:
        - request: Object of request

        Output: The public URL of the uploaded image in Firebase Storage.
        '''
        bucket = storage.bucket()
        blob = bucket.blob(self.filenameGenerator())
        blob.upload_from_string(base64.b64decode(base64.b64encode(request.FILES.get("image").read())), content_type='image/png')
        blob.make_public()
        return blob.public_url
    
    def updateData(self, dataObj, request):
        '''
        Parameters:
        - dataObj: Object of the model to be updated
        - request: Object of the request containing the data to be updated

        Output: None
        '''
        
        if "name" in request.POST:
            dataObj.name = request.POST.get("name")
        if "category" in request.POST:
            dataObj.category = request.POST.get("category")
        if "brand" in request.POST:
            dataObj.brand = request.POST.get("brand")
        if 'image' in request.FILES: 
            self.deleteImage(dataObj)
            dataObj.image = self.uploadImage(request)
        dataObj.save()
    
    def deleteImage(self, dataObj):
        '''
        Parameters:
        - dataObj: object of model which is going to be updated

        Output:
        - void
        '''
        bucket = storage.bucket()
        public_url = dataObj.values('image').get()['image'] 
        blob = bucket.blob(public_url.split('?')[0].split('/')[-1])
        if blob.exists():
            blob.delete()