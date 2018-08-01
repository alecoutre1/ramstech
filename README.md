# RAMSTECH


## Installation

```
cd ramstech_REST
virtualenv venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt
```
The app also needs some packages:
```
sudo apt-get install  sox ffmpeg libasound2-dev
```

Then launch the app with (preferably in a screen):

```
python3 app.py
```

The ramstech_web folder can then be placed in the website folder.
For example :

```
cp -r ramstech_web /var/www/html/
```
and then accessible via http://localhost/ramstech_web/
