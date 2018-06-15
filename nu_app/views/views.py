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
#from nu_app.models.key_value_store import KVStore
from nu_app.models.player import Player
from nu_app.views.url_utils import url_with_prefix
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify
import json

#  MPD music player model instance
player = Player()

@app.route(url_with_prefix("/"))
def root():
    """
    Redirect to the effective home page of the app.
    :return:
    """
    return redirect(url_for('mpd_player'))


@app.route(url_with_prefix("/player"), methods=['GET'])
def mpd_player():
    """
    Show the MPD player page.
    :return:
    """
    return render_template('player.html', ngapp="agentmpd", ngcontroller="homeController")


@app.route(url_with_prefix("/player/currentstatus"), methods=['GET'])
def get_current_status():
    """
    Return the current player status.
    :return:
    """
    current_status = player.get_current_player_status()
    if "pos" in current_status:
        current_status["pos1"] = int(current_status["pos"]) + 1
    else:
        current_status["pos1"] = ""
    return jsonify(**current_status)


@app.route(url_with_prefix("/player/currentsong/<pos>"), methods=['PUT'])
def play_song(pos):
    """
    Make the current song be current playlist[pos].
    The value of pos can be first, previous, next, last or nnn (a number).
    :param pos:
    :return:
    """
    try:
        n = int(pos)
        player.play(n)
    except:
        # The new song is not a position number (0-n)
        if pos == "first":
            play_first();
        elif pos == "previous":
            play_previous()
        elif pos == "next":
            play_next()
        elif pos == "last":
            play_last()

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route(url_with_prefix("/player/nextsong/<id>"), methods=['PUT'])
def queue_song(id):
    """
    Queue a song to be played next. The id is the songid, not the song position.
    :param id:
    :return:
    """
    try:
        n = int(id)
        player.queue(n)
    except:
        pass

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route(url_with_prefix("/player/status"), methods=['PUT'])
def update_player_status():
    """
    Update the player status. New status keys can be
    playstatus - values can be toggle, play or stop.
    random - 0 or 1
    sonsume - 0 or 1
    repeat - 0 or 1
    single - 0 or 1
    :return:
    """
    new_status_kv = json.loads(request.data)

    if "playstatus" in new_status_kv:
        new_status = new_status_kv["playstatus"]
        current_status = player.get_current_player_status()

        if new_status == "toggle":
            if current_status['state'] == 'play':
                player.pause(1)
            elif current_status['state'] == 'pause':
                player.pause(0)
            elif current_status['state'] == 'stop':
                # If there is a song in the current status, we'll start
                # playing it. Otherwise, we'll arbitrarily play the first song.
                if "song" in current_status:
                    player.play(current_status['song'])
                else:
                    player.play(0)
        elif new_status == "play":
            player.play(current_status['song'])
        elif new_status == "stop":
            player.stop()
    if "random" in new_status_kv:
        player.random(int(new_status_kv["random"]))
    if "consume" in new_status_kv:
        player.consume(int(new_status_kv["consume"]))
    if "single" in new_status_kv:
        player.single(int(new_status_kv["single"]))
    if "repeat" in new_status_kv:
        player.repeat(int(new_status_kv["repeat"]))

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


def play_first():
    """
    Play the first song in the current playlist.
    :return:
    """
    player.play(0)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)

#
# Note on play previous and play last.
# The client.previous() and client.next() methods
# only work IF MPD is playing or paused. If MPD is
# stopped, neither method seems to work. As a result,
# we have chosen to implement the logical actions
# of play previous and play next so that they play
# the previous/next playlist entry regardless of the
# current state of MPD
#

def play_previous():
    """
    Play the previous song in the current playlist
    :return:
    """
    current_status = player.status()
    playlist_len = int(current_status[u'playlistlength'])
    song = int(current_status[u'song']);
    if song > 0:
        player.play(song - 1)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


def play_next():
    """
    Play the next song in the current playlist
    :return:
    """
    current_status = player.status()
    playlist_len = int(current_status[u'playlistlength'])
    song = int(current_status[u'song']);
    if (song + 1) < playlist_len:
        player.play(song + 1)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


def play_last():
    """
    Play the last song in the current playlist
    :return:
    """
    current_status = player.status()
    player.play(int(current_status[u'playlistlength']) - 1)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route(url_with_prefix("/player/volumelevel"), methods=['PUT'])
def volume_change():
    """
    Change the current volume setting.
    :return:
    """
    args = json.loads(request.data)
    try:
        new_volume = int(args["amount"])
        player.setvol(new_volume)
    except:
        pass

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route(url_with_prefix("/player/songposition"), methods=['PUT'])
def song_time_change():
    """
    Change the current song position.
    :return:
    """
    args = json.loads(request.data)
    try:
        new_time = int(args["time"])
        player.settime(new_time)
    except:
        pass

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route(url_with_prefix("/player/musicdatabase"), methods=['PUT'])
def update_music_database():
    """
    Change the current volume setting by a +/- amount.
    :return:
    """
    try:
        player.update_music_database()
    except:
        pass

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route(url_with_prefix("/about"))
def about():
    """
    Show the about page
    :return:
    """
    return render_template("about.html")


def reset_player():
    """
    Reset the player instance when settings are changed.
    :return:
    """
    player = Player()