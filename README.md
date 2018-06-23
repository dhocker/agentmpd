# AgentMPD
Copyright © 2015, 2018 by Dave Hocker

## Overview

AgentMPD is a web server based client app for the [mpd](http://www.musicpd.org) music server.
It will also work with the [Mopidy](https://www.mopidy.com/) music server.
It will allow you to control one running instance of mpd from any web browser (it has been tested
with Chrome, Firefox, Firefox Developer Edition and Brave).

AgentMPD was written in Python/Flask to run on a light weight system (e.g. a Raspberry Pi).
While the server app was designed to run on a lightweight system, it will run on any system that
supports Python 3.6 (including Windows) and the Flask framework. The mpd music server can be running
anywhere as long as you can get to it via a TCP/IP connection.

AgentMPD is open source. Anyone can fork it and build upon it.

## License

The AgentMPD app is licensed under the GNU General Public License v3 as published by the Free Software Foundation, Inc.. See the
LICENSE file for the full text of the license.

## Source Code

The full source is maintained on [GitHub](https://www.github.com/dhocker/agentmpd).

## Build Environment

AgentMPD was originally written in Python 2.7 and subsequently migrated to Python 3.6.
While it will still run on Python 2.7, support for that version will be
dropped in the near future. Only Python 3.6+ will be supported going forward.

AgendtMPD uses the popular Flask framework.

A suitable development environment would use virtualenv and virtualenvwrapper to create a working virtual environment.
The requirements.txt file can be used with pip to create the required virtual environment with all dependencies.

The following steps should provide a working installation.

1. Clone the source repository from GitHub into a project directory of your choice.
1. Create a virtual environment using virtualenv and virtualenvwrapper.

   * To create: mkvirtualenv -r requirements.txt agentmpd
   * To activate: workon agentmpd
   * You can use the -a option of mkvirtualenv to automatically switch to the correct venv when you enter the 
project directory.

1. You can run the web app from the project directory using: python runserver.py
1. If you use PyCharm as your IDE you can set up a test configuration that starts runserver.py.

AgentMPD was developed using PyCharm CE. PyCharm CE is highly recommended. However, a good text editor
of your choice is all that is really required.

## Configuration

All configuration is done through the Settings page of the web app. The only setting that usually requires change is the
hostname or IP address of the mpd music server. You can get to the settings page by going to the home page
(e.g. http://localhost:5000/mpd) and clicking on the Settings menu item.

## Running as an Application

You can run AgentMPD as an application as follows.

1. If you are using virtualenv, activate the environment you set up: workon mpd_web_client
2. Then: python runserver.py

## Running Under a Web Server

AgentMPD can be run under a web server (e.g. nginx) using the uWSGI gateway. The top project directory
contains a uwsgi.py and several configuration files to facilitate this choice. Readme.txt descibes the
various configuration files for nginx and uWSGI.

The following links discuss the details of setting up nginx and uWSGI to run a Python/Flask web application.

* [serving-flask-with-nginx-on-ubuntu](http://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/)
* [how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04)
