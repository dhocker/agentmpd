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

        return s

    @mpd_client_handler()
    def status(self):
        if self.connect_to_mpd():
            return self.client.status()

    @mpd_client_handler()
    def play(self, pos):
        if self.connect_to_mpd():
            self.client.play(pos)

    @mpd_client_handler()
    def pause(self, pos):
        if self.connect_to_mpd():
            self.client.pause(pos)

    @mpd_client_handler()
    def stop(self):
        if self.connect_to_mpd():
            self.client.stop()

    @mpd_client_handler()
    def setvol(self, level):
        if self.connect_to_mpd():
            self.client.setvol(level)

    @mpd_client_handler()
    def idle(self):
        if self.connect_to_mpd():
            self.client.idle()

    @mpd_client_handler()
    def random(self, state):
        if self.connect_to_mpd():
            self.client.random(state)

    @mpd_client_handler()
    def consume(self, state):
        if self.connect_to_mpd():
            self.client.consume(state)

    @mpd_client_handler()
    def repeat(self, state):
        if self.connect_to_mpd():
            self.client.repeat(state)

    @mpd_client_handler()
    def single(self, state):
        if self.connect_to_mpd():
            self.client.single(state)

    @mpd_client_handler()
    def update_music_database(self):
        if self.connect_to_mpd():
            self.client.update();
