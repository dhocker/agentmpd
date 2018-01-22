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
from nu_app import app
from nu_app.models.mpd_model import MPDModelException
from flask import jsonify


@app.errorhandler(MPDModelException)
def handle_model_exception(ex):
    response = jsonify(ex.to_dict())
    response.status_code = ex.status_code
    return response