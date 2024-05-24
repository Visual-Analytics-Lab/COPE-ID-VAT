# COPE-ID-VAT

## Description

## Requirements
* pgAdmin
* WinSCP
* PuTTY  
* python >= 3.0
* pip install
   * pandas
   * django
   * psycopg2
   * psycopg2-binary
   * crispy-bootstrap4
   * django-crispy-forms
   * sqlalchemy
   * pyyaml

## Getting Started
In the terminal, navigate to:
- COPE-ID-VAT/  
  - mysite/
    - manage.py

For Windows, run:
```bash
python manage.py runserver
```
Linux:
```bash
python3 manage.py runserver
```


## Details[^note]

- mysite/ # Website folder  

   - manage.py     # Script to run Django tools for this project (created using django-admin)  

   - main/        # Website/project folder (created using django-admin)  

   - mysite/    # Application folder (created using manage.py)  

     - \_\_init\_\_.py  # Empty file that instructs Python to treat this directory as a Python package.  

     - settings.py  # Contains all the website settings, including registering any applications we create,
                     the location of our static files, database configuration details, etc.  

     - urls.py      # Defines the site URL-to-view mappings. While this could contain all the URL mapping code,
                     it is more common to delegate some of the mappings to particular applications, as you'll see later.  

     - wsgi.py      # Used to help your Django application communicate with the webserver. You can treat this as boilerplate.  

     - asgi.py      # Standard for Python asynchronous web apps and servers to communicate with each other.  
                     ASGI is the asynchronous successor to WSGI and provides a standard for both asynchronous and synchronous
                     Python apps (whereas WSGI provided a standard for synchronous apps only). It is backward-compatible with 
                     WSGI and supports multiple servers and application frameworks.  
                     
                     
## Sources:
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [jQuery](https://jquery.com/)
- [MDN HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [MDN Django](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
                     
                     
[^note]:
    Detail information from MDN Web Docs (Mozilla Developer Network).    
    Link: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
