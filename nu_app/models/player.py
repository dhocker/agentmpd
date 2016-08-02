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
import os


class Player(MPDModel):
    """
    Model class representing the MPD player interface
    """

    def __init__(self):
        MPDModel.__init__(self)

    @staticmethod
    def string_encode(encoding, s):
        """
        Encodes a string or list of strings
        :param encoding: Desired encoding (e.g. utf8 or ascii)
        :param s: string or list to be encoded
        :return: Returns an encoded string or a list of encoded strings
        """
        if type(s) == type([]):
            e = []
            for i in s:
                e.append(i.encode(encoding, 'ignore'))
            return e

        return s.encode(encoding, 'ignore')

    @mpd_client_handler()
    def get_current_player_status(self):
        s = {}
        if self.connect_to_mpd():
            current_status = self.client.status()
            current_song = self.client.currentsong()

            # Translate the status and song info to a single status dict
            # Translate keys/values from unicode to utf-8
            encoding = 'utf_8'
            for k, v in current_status.iteritems():
                s[k.encode(encoding,'ignore')] = v.encode(encoding,'ignore')
            for k, v in current_song.iteritems():
                # Some song properties (e.g. genre) can be a list
                # TODO Need to produce values for title, album and artist.
                # Normalization needs to be like playlist normalization.
                try:
                    s[k.encode(encoding,'ignore')] = Player.string_encode(encoding, v)
                except Exception as ex:
                    # This throws away properties that fail encoding
                    pass

            # Normalize required values
            if 'title' not in s:
                if ('file' in s):
                    base = os.path.basename(s['file'])
                    s['title'] = os.path.splitext(base)[0]
                else:
                    s["title"] = "N/A"
            if "album" not in s:
                s["album"] = "N/A"
            if "artist" not in s:
                s["artist"] = "N/A"

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
        v = "Unknown"
        # Every page has the MPD version on it and we don't
        # want every page to fail if there is no MPD server
        # accessible.
        try:
            if self.connect_to_mpd():
                v = self.client.mpd_version
                self.client.close()
        except:
            pass
        return v


    @mpd_client_handler()
    def play(self, pos):
        if self.connect_to_mpd():
            self.client.play(pos)
            self.close_mpd_connection()

    @mpd_client_handler()
    def queue(self, id):
        if self.connect_to_mpd():
            self.client.prioid(255, id)
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
    def settime(self, new_time):
        if self.connect_to_mpd():
            self.client.seekcur(new_time)
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
