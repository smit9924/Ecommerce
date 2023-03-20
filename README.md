# Requirements
python

django

firebase_admin

google-cloud-storage

# Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation. You can do this by running the command

`python -m venv env`

After this, it is necessary to activate the virtual environment.

You can install all the required dependencies by running

`pip install -r requirements.txt`

# Structure
|Endpoints         |HTTP Method|Result     |
|------------------|-----------|-----------|
|dataApi/insertData|POST       |Insert Item|
|dataApi/deleteData|GET        |Delete Item|
|dataApi/updateData|POST|Update Item Details|
|dataApi/filterData|POST|Retrive Data|
|dataApi/getToken|GET|Get django csrf token(for testing)|

# Use
First, we have to start up Django's development server.

`python manage.py runserver`

### get CSRF TOKEN
` http://127.0.0.1:8000/dataApi/getToken`

we get

`{"csrf_token" : <CSRF TOKEN>}`

### Insert Data
type:POST

parmas:['name', 'brand', 'category', 'image(Form Image Object)'] 

`http://127.0.0.1:8000/dataApi/insertData`

we get

`{seccess: <True or False>, error:<null or error_string>}`

### Update Data
type:POST

parmas:['id', 'name', 'brand', 'category', 'image(Form Image Object)'] 

` http://127.0.0.1:8000/dataApi/updateData`

we get

`{seccess: <True or False>, error:<null or error_string>}`

### Delete Data
type:GET

parmas:['id'] 

` http://127.0.0.1:8000/dataApi/deleteData`

we get

`{seccess: <True or False>, error:<null or error_string>}`

### Retrive Data
type:POST

parmas:['category(optional)', 'brand(optional)'] 

` http://127.0.0.1:8000/dataApi/filterData`

we get

list of objects

`data: [{'name':<item name>, 'brand': <item brand>, 'category': <item category>, 'image':<item image url>}....]`
