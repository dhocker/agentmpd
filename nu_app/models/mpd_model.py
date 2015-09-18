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


# Wrapper to provide consistent error handling across all mpd client calls
def mpd_client_handler():
    def decorate(func):
        def call(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as ex:
                # args[0] should be the MPDModel instance
                # We make the gross assumption that the exception is caused
                # by a dropped connection to the mpd host.
                args[0].client = None
                raise MPDModelException(str(ex))
            return result
        return call
    return decorate


class MPDModelException(Exception):
    """
    MPD error reporting exception.
    """
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = "An error occurred while attempting to communicate with MPD: {0}".format(self.message)
        return rv


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
                self.client.close()
                self.client = None
                raise MPDModelException(str(ex))
            return False

        self.last_use = datetime.now()
        return True

    def close_mpd_connection(self):
        self.client.close()
        self.client = None
