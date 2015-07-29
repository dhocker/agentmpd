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

import json
import platform


class KVStore:
    @classmethod
    def get(cls, cat, key, default):
        kvs = cls.load_store()
        try:
            v = kvs[cat][key]
        except:
            v = default
        return v


    @classmethod
    def set(cls, cat, key, value):
        kvs = cls.load_store()
        kvs[cat][key] = value
        cls.dump_store(kvs)


    @classmethod
    def load_store(cls):
        kvs_fn = KVStore.get_store_path()
        kvstore = {"mpd":{}, "player":{}}
        try:
            store = open(kvs_fn, "r")
            kvstore = json.loads(store.read())
            store.close()
        except Exception as ex:
            # Assume first time access
            print ex
        return kvstore


    @classmethod
    def dump_store(cls, kvstore):
        kvs_fn = KVStore.get_store_path()
        try:
            store = open(kvs_fn, "w")
            store.write(json.dumps(kvstore))
            store.close()
        except Exception as ex:
            print ex


    @staticmethod
    def get_store_path():
        """
        Based on OS, return full path to k-v store file
        """
        osname = platform.system()
        if osname == "Darwin":
            return "/var/mpd_web_client/kvstore.json"
        if osname == "Linux":
            return "/var/mpd_web_client/kvstore.json"
        if osname == "Windows":
            import os
            return os.path.expanduser("~\\mpd_web_client\\kvstore.json")
        return "other"