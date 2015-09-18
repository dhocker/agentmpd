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
from mpd_model import MPDModel, mpd_client_handler


class Player(MPDModel):
    """
    Model class representing the MPD player interface
    """

    def __init__(self):
        MPDModel.__init__(self)

    @mpd_client_handler()
    def get_current_player_status(self):
        s = {}
        if self.connect_to_mpd():
            current_status = self.client.status()
            current_song = self.client.currentsong()

            # Translate the status and song info to a single status dict
            # Translate keys/values from unicode to ascii
            for k, v in current_status.iteritems():
                s[k.encode('ascii','ignore')] = v.encode('ascii','ignore')
            for k, v in current_song.iteritems():
                s[k.encode('ascii','ignore')] = v.encode('ascii','ignore')

            self.close_mpd_connection()

        return s

    @mpd_client_handler()
    def status(self):
        if self.connect_to_mpd():
            s = self.client.status()
            self.close_mpd_connection()
            return s

    @mpd_client_handler()
    def mpd_version(self):
        v = "unknown"
        if self.connect_to_mpd():
            v = self.client.mpd_version
            self.client.close()
        return v


    @mpd_client_handler()
    def play(self, pos):
        if self.connect_to_mpd():
            self.client.play(pos)
            self.close_mpd_connection()

    @mpd_client_handler()
    def pause(self, pos):
        if self.connect_to_mpd():
            self.client.pause(pos)
            self.close_mpd_connection()

    @mpd_client_handler()
    def stop(self):
        if self.connect_to_mpd():
            self.client.stop()
            self.close_mpd_connection()

    @mpd_client_handler()
    def setvol(self, level):
        if self.connect_to_mpd():
            self.client.setvol(level)
            self.close_mpd_connection()

    @mpd_client_handler()
    def idle(self):
        if self.connect_to_mpd():
            self.client.idle()
            self.close_mpd_connection()

    @mpd_client_handler()
    def random(self, state):
        if self.connect_to_mpd():
            self.client.random(state)
            self.close_mpd_connection()

    @mpd_client_handler()
    def consume(self, state):
        if self.connect_to_mpd():
            self.client.consume(state)
            self.close_mpd_connection()

    @mpd_client_handler()
    def repeat(self, state):
        if self.connect_to_mpd():
            self.client.repeat(state)
            self.close_mpd_connection()

    @mpd_client_handler()
    def single(self, state):
        if self.connect_to_mpd():
            self.client.single(state)
            self.close_mpd_connection()

    @mpd_client_handler()
    def update_music_database(self):
        if self.connect_to_mpd():
            self.client.update();
            self.close_mpd_connection()
