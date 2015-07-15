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
import mpd

# use_unicode will enable the utf-8 mode for python2
# see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
client = None
status = ""

def connect_to_mpd():
    global client
    if not client:
        client = mpd.MPDClient(use_unicode=True)
        client.connect("raspberrypi-fs", 6600)


def get_current_player_status():
    current_status = client.status()
    current_song = client.currentsong()

    # Translate the status and song info to a single status dict
    s = {}
    s['state'] = current_status['state']
    s['song'] = current_status['song']
    for k, v in current_song.iteritems():
        s[k.encode('ascii','ignore')] = v.encode('ascii','ignore')

    return s

@app.route("/")
def root():
    return redirect(url_for('home'))


@app.route("/home", methods=['GET'])
def home():
    global client
    global status

    connect_to_mpd()

    lsinfo = client.lsinfo("/")
    current_song = get_current_player_status()
    status = current_song["state"]

    return render_template('home.html', current_song=current_song)


@app.route("/home/current_playlist", methods=['GET'])
def get_current_playlist():
    connect_to_mpd()
    info = client.playlistinfo()
    playlist = {}
    playlist["playlist"] = info
    return jsonify(**playlist)


@app.route("/home/current_status", methods=['GET'])
def get_current_status():
    connect_to_mpd()
    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/current_song", methods=['POST'])
def get_current_song():
    connect_to_mpd()
    current_song = get_current_player_status()
    return jsonify(**current_song)

@app.route("/home/play_song/<int:pos>", methods=['POST'])
def play_song(pos):
    connect_to_mpd()

    client.play(pos)

    current_status = get_current_player_status()
    return jsonify(**current_status)

@app.route("/home/toggle_play", methods=['POST'])
def toggle_play():
    connect_to_mpd()
    current_status = get_current_player_status()
    if current_status['state'] == 'play':
        client.pause(1)
    elif current_status['state'] == 'pause':
        client.pause(0)
    elif current_status['state'] == 'stop':
        client.play(current_status['song'])

    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/stop_play", methods=['POST'])
def stop_play():
    global status
    connect_to_mpd()
    client.stop()
    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_first", methods=['POST'])
def play_first():
    global status
    connect_to_mpd()
    client.play(0)
    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_previous", methods=['POST'])
def play_previous():
    global status
    connect_to_mpd()
    client.previous()
    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_next", methods=['POST'])
def play_next():
    global status
    connect_to_mpd()
    client.next()
    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/home/play_last", methods=['POST'])
def play_last():
    global status
    connect_to_mpd()
    current_status = client.status()
    client.play(int(current_status[u'playlistlength']) - 1)
    current_status = get_current_player_status()
    return jsonify(**current_status)


@app.route("/about")
def about():
    return render_template("about.html")


status = "stopped"
