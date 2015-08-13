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
import re


class Playlist(MPDModel):
    """
    Model class representing the MPD playlist
    """

    def __init__(self):
        MPDModel.__init__(self)

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

    def search_for_playlists(self, search_pat):
        all_pl = self.get_playlists()
        result_pl = []

        rx_pat = ".*{0}.*".format(search_pat)
        rxo = re.compile(search_pat, flags=re.IGNORECASE + re.DOTALL)

        for pl in all_pl:
            if rxo.search(pl):
                result_pl.append(pl)

        return result_pl

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

    def search_for_albums(self, search_pat):
        all_albums = self.get_albums()
        result_albums = []

        rx_pat = ".*{0}.*".format(search_pat)
        rxo = re.compile(search_pat, flags=re.IGNORECASE + re.DOTALL)

        for album in all_albums:
            if rxo.search(album):
                result_albums.append(album)

        return result_albums

    def search_for_albums_by_artist(self, search_pat):
        result_albums = []
        if self.connect_to_mpd():
            result_albums = self.client.list("album", "artist", search_pat)
        return result_albums

    def get_album_tracks(self, title):
        tracks = []
        if self.connect_to_mpd():
            tracks = self.client.search("album", title)
        # It would be tempting to sort the list of tracks by title, but
        # you usually want to see the tracks in an album by track number order.
        return tracks

    def search_for_tracks(self, search_pat):
        tracks = []
        if self.connect_to_mpd():
            tracks = self.client.search("title", search_pat)
        # Sort by title
        tracks.sort(key=lambda s: s["title"].lower())
        return tracks

    def add_track(self, uri):
        if self.connect_to_mpd():
            self.client.add(uri)

    def save_current_playlist(self, name):
        if self.connect_to_mpd():
            self.remove_playlist(name)
            self.client.save(name)

    def remove_playlist(self, name):
        # Try to delete an existing playlist. Ignore errors if one does not exist.
        if self.connect_to_mpd():
            try:
                self.client.rm(name)
            except:
                pass
