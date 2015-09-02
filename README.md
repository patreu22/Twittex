# Twittex 
Twittex is a short messaging service (similar to Twitter) with finer privacy settings for use in a university environment. For a feature list check out our Github Wiki page.

<img src="https://cloud.githubusercontent.com/assets/11362357/8591885/8a5f930e-262b-11e5-8d19-e56cc82e9ef8.png"></img>

##Guide to install Twittex

1. Install Python
2. Install Pip
3. Install Django
4. Install Git
5. Install Pillow via Pip (`$pip install pillow`)
6. Install Pyscss via Pip (`$pip install pyscss`)
7. Install Psycopg2 
7. Download this repo (`$git clone https://github.com/patreu22/Twittex/`)
8. Install PostgreSQL (Easy going for Mac: http://postgresapp.com/de/ , for other OS you have to take a deeper look)
9. Run PostgreSQL
10. Open PostgreSQL with `$psql`
11. Run `CREATE USER django PASSWORD 'django'`
12. Run `CREATE DATABASE twittex_db OWNER django;`
13. Close Postgres and run `$python manage.py migrate auth` in manage.py folder of the Django Project
14. Run `$python manage.py migrate`
15. Start Twittex with `$python manage.py runserver`locally. For making it accessible over your IP for everybody use `$python manage.py runserver 0.0.0.0:8000`


That is the instruction for installing Twittex on a (Amazon) Ubuntu machine, for other systems you have to update the path for file storing in the settings.py.
  
Enjoy ;-)  
  
  
