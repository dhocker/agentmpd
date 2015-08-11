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
    $("#load-albums-button").prop("disabled", true);
    $("#load-tracks-button").prop("disabled", true);
    $("#load-all-tracks-button").prop("disabled", true);

    get_playlists();
    get_current_playlist();
    get_albums();

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

    function get_albums() {
        $http.get('/playlist/albums', {}).
            success(function(data, status, headers, config) {
                $scope.albums = data.albums;
                $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Server communication error";
            });
    };

    $scope.playlist_selected = function () {
        if ($("#available-playlists option:selected").length > 0) {
            $("#load-button").prop("disabled", false);
        }
        else {
            $("#load-button").prop("disabled", true);
        }
    };

    $scope.album_selected = function () {
        if ($("#available-albums option:selected").length > 0) {
            $("#load-albums-button").prop("disabled", false);
            // Get tracks for selected albums
            var arg_list = $("#available-albums").val() || [];
            var c = arg_list.length;

            $http.post('/playlist/album_tracks', {"albums" : arg_list}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    $scope.tracks = data.tracks;
                    $scope.tracks_size = $scope.tracks.length > 15 ? 15 : $scope.tracks.length;
                    if ($scope.tracks.length > 0) {
                        $("#load-all-tracks-button").prop("disabled", false);
                    }
                }).
                error(function(data, status, headers, config) {
                    $scope.error = "Album tracks query failed due to server communication error";
                });
        }
        else {
            $("#load-albums-button").prop("disabled", true);
            $("#load-all-tracks-button").prop("disabled", true);
            $scope.tracks = [];
        }
    };

    $scope.track_selected = function () {
        if ($("#available-tracks option:selected").length > 0) {
            $("#load-tracks-button").prop("disabled", false);
        }
        else {
            $("#load-tracks-button").prop("disabled", true);
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

    $scope.load_selected_tracks = function() {
        var arg_list = $("#available-tracks").val() || [];
        var c = arg_list.length;

        $http.post('/playlist/load_tracks', {"tracks" : arg_list}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Loading of tracks failed due to server communication error";
            });

    };

    $scope.load_all_tracks = function() {
        var all_tracks = []
        for (i = 0; i < $scope.tracks.length; i++) {
            all_tracks.push($scope.tracks[i].uri)
        }
        $http.post('/playlist/load_tracks', {"tracks" : all_tracks}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Loading of tracks failed due to server communication error";
            });

    };

    $scope.select_all = function () {
        // Invert selection
        $.each($("[id^='check-']"), function (index, x) {
            x.checked = !x.checked;
        });
    };

    $scope.remove_selected = function () {
        // Build a list of songids to be removed (those entries that are checked)
        var ids = [];
        $.each($("[id^='check-']"), function (index, x) {
            if (x.checked) {
                ids.push($(x).attr('songid'));
            }
        });

        // If anything was checked, remove it with a delete
        if (ids.length > 0) {
            $http.post('/playlist/remove_selected', {"songids" : ids}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    get_current_playlist();
                }).
                error(function(data, status, headers, config) {
                    $scope.error = "Remove songs failed due to server communication error";
                });
        }
    };

    // Launches modal dialog to save the current playlist as a named playlist
    $scope.save_playlist = function () {
        $("#save-playlist-dlg").modal('show');
    };

    // Saves the current playlist in the named playlist
    $scope.save_playlist_by_name = function () {
        alert("Saved");
    }

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

    $scope.show_error = function() {
        // How do you clone this string???
        return $scope.error;
    };

}]);
