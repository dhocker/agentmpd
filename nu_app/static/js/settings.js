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
    AgentMPD home page app
*/

var app = angular.module('settings', []);

// Change the interpolation marker from {{ }} to {= =} to avoid
// collision with the Jinga2 template system.
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{=');
    $interpolateProvider.endSymbol('=}');
});

/*
    Settings page app controller
*/
app.controller('settingsController', function($scope, $http) {
    // Initialization

    $scope.title = "AgentMPD";
    $scope.host = "";
    $scope.port = "";

    $("#menu-settings").hide();

    $http.get("/settings").
        success(function(data, status, headers, config) {
            $scope.host = data["host"];
            $scope.port = data["port"];
        }).
        error(function(data, status, headers, config) {
            $scope.status = "Host communication error";
        });

    $scope.save_settings = function() {
        $http.post("/settings", {'host': $scope.host, 'port': $scope.port}).
            success(function(data, status, headers, config) {
            }).
            error(function(data, status, headers, config) {
                $scope.status = "Host communication error";
            });
    };

    $scope.cancel = function() {
        // goto home
        window.location.replace("/home");
    };

});
