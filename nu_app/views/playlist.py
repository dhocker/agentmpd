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
# A reasonable attempt was made to design this part of the app along the lines of REST.
# The following collections are involved.
#   - The current playlist is a collection of songs/tracks/URIs.
#   - Named/stored playlists
#   - Albums
#
# The following records/members/elements are involved.
#   - Tracks/songs/URIs

from nu_app import app
from nu_app.models.playlist import Playlist
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify
import json

#  MPD music player model instance
playlist = Playlist()


@app.route("/cpl/playlist", methods=['DELETE'])
def clear_playlist():
    """
    Remove all entries from the current playlist (collection).
    :return:
    """
    playlist.clear()
    return ""


@app.route("/cpl/managecurrentplaylist", methods=['GET'])
def manage_playlist():
    """
    Show the manage current playlist page.
    :return:
    """
    return render_template("manage_playlist.html", ngapp="agentmpd", ngcontroller="playlistController")


@app.route("/cpl/currentplaylist", methods=['GET'])
def get_current_playlist():
    pl = playlist.get_current_playlist()
    return jsonify(**pl)


@app.route("/cpl/namedplaylists", methods=['GET'])
def get_all_named_playlists():
    """
    Return a collection of named/stored playlists.
    If a search/query parameter ("s") is provided, the
    queried playlists are returned. Otherwise, all
    playlists are returned.
    :return:
    """
    if len(request.args) > 0:
        all_playlists = playlist.search_for_playlists(request.args["s"])
    else:
        all_playlists = playlist.get_playlists()

    return jsonify({"playlists": all_playlists})


@app.route("/cpl/artists", methods=['GET'])
def get_artists():
    """
    Return a collection of artists.
    If a search/query parameter ("s") is provided, the
    queried artists are returned. Otherwise, all
    artists are returned.
    :return:
    """
    if len(request.args) > 0:
        #all_artists = playlist.search_for_playlists(request.args["s"])
        all_artists = []
    else:
        all_artists = playlist.get_artists()

    return jsonify({"artists": all_artists})


@app.route("/cpl/playlist", methods=['POST'])
def append_stored_playlists():
    """
    Append to the current playlist the contents of one or more stored playlists.
    The request data contains an object/dict identfifying the playlists to be appended.
    :return:
    """
    args = json.loads(request.data.decode())["data"]
    if "playlists" in args:
        for pl in args["playlists"]:
            playlist.load_playlist(pl)
    elif "uris" in args:
        for uri in args["uris"]:
            playlist.add_track(uri)
    return ""


@app.route("/cpl/playlistentry", methods=['DELETE'])
def remove_playlist_entries():
    """
    Remove one or more entries from the current playlist.
    The request data is an array of songids
    to be removed from the current playlist.
    :return:
    """
    songids = json.loads(request.data.decode())
    for songid in songids:
        playlist.remove_by_songid(songid)
    return ""


@app.route("/cpl/albums", methods=['GET'])
def get_all_albums():
    """
    Get albums in the library. If there are search args, the list of
    albums returned will be based on queries using the search args.
    :return:
    """
    if len(request.args) > 0:
        if "album" in request.args:
            # Query for albums
            all_albums = playlist.search_for_albums(request.args["album"])
        elif "artist" in request.args:
            # Query for albums by artist
            all_albums = playlist.search_for_albums_by_artist(request.args["artist"])
        elif "artists" in request.args:
            # Query for albums by artist(s)
            artists = json.loads(request.args["artists"])
            if type(artists) != list:
                artists = [request.args["artists"]]
            all_albums = []
            for artist in artists:
                albums = playlist.search_for_albums_by_artist(artist)
                for a in albums:
                    all_albums.append(a)
    else:
        all_albums = playlist.get_albums()

    all_albums.sort()
    return jsonify({"albums": all_albums})


@app.route("/cpl/album/tracks", methods=['GET'])
def get_album_tracks():
    """
    Get the tracks contained in one or more albums.
    The request data is an array of album titles.
    :return:
    """
    all_tracks = []
    # args is a dict of album titles (the key is an array index).
    for index, album_title in request.args.iteritems():
        album_tracks = playlist.get_album_tracks(album_title)
        for t in album_tracks:
            all_tracks.append({"title":t["title"], "uri":t["file"]})
    return jsonify({"tracks": all_tracks})


@app.route("/cpl/tracks", methods=['GET'])
def search_for_tracks():
    """
    Search for tracks.
    :return:
    """
    if len(request.args) > 0:
        if "track" in request.args:
            # Query for tracks
            tracks = playlist.search_for_tracks(request.args["track"])
    else:
        tracks = []

    return jsonify({"tracks": tracks})


@app.route("/cpl/namedplaylists", methods=['POST'])
def save_named_playlist():
    """
    Save the current playlist as a named playlist
    (add current playlist to the collection of named playlists).
    The request data contains the name for the new named playlist.
    :return:
    """
    # args is the name for the saved playlist
    args = json.loads(request.data.decode())
    playlist.save_current_playlist(args["data"]["name"])
    return ""
