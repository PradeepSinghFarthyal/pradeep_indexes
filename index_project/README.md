## Setup Environment and Insatll Dependencies:

### Install virtual enviournment
>`pip install virtualenv`

>https://www.geeksforgeeks.org/python-virtual-environment/

#### Create virtual envoiurnment

```python -m venv <env_name>```

or
    
>/usr/bin/python -m venv env
>>Ex: python -m venv env
  
#### Activate virtual envoiurnment

```source <env_name>/bin/activate```
>Ex: source env/bin/activate

  

#### Install requirements / Dependencies


>`pip install --upgrade pip`
> 
>`pip install -r requirements.txt`
> 


## Check if any grc or grpcio issue occur

	python -m pip install grpcio

>https://grpc.io/docs/languages/python/quickstart/


## Database Installation


**MySQL Installation**

>https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04

## Setup Database
Currently i'm using sql data base
so first we have to crate table and update DB redentials.


## Create DB Tables:

>`python manage.py makemigrations`
> 
`python manage.py migrate`

## Run Server:

>`python manage.py runserver`
> 
>OR
> 
>`python manage.py runserver host:port`
