### News app
## Database: postgres
## Setup
# Tạo env, install thư viện:
```
pip install -r requirements.txt
```

# Setup database trong file settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crawl_data',
        'USER': 'bdsg',
        'PASSWORD': 'bdsg',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

# Run app:
```
python manage.py runserver
```

# Migrate database:
```
python manage.py migrate
```

# Tạo super user:
```
python manage.py createsuperuser
```
# Crawl data:
```
cd api
python crawl.py
```
# Import file postman.json vào postman, test các API