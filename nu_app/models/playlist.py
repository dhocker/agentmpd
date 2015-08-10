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
from mpd_model import MPDModel


class Playlist(MPDModel):
    """
    Model class representing the MPD playlist
    """

    def __init__(self):
        MPDModel.__init__(self)

    def clear(self):
        if self.connect_to_mpd():
            self.client.clear()

    def get_playlists(self):
        lst = []

        if self.connect_to_mpd():
            pd_list = self.client.listplaylists()
            for p in pd_list:
                lst.append(p["playlist"])

            # Case insensitive sort for default ordering
            lst.sort(key=lambda s: s.lower())

        return lst

    def load_playlist(self, pl):
        if self.connect_to_mpd():
            self.client.load(pl)

    def remove_by_songid(self, songid):
        if self.connect_to_mpd():
            self.client.deleteid(songid)

    def get_albums(self):
        albums = None
        if self.connect_to_mpd():
            albums = self.client.list("album")
        return albums

    def get_album_tracks(self, title):
        tracks = None
        if self.connect_to_mpd():
            tracks = self.client.search("album", title)
        return tracks

    def add_track(self, uri):
        if self.connect_to_mpd():
            self.client.add(uri)