Link to site:
https://sherin-khaira-willspbpsiteorwhatever.pbp.cs.ui.ac.id/


TUGAS 4:
1.


TUGAS 2:
1. I followed most of the tutorial but found a /TemplateNotFound error which is fixed by adding 'main' to the INSTALLED_APPS variable within football_news/settings.py

2. Client Request -> urls.py (wills-pbp-site-or-whatever) -> (if valid endpoint) go to include('main.urls') -> urls.py (main)

3. A general configuration file. Most web frameworks have one. They contain settings for things like language, a base url for static files (img, videos, etc), production databases once you get to that, apps that are within this django project, etc. I honestly wish we used Next.JS instead, its so much more simple and fast, other than teaching the students how to use React which is a must in today's web development world.

4. Migrations is a feature so you can keep your database schema in tune with your python models. For example, a model Article gets a new attribute which is datePublished. The codebase will not detect this change until you scan it with python manage.py makemigrations and python manage.py migrate

5. Probably cause python is the "basic" learning language of early semesters, django also happens to be in python. If it wasn't, the other students who don't code outside of school would be left behind. Although i prefer javascript and typescript (because of many features such as autocomplete, linting, and keeping maintainability when the project goes very large). Python isn't the fastest programming language and Next.JS likely wins in simplicity and support, especially with the use of React and JSX/TSX.

6. Use NextJS :P