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
import re


class Playlist(MPDModel):
    """
    Model class representing the MPD playlist
    """

    def __init__(self):
        MPDModel.__init__(self)

    @mpd_client_handler()
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
                pe["track"] = ""
                if "name" in i:
                    pe["track"] = i["name"]
                elif "title" in i:
                    pe["track"] = i["title"]
                pe["track"] = pe["track"] + " - " + i["file"]
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

            self.close_mpd_connection()

        playlist = {}
        playlist["playlist"] = pl
        # TODO Figure out how to get current playlist name and add it to dict
        return playlist

    @mpd_client_handler()
    def clear(self):
        if self.connect_to_mpd():
            self.client.clear()
            self.close_mpd_connection()

    @mpd_client_handler()
    def get_playlists(self):
        lst = []

        if self.connect_to_mpd():
            pd_list = self.client.listplaylists()
            for p in pd_list:
                lst.append(p["playlist"])
            self.close_mpd_connection()

        # Case insensitive sort for default ordering
        lst.sort(key=lambda s: s.lower())
        return lst

    @mpd_client_handler()
    def get_artists(self):
        lst = []

        if self.connect_to_mpd():
            lst = self.client.list("artist")
            self.close_mpd_connection()

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

    @mpd_client_handler()
    def load_playlist(self, pl):
        if self.connect_to_mpd():
            self.client.load(pl)
            self.close_mpd_connection()

    @mpd_client_handler()
    def remove_by_songid(self, songid):
        if self.connect_to_mpd():
            self.client.deleteid(songid)
            self.close_mpd_connection()

    @mpd_client_handler()
    def get_albums(self):
        albums = None
        if self.connect_to_mpd():
            albums = self.client.list("album")
            self.close_mpd_connection()
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

    @mpd_client_handler()
    def search_for_albums_by_artist(self, search_pat):
        result_albums = []
        if self.connect_to_mpd():
            result_albums = self.client.list("album", "artist", search_pat)
            self.close_mpd_connection()
        return result_albums

    def search_for_albums_by_artists(self, artists):
        all_albums = []
        for artist in artists:
            albums = self.search_for_albums_by_artist(artist)
            for a in albums:
                all_albums.append(a)

        return all_albums

    @mpd_client_handler()
    def get_album_tracks(self, title):
        tracks = []
        if self.connect_to_mpd():
            tracks = self.client.search("album", title)
            self.close_mpd_connection()
        # It would be tempting to sort the list of tracks by title, but
        # you usually want to see the tracks in an album by track number order.
        return tracks

    @mpd_client_handler()
    def search_for_tracks(self, search_pat):
        tracks = []
        if self.connect_to_mpd():
            tracks = self.client.search("title", search_pat)
            self.close_mpd_connection()
        # Sort by title
        tracks.sort(key=lambda s: s["title"].lower())
        return tracks

    @mpd_client_handler()
    def add_track(self, uri):
        if self.connect_to_mpd():
            self.client.add(uri)
            self.close_mpd_connection()

    @mpd_client_handler()
    def save_current_playlist(self, name):
        self.remove_playlist(name)
        if self.connect_to_mpd():
            self.client.save(name)
            self.close_mpd_connection()

    @mpd_client_handler()
    def remove_playlist(self, name):
        # Try to delete an existing playlist. Ignore errors if one does not exist.
        if self.connect_to_mpd():
            try:
                self.client.rm(name)
                self.close_mpd_connection()
            except:
                pass
