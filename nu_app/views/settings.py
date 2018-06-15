#
# AgentMPD - web app for controlling an mpd instance
# Copyright (C) 2015, 2018  Dave Hocker (email: AtHomeX10@gmail.com)
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
from nu_app.views.views import reset_player
from nu_app.models.settings import Settings
from nu_app.views.url_utils import url_with_prefix
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify
import json


@app.route(url_with_prefix("/settings_page"), methods=['GET'])
def settings_page():
    return render_template("settings.html", host="raspberrypi-fs", ngapp="agentmpd", ngcontroller="settingsController")


@app.route(url_with_prefix("/settings"), methods=['GET'])
def get_settings():
    # Return current settings
    return jsonify(Settings.get())


@app.route(url_with_prefix("/settings"), methods=['PUT'])
def save_settings():
    # Save settings
    args = json.loads(request.data.decode())
    Settings.save(args["data"])
    reset_player()
    return ""