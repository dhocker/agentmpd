#!/usr/bin/python

#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014, 2015  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#
# To start the web server:
#   workon flask-env            # Establish working virtual environment with Flask
#   python runserver.py

from nu_app import app
#import configuration
#import Logging
#import logging


if __name__ == "__main__":

    app.run('0.0.0.0', debug=True)

    #logger = logging.getLogger("app")

    #logger.info("AHPS_Web ended")
    #logger.info("################################################################################")
    #Logging.Shutdown()

