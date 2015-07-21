#
# AgentMPD - web app for controlling an mpd instance
# Copyright (C) 2015  Dave Hocker (email: AtHomeX10@gmail.com)
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
from nu_app import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify
import json


@app.route("/settings_page", methods=['GET'])
def settings_page():
    if request.method == 'GET':
        return render_template("settings.html", host="raspberrypi-fs")
    return ""


@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        # Return current settings
        return jsonify({'host': "localhost", 'port': 6600})
    elif request.method == 'POST':
        # Save settings
        args = json.loads(request.data.decode())
        print args["host"]
        print args["port"]
        return ""