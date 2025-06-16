# SKF-auto-quotation

## Setup the Project

```sh
mkdir SKF
git clone https://github.com/priteshtagline/SKF-auto-quotation.git
cd SKF-auto-quotation
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create .env file
```sh
cp .env.sample .env
```

### Migrate the database

```sh
python manage.py migrate
```

### Create the super user

```sh
python manage.py createsuperuser
```

The project is now running on http://127.0.0.1:8000.

