# Twittex  

Get it work:  

1) Install Django  
2) Install PostgreSQL (Easy going for Mac: http://postgresapp.com/de/)  
3) Set up the Database:  
   a) Enter psql console by terminal  
      # CREATE USER django;  
   b) After that enter following:  
      # CREATE DATABASE twittextestdb OWNER django;  
    
(Guide reference: http://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/optional_postgresql_installation/README.html)  
  
  
Start it:  
1) Run Postgresql with user: django pw: django and db: twittex_db
2) Start App with

	($python manage.py createsuperuser)
	
	$python manage.py migrate
	
	$python manage.py runserver	
	
  
Enjoy ;-)  
  
  
