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
from nu_app.models.playlist import Playlist
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify

#  MPD music player model instance
playlist = Playlist()


@app.route("/playlist/clear", methods=['PUT'])
def playlist_clear():
    playlist.clear()
    return ""
