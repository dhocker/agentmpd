
AgendMPD - mpd web client (aka AgentMPD)
----------------------------------------

This web app is designed to manage an instance of the mpd (music player daemon) app. It will also work with
the Mopidy server (it's mpd implementation).

Files of Note
-------------

requirements.txt - pip requirements file. Can be used to create the required virtual environment.
    Note that the uwsgi file is set up for a flask virtual environment.
nginx_site - nginx configuration file for the app. This file should go in /etc/nginx/sites-available.
    To activate the site, put a symbolic link to the file in /etc/nginx/sites-enabled.
    Edit this file based on your nginx server installation. If AgentMPD is the only web app running
    under nginx, you might not need to make any changes. AgentMPD urls are all prefixed with /mpd so
    they can be routed easily within nginx. The nginx_site file does exactly this.
emperor.ini - If you want to run emperor mode, put this file in /etc/uwsgi/vassals.
uwsgi_app.ini - uwsgi configuration file for the app. This file should go in /etc/uwsgi/apps-available.
    To activate the app for non-Emperor mode, put a symbolic link in /etc/uwsgi/apps-enabled.
    For emperor mode, put this file in /etc/uwsgi/vassals.
    Edit this file based on how you set up your virtualenv. If you rename the file, make sure it ends
    with .ini otherwise uwsgi will not recognize it.
runserver.py - useful for testing the app, particularly under PyCharm. This will run the app without
    involving either nginx or uwsgi.
uwsgi-emperor - If you want to use emperor mode, put this file in /etc/init.d and register it as
    a start up daemon using update-rc.d.

NGINX
-----

The stock version of nginx that installs through apt-get is usually adequate. The mpd_web_client does not
present a heavy load.
uWSGI
-----

The stock version of uWSGI that is currently installed under Raspbian Wheezy and Jessie is usually out of date. 
It is recommended that you install the most current version of uWSGI (as identified in the requirements.txt file)
and modify the init.d script to use the version you install in a virtualenv.
