# COPE-ID-VAT

## Description

## Requirements
* PostgreSQL version 16.x
* pgAdmin 4
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
### Running Locally (non-internal users)
This will be updated in the future with more specifics, but at a minimum you will need to have all of the above requirements installed. Once PostgreSQL is installed and configured, install pgAdmin 4. Launch pgAdmin 4, right click Servers -> Register -> Server. Give the server a name. Go to the Connection tab and set the Host name/address to localhost. Leave the port as 5432. If you configured postgres to use postgres as the username the leave the username and maintenance database values the same. If you would like, you can right click on the server instance that was just created and create another database for the sample data and all django app specific data for the tool. TODO: The insert_sample_data_postgres.py script will need several alterations to run and upload the documents in test_main_sample_data.json to the main_sample_data table.

### Running as Internal Team member:
You should all be added to the correct departmental VPN. If unable to connect, reach out to IT. You will need to have PuTTY installed on your local machine and make the following changes to your connection within PuTTY: Go to Connection -> SSH and set the source port 8000. Set the destination to 127.0.0.1:8000. Click Add. You should see those values in the above box. Be sure to save your changes/connection so you will not have to do this every time. This change allows you to browse to the server hosted on the VM that you are connecting to via PuTTY.

In the VM terminal, navigate to:
- /home/shared/repos/COPE-ID-VAT/mysite/
- activate the python virtual environment with ```. /home/shared/venv/bin/activate``` (you should see (venv) next to your name on the command line in the terminal)
- run ```python manage.py runserver``` to start the server and you should see something similar to the below image

-   ![image](https://github.com/Visual-Analytics-Lab/COPE-ID-VAT/assets/46544893/a41cd3db-a71d-4176-9dec-d4cf803a9639)
- go to your local browser and enter http://127.0.0.1:8000 to view the tool


## Details[^note]

- mysite/ # Website folder  

   - manage.py     # Script to run Django tools for this project (created using django-admin)  

   - main/        # Website/project folder (created using django-admin)  

   - mysite/    # Application folder (created using manage.py)  

     - \_\_init\_\_.py  # Empty file that instructs Python to treat this directory as a Python package.
       
     - config.yml  # This file is not in the repo as it contains specific database and user information such as passwords.
                     The file should follow the below template exactly and updated with the correct values.
 
             secret_key:
                key: <django-secret-key>
             databases:
                name: <database_name>
                user: <user_name>
                password: <password>
                host: 127.0.0.1
                port: 54322
       
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
