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


class Settings:


    @classmethod
    def get(cls):
        host = KVStore.get("mpd", "host", "localhost")
        port = KVStore.get("mpd", "port", "6600")
        status_update_interval = KVStore.get("player", "status_update_interval", "10")
        playlist_update_interval = KVStore.get("player", "playlist_update_interval", "30")
        s = {'host': host, 'port': port, 'status_update_interval': status_update_interval, 'playlist_update_interval': playlist_update_interval}
        return s


    @classmethod
    def save(cls, s):
        KVStore.set("mpd", "host", s["host"])
        KVStore.set("mpd", "port", s["port"])
        KVStore.set("player", "status_update_interval", s["status_update_interval"])
        KVStore.set("player", "playlist_update_interval", s["playlist_update_interval"])
