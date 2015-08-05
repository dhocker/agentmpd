/*
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
*/

/*
    Settings page app controller
*/
app.controller('settingsController', function($scope, $http) {
    // Initialization

    $scope.title = "AgentMPD";
    $scope.error = "";
    $scope.host = "";
    $scope.port = "";
    $scope.status_update_interval = 10;
    $scope.playlist_update_interval = 30;
    $scope.volume_increment = 5;

    $("#menu-settings").hide();

    $http.get("/settings").
        success(function(data, status, headers, config) {
            $scope.host = data["host"];
            $scope.port = data["port"];
            $scope.status_update_interval = data["status_update_interval"];
            $scope.playlist_update_interval = data["playlist_update_interval"];
            $scope.volume_increment = data["volume_increment"];
        }).
        error(function(data, status, headers, config) {
            $scope.error = "Host communication error";
        });

    $scope.save_settings = function() {
        if (validate_settings($scope)) {
            $http.post("/settings",
                    {'host': $scope.host,
                    'port': $scope.port,
                    'status_update_interval': $scope.status_update_interval,
                    'playlist_update_interval': $scope.playlist_update_interval,
                    'volume_increment': $scope.volume_increment}).
                success(function(data, status, headers, config) {
                }).
                error(function(data, status, headers, config) {
                    $scope.error = "Host communication error";
                });
        }
    };

    $scope.cancel = function() {
        // goto home
        window.location.replace("/home");
    };

    $scope.show_error = function() {
        // How do you clone this string???
        return $scope.error;
    };

    function validate_settings($scope) {
        $scope.error = '';
        if ($scope.host.length == 0) {
            // host error
            $scope.error = "Invalid host address";
            $("#host").focus();
            return false;
        }
        var port = parseInt($scope.port);
        if (isNaN(port)) {
            // port error
            $scope.error = "Invalid port number";
            $("#port").focus();
            return false;
        }
        var interval = parseInt($scope.status_update_interval);
        if (isNaN(interval) || interval <= 0) {
            // status_update_interval error
            $scope.error = "Invalid status update interval. It must be a number greater than zero.";
            $("#status-update-interval").focus();
            return false;
        }
        interval = parseInt($scope.playlist_update_interval);
        if (isNaN(interval) || interval <= 0) {
            // playlist_update_interval error
            $scope.error = "Invalid playlist update interval. It must be a number greater than zero.";
            $("#playlist-update-interval").focus();
            return false;
        }
        var increment = parseInt($scope.volume_increment);
        if (isNaN(increment) || increment <= 0 || increment > 50) {
            // volume incrementl error
            $scope.error = "Invalid volume increment value. It must be a number between 0 and 50.";
            $("#volume-increment").focus();
            return false;
        }
        return true;
    };

});
