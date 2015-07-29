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
#from nu_app.models.key_value_store import KVStore
from nu_app.models.player import Player
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, jsonify
import mpd

#  MPD music player model instance
player = Player()


@app.route("/")
def root():
    return redirect(url_for('home'))


@app.route("/home", methods=['GET'])
def home():
    current_song = player.get_current_player_status()
    status = current_song["state"]

    return render_template('home.html', current_song=current_song, ngapp="agentmpd", ngcontroller="homeController")


@app.route("/home/current_playlist", methods=['GET'])
def current_playlist():
    playlist = player.get_current_playlist()
    return jsonify(**playlist)


@app.route("/home/current_status", methods=['GET'])
def get_current_status():
    current_status = player.get_current_player_status()
    if "pos" in current_status:
        current_status["pos1"] = int(current_status["pos"]) + 1
    else:
        current_status["pos1"] = ""
    return jsonify(**current_status)


@app.route("/home/current_song", methods=['POST'])
def get_current_song():
    current_song = player.get_current_player_status()
    return jsonify(**current_song)


@app.route("/home/play_song/<int:pos>", methods=['POST'])
def play_song(pos):
    player.play(pos)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/toggle_play", methods=['POST'])
def toggle_play():
    current_status = player.get_current_player_status()
    if current_status['state'] == 'play':
        player.pause(1)
    elif current_status['state'] == 'pause':
        player.pause(0)
    elif current_status['state'] == 'stop':
        player.play(current_status['song'])

    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/stop_play", methods=['POST'])
def stop_play():
    player.stop()
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_first", methods=['POST'])
def play_first():
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

@app.route("/home/play_previous", methods=['POST'])
def play_previous():
    current_status = player.status()
    playlist_len = int(current_status[u'playlistlength'])
    song = int(current_status[u'song']);
    if song > 0:
        player.play(song - 1)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_next", methods=['POST'])
def play_next():
    current_status = player.status()
    playlist_len = int(current_status[u'playlistlength'])
    song = int(current_status[u'song']);
    if (song + 1) < playlist_len:
        player.play(song + 1)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_last", methods=['POST'])
def play_last():
    current_status = player.status()
    player.play(int(current_status[u'playlistlength']) - 1)
    current_status = player.get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/idle", methods=['GET'])
def idle():
    print "Idling..."
    response = player.idle()
    return response


@app.route("/about")
def about():
    return render_template("about.html")
