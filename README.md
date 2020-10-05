# simple_webpush_service
A simple service which implemented the functionality of web push notifications

# How to setup
1. install packages(in a python3.7 virtual envirinment)
```
pip install -r requirements.txt
```
2. set up database
```
python manage.py makemigrations
python manage.py migrate
```
3. create localhost website
```
python add_website.py
```

# How to use
1. visit `http://localhost:8000` from your favotrite browser and click on `subscribe me` button on the page
2. visit `http://localhost:8000/dashboard`, and click on `Trigger push notification for localhost` button
3. you should expect a notification popping up with a test title, a test message

