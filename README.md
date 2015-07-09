# Twittex 

##What is Twittex?

Twittex is a short messaging service (similar to Twitter) with finer privacy settings for use in a university environment. For a feature list check out our Github Wiki page.
<img src="https://cloud.githubusercontent.com/assets/11362357/8591885/8a5f930e-262b-11e5-8d19-e56cc82e9ef8.png"></img>

##Guide to install Twittex

1. Install Python
2. Install Django
3. Install Pip
4. Install Pillow via Pip (`$pip install pillow`)
5. Install Pyscss via Pip (`$pip install python-pyscss`)
6. Download this repo (`$git clone https://github.com/patreu22/Twittex/`)
7. Install PostgreSQL (Easy going for Mac: http://postgresapp.com/de/ , for other OS you have to take a deeper look)
8. Run PostgreSQL
9. Open PostgreSQL with `$psql`
10. Run `CREATE USER django PASSWORD 'django'`
11. Run `CREATE DATABASE twittex_db OWNER django;`
12. Run `$python manage.py migrate auth`
13. Run `$python manage.py migrate`
14. Start Twittex with `$python manage.py runserver`locally. For making it accessible over your IP for everybody use `$python manage.py runserver 0.0.0.0:8000`


	
  
Enjoy ;-)  
  
  
