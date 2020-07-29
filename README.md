# CaRental
A car rental website built with Django.

***

### Usage:
- `git clone https://github.com/Badredine-Kheddaoui/carental`

- `pip install -r requirements.txt`

- `python manage.py makemigrations`

- `python manage.py migrate`

- `python manage.py runserver`

- go to 'http://127.0.0.1:8000/'

****

### Tech stack
- Django on the server side
- jQuery and Bootstrap for responsiveness
- AJAX/Django communication to update parts of the page according to the database without refreshing the whole page

***

### Features
- A custom user model thet extends the default Django's with more functionality.
- An admin panel to add, update and delete users, restaurants, products and managing orders.
- The content(restaurants rating, reviews and products) is dynamic and changes according to the database
- Since most HTML pages have similar sections(shopping cart, navbar, footer...), They all extend a base HTML page.

***

### Security Measures
- User passwords are hashed before saved in the database.
- Protection against Cross Site Request Forgeries by sending the user a token that has to be returned when submitting the form.
- Input fields are sanitized to prevent JavaScript injections.
- Database queries are protected from SQL injection by using query parameterization.
