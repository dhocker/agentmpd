#
# AgentMPD - web app for controlling an mpd instance
# Copyright (C) 2015, 2018  Dave Hocker (email: AtHomeX10@gmail.com)
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
from nu_app.models.key_value_store import KVStore
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
        # This is a temporary fix to the threading changes that
        # have surfaced with the latest version of Flask.
        # A better solution would probably be a connection pool.
        self.last_use = datetime.now()

    def connect_to_mpd(self):
        """
        Get a connection to the configured mpd server.
        This implementation strives to minimize the number of
        connections that are made. However, if an existing connection
        is idle for very long, mpd will close it. Hence, the error retry
        code makes several attempts to connection before declaring failure.
        :return: True if a connection was obtained. Otherwise, False.
        """
        # This is a temporary fix to the threading changes that
        # have surfaced with the latest version of Flask.
        # Restart the connection periodically because eventually the connection will drop
        delta = datetime.now() - self.last_use
        if (delta.total_seconds() > 60) and self.client:
            try:
                self.client.close()
            except:
                pass
            print("Restarting connection to mpd")
            self.client = None

        retry_max = 2
        for retry_count in range(retry_max + 1):
            # If the client connection is closed, reopen it
            if not self.client:
                # use_unicode will enable the utf-8 mode for python2
                # see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
                try:
                    self.client = mpd.MPDClient(use_unicode=True)
                except Exception as ex:
                    print(ex)
                    continue
                host = KVStore.get("mpd", "host", "localhost")
                port = KVStore.get("mpd", "port", "6600")
                try:
                    self.client.connect(host, int(port))
                    self.last_use = datetime.now()
                    return True
                except Exception as ex:
                    print(ex)
                    if self.client:
                        self.client.close()
                    self.client = None
                    if retry_count >= retry_max:
                        #self.connection_lock.release()
                        raise MPDModelException(str(ex))

        self.last_use = datetime.now()
        return True

    def close_mpd_connection(self):
        """
        Make as if the connection is closed. Originally, every mpd interaction
        resulted in a connect/close sequence. This is here simply to surround
        the connection use.
        :return:
        """
        try:
            self.client.close()
        except Exception as ex:
            print(ex)
        self.client = None
