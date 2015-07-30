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
from datetime import datetime, timedelta


class MPDModel:
    """
    Base class for models
    """

    def __init__(self):
        self.client = None
        self.last_use = datetime.now()

    def connect_to_mpd(self):
        # Restart the connection periodically because eventually the connection will drop
        delta = datetime.now() - self.last_use
        if (delta.total_seconds() > 60) and self.client:
            try:
                self.client.close()
            except:
                pass
            print "Restarting connection to mpd"
            self.client = None

        if not self.client:
            # use_unicode will enable the utf-8 mode for python2
            # see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
            self.client = mpd.MPDClient(use_unicode=True)
            host = KVStore.get("mpd", "host", "localhost")
            port = KVStore.get("mpd", "port", "6600")
            try:
                self.client.connect(host, int(port))
                self.last_use = datetime.now()
                return True
            except Exception as ex:
                print ex
                self.client = None
            return False

        self.last_use = datetime.now()
        return True
