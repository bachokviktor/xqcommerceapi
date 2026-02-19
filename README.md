# XQCommerceAPI

Simple e-commerce system API built with Django REST Framework.

## Installation

**Note:** It is recommended that you use PostgreSQL database for this project,
otherwise you will have to modify `settings.py`.

Clone the repository

``` bash
git clone https://github.com/bachokviktor/xqcommerceapi.git && cd xqcommerceapi
```

Create a virtual environment

``` bash
python -m venv venv
```

Activate it

``` bash
source venv/bin/activate
```

Install dependencies

``` bash
pip install -r requirements.txt
```

Set the environent variables in `.env.example` and rename it to `.env`

``` bash
mv .env.example .env
```

Run migrations

``` bash
python manage.py migrate
```

Run the development server

``` bash
python manage.py runserver
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
