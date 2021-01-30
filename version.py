#
# AgentMPD - web app for controlling an mpd instance
# Copyright © 2015, 2021  Dave Hocker (email: AtHomeX10@gmail.com)
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

from nu_app import app
from nu_app.models.player import Player

def GetVersion():
  """
  Returns the current app version
  """
  return "2021.0.0.1"

def GetMPDVersion():
    player = Player()
    return player.mpd_version()
import socket

def GetHostName():
  """
  Returns the current hostname
  """
  # Just go for the first token in the full hostname
  hn = socket.gethostname().split('.')
  return hn[0]

@app.context_processor
def get_release_version():
    '''
    Exposes the variable version to jinga2 teplate renderer.
    :return:
    '''
    return dict(
        release_version = GetVersion(),
        mpd_version = GetMPDVersion(),
        hostname = GetHostName()
    )
