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
from key_value_store import KVStore
import mpd


class Player:
    """
    Model class representing the MPD interface
    """

    def __init__(self):
        self.client = None

    def connect_to_mpd(self):
        if not self.client:
            # use_unicode will enable the utf-8 mode for python2
            # see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
            self.client = mpd.MPDClient(use_unicode=True)
            host = KVStore.get("mpd", "host", "localhost")
            port = KVStore.get("mpd", "port", "6600")
            try:
                self.client.connect(host, int(port))
                return True
            except Exception as ex:
                print ex
            return False
        return True

    def get_current_player_status(self):
        s = {}
        if self.connect_to_mpd():
            current_status = self.client.status()
            current_song = self.client.currentsong()

            # Translate the status and song info to a single status dict
            s['state'] = current_status['state']
            s['song'] = current_status['song']
            # Translate keys/values from unicode to ascii
            for k, v in current_song.iteritems():
                s[k.encode('ascii','ignore')] = v.encode('ascii','ignore')

        return s

    def get_current_playlist(self):
        pl = []
        if self.connect_to_mpd():
            info = self.client.playlistinfo()

            # Normalize playlist entries. The data returned from
            # MPD varies according to what is playing (radio stations
            # and records).
            for i in info:
                pe = {}
                pe["id"] = i["id"]
                # 0-based position
                pe["pos"] = i["pos"]
                # 1-based position
                pe["pos1"] = int(i["pos"]) + 1
                # Pick a name based on the best available property
                # The fall back is the file name which is always present
                if "name" in i:
                    pe["track"] = i["name"]
                elif "title" in i:
                    pe["track"] = i["title"]
                else:
                    pe["track"] = i["file"]
                if "album" in i:
                    pe["album"] = i["album"]
                else:
                    pe["album"] = "."
                if "artist" in i:
                    pe["artist"] = i["artist"]
                else:
                    pe["artist"] = "."
                if "time" in i:
                    pe["time"] = i["time"]
                else:
                    pe["time"] = ""
                pe["file"] = i["file"]
                pl.append(pe)

        playlist = {}
        playlist["playlist"] = pl
        # TODO Figure out how to get current playlist name and add it to dict
        return playlist

    def status(self):
        return self.client.status()

    def play(self, pos):
        self.client.play(pos)

    def pause(self, pos):
        self.client.pause(pos)

    def stop(self):
        self.client.stop()

    def idle(self):
        self.client.idle()