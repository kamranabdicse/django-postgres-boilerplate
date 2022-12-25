# Django Rest Framework boilerplate
The MVP of our Order book in library platform.

To run this app for local development you have to provide right values for environment variables specified in '.env'
and install required python packages specified in 'requirements.txt'. You can find both files in root directory of project.

**Warning:** Remember to place values that have white space inside them between **""**

## Datbase Migrations:
- First of all you must run makemigrations and migrate
```
$ python manage.py makemigrations
```
```
python manage.py migrate
```


For enabling localization for each request we followed instructions specified in below link:

https://www.django-rest-framework.org/topics/internationalization/
- First of all you must install gettext for ubuntu
```
sudo apt-get install gettext
```
or install gettext for windows
```
https://mlocati.github.io/articles/gettext-iconv-windows.html
```
- then run
```
python3 manage.py compilemessages -l fa_IR
```
- For using celery you must install redis or rabbitmq then use
```
celery -A config worker -l info
```
