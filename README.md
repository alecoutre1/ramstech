# RAMSTECH


## Installation

```
cd ramstech_REST
virtualenv venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt
```
The app also needs soundfile sox and ffmpeg to work:
```
sudo apt-get install soundfile sox ffmpeg libasound2-dev
```


## Application setup
### Local setup

To test locally, uncomment the line in ramstech_web/js/app.js to set URL='http://localhost:4444/'

Then : 
```
cd ramstech_REST
python3 app.py
```

In a different screen or window :

```
cd ramstech_web
python3 -m http.server 8000
```

### Web server setup

To test on web server, keep the line in ramstech_web/js/app.js to set URL='../php/ajax.php'

Then :

```
cd ramstech_REST
python3 app.py
```

You can then place the folder in your web container and access it from outside..


