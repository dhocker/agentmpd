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
import json

#  MPD music player model instance
playlist = Playlist()


@app.route("/playlist/clear", methods=['PUT'])
def playlist_clear():
    playlist.clear()
    return ""


@app.route("/playlist/manage", methods=['GET'])
def playlist_manage():
    return render_template("manage_playlist.html", ngapp="agentmpd", ngcontroller="playlistController")


@app.route("/playlist/all", methods=['GET'])
def playlist_all():
    all_playlists = playlist.get_playlists()
    return jsonify({"playlists": all_playlists})


@app.route("/playlist/load_selected", methods=['POST'])
def playlist_load_selected():
    args = json.loads(request.data.decode())
    for pl in args["playlists"]:
        playlist.load_playlist(pl)
    return ""


@app.route("/playlist/remove_selected", methods=['POST'])
def playlist_remove_selected():
    # args is a list of songids to be removed from the current playlist
    args = json.loads(request.data.decode())
    for songid in args["songids"]:
        playlist.remove_by_songid(songid)
    return ""


@app.route("/playlist/albums", methods=['GET'])
def playlist_get_albums():
    all_albums = playlist.get_albums()
    all_albums.sort()
    return jsonify({"albums": all_albums})


@app.route("/playlist/album_tracks", methods=['POST'])
def playlist_get_album_tracks():
    all_tracks = []
    # args is a list of album titles
    args = json.loads(request.data.decode())
    for album_title in args["albums"]:
        album_tracks = playlist.get_album_tracks(album_title)
        for t in album_tracks:
            all_tracks.append({"title":t["title"], "uri":t["file"]})
    return jsonify({"tracks": all_tracks})


@app.route("/playlist/load_tracks", methods=['POST'])
def playlist_add_tracks():
    # args is a list of uri's to be added to the current playlist
    args = json.loads(request.data.decode())
    for uri in args["tracks"]:
        playlist.add_track(uri)
    return ""


@app.route("/playlist/save", methods=['POST'])
def playlist_save():
    # args is the name for the saved playlist
    args = json.loads(request.data.decode())
    playlist.save_current_playlist(args["name"])
    return ""
