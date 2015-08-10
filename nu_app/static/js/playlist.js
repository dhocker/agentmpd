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
    Home page app controller
*/
app.controller('playlistController', ["$scope", "$http", function($scope, $http) {
    // Initialization
    $scope.error = "";
    $scope.playlists = ["one"];
    $("#load-button").prop("disabled", true);

    get_playlists();
    get_current_playlist();

    function get_playlists() {
        $http.get('/playlist/all', {}).
            success(function(data, status, headers, config) {
                $scope.playlists = data.playlists;
                $scope.playlist_size = $scope.playlists.length > 15 ? 15 : $scope.playlists.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Server communication error";
            });
    };

    $scope.enable_load = function () {
        if ($("#available-playlists option:selected").length > 0) {
            $("#load-button").prop("disabled", false);
        }
        else {
            $("#load-button").prop("disabled", true);
        }
    };

    $scope.load_playlists = function() {
        var arg_list = $("#available-playlists").val() || [];
        var c = arg_list.length;

        $http.post('/playlist/load_selected', {"playlists" : arg_list}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Loading of playlists failed due to server communication error";
            });

    };

    $scope.select_all = function () {
        // Invert selection
        $.each($("[id^='check-']"), function (index, x) {
            x.checked = !x.checked;
        });
    };

    $scope.remove_selected = function () {
        var ids = [];
        $.each($("[id^='check-']"), function (index, x) {
            if (x.checked) {
                ids.push($(x).attr('songid'));
            }
        });

        // If anything was checked, remove it with a delete
        console.log(ids);
    };

    function get_current_playlist() {
        $http.get('/home/current_playlist', {}).
            success(function(data, status, headers, config) {
                $scope.current_playlist = data;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Server communication error";
            });
    };

    // Menu functions

    $scope.menu_playlist_clear = function() {
        $http.put('/playlist/clear', {}).
            success(function(data, status, headers, config) {
                get_current_playlist();
                showMessagebox($scope, "Clear Playlist", "Playlist has been cleared.");
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Host communication error";
            });
    };

    $scope.menu_playlist_edit = function() {
        alert("Edit has been invoked");
    };

    $scope.menu_playlist_save = function() {
        alert("Save has been invoked");
    };

    $scope.menu_playlist_rename = function() {
        alert("Rename has been invoked");
    };

    function showMessagebox($scope, header, body) {
        $scope.messagebox_header = header;
        $scope.messagebox_body = body;
        $("#menu-messagebox").modal('show');
    };

}]);
