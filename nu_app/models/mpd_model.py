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
import threading


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


class MPDConnection:
    """
    An MPD TCP/IP connection.
    """
    def __init__(self):
        self.client = mpd.MPDClient(use_unicode=True)
        self.last_use = datetime.now()


class MPDModel:
    """
    Base class for models
    """
    # Shared connection pool among all derived classes
    _pool_lock = threading.Lock()
    _connection_pool = []
    # Timeout in seconds
    _connection_timeout = 60

    def __init__(self):
        self._cnn = None
        self.client = None
        # This is a temporary fix to the threading changes that
        # have surfaced with the latest version of Flask.
        # A better solution would probably be a connection pool.
        self.last_use = datetime.now()

    @staticmethod
    def _clean_pool():
        """
        Clean out all expired connections. MUST be called
        with lock acquired.
        :return:
        """
        # Traverse connection pool backwards so we can remove
        # exoired connections without issue.
        i = len(MPDModel._connection_pool)
        print("Pool size:", i)
        while i > 0:
            i -= 1
            cnn = MPDModel._connection_pool[i]
            delta = datetime.now() - cnn.last_use
            if delta.total_seconds() > MPDModel._connection_timeout:
                try:
                    cnn.client.close()
                    print("Closed MPD connection:", cnn)
                except:
                    pass
                MPDModel._connection_pool.pop(i)

    def acquire_connection(self):
        #============================
        MPDModel._pool_lock.acquire()
        #============================

        # Close and remove all expired connections
        MPDModel._clean_pool()

        cnn = None
        while not cnn:
            # Try to get a connection out of the pool
            if len(MPDModel._connection_pool) > 0:
                cnn = MPDModel._connection_pool.pop(0)
                cnn.last_use = datetime.now()
            else:
                # Empty pool, so create a new connection
                try:
                    cnn = MPDConnection()
                except Exception as ex:
                    print(ex)
                    cnn = None
                    continue
                host = KVStore.get("mpd", "host", "localhost")
                port = KVStore.get("mpd", "port", "6600")
                try:
                    cnn.client.connect(host, int(port))
                    cnn.last_use = datetime.now()
                    print("Create connection:", cnn)
                except Exception as ex:
                    # Attempt to open a new connection failed
                    print(ex)
                    cnn = None
                    #============================
                    MPDModel._pool_lock.release()
                    #============================
                    raise MPDModelException(str(ex))

        #============================
        MPDModel._pool_lock.release()
        #============================
        return cnn

    def release_connection(self, cnn):
        """
        Put a connection back into the pool
        :param cnn:
        :return:
        """
        #============================
        MPDModel._pool_lock.acquire()
        #============================

        MPDModel._connection_pool.append(cnn)

        #============================
        MPDModel._pool_lock.release()
        #============================

    def connect_to_mpd(self):
        """
        Get a connection to the configured mpd server.
        This implementation strives to minimize the number of
        connections that are made. However, if an existing connection
        is idle for very long, mpd will close it.
        :return: True if a connection was obtained. Otherwise, False.
        """
        self._cnn = self.acquire_connection()
        self.client = self._cnn.client
        return True

    def close_mpd_connection(self):
        """
        Make as if the connection is closed. Originally, every mpd interaction
        resulted in a connect/close sequence. This is here simply to surround
        the connection use.
        :return:
        """
        self.release_connection(self._cnn)
        self._cnn = None
        self.client = None
