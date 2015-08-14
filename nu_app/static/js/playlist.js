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
app.controller('playlistController', ["$scope", "$http", "$timeout", function($scope, $http, $timeout) {
    // Initialization
    $scope.error = "";
    $scope.playlists = ["one"];
    $scope.playlist_name = "";
    $("#load-button").prop("disabled", true);
    $("#load-albums-button").prop("disabled", true);
    $("#load-tracks-button").prop("disabled", true);
    $("#load-all-tracks-button").prop("disabled", true);
    $("#add-uri-button").prop("disabled", true);
    $("#remove-button").prop("disabled", true);
    $("#search-button").prop("disabled", false);
    $("#reset-button").prop("disabled", false);
    // Initialize Bootstrap popovers, if there are any
    $('[data-toggle="popover"]').popover();

    get_playlists();
    get_artists();
    get_current_playlist();
    get_albums();

    function get_playlists() {
        $http.get('/cpl/namedplaylists', {}).
            success(function(data, status, headers, config) {
                $scope.playlists = data.playlists;
                $scope.playlist_size = $scope.playlists.length > 15 ? 15 : $scope.playlists.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Server communication error";
            });
    };

    function get_artists() {
        $http.get('/cpl/artists', {}).
            success(function(data, status, headers, config) {
                $scope.artists = data.artists;
                $scope.artist_size = $scope.artists.length > 15 ? 15 : $scope.artists.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Server communication error";
            });
    };

    function get_albums() {
        $http.get('/cpl/albums', {}).
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

    $scope.artist_selected = function () {
        if ($("#available-artists option:selected").length > 0) {
            // Get albums for selected artists
            var arg_list = $("#available-artists").val() || [];

            $http.get('/cpl/albums', {"params" : {"artists" : [arg_list]}}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    $scope.albums = data.albums;
                    $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                    if ($scope.tracks.length > 0) {
                        $("#load-all-tracks-button").prop("disabled", false);
                    }
                }).
                error(function(data, status, headers, config) {
                    $scope.error = "Artist album query failed due to server communication error";
                });
        }
        else {
        }
    };

    $scope.album_selected = function () {
        if ($("#available-albums option:selected").length > 0) {
            $("#load-albums-button").prop("disabled", false);
            // Get tracks for selected albums
            var arg_list = $("#available-albums").val() || [];

            $http.get('/cpl/album/tracks', {"params" : arg_list}).
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

    $scope.manual_uri_change = function () {
        if ($scope.manual_uri.length > 0) {
            $("#add-uri-button").prop("disabled", false);
        }
        else {
            $("#add-uri-button").prop("disabled", true);
        }
    };

    $scope.load_playlists = function() {
        var arg_list = $("#available-playlists").val() || [];
        var c = arg_list.length;

        $http.post('/cpl/playlist', {"data" : {"playlists" : arg_list}}).
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

        $http.post('/cpl/playlist', {"data" : {"uris" : arg_list}}).
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
        $http.post('/cpl/playlist', {"data" : {"uris" : all_tracks}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Loading of tracks failed due to server communication error";
            });

    };

    $scope.add_manual_uri = function() {
        $http.post('/cpl/playlist', {"data" : {"uris" : [$scope.manual_uri]}}).
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
        $scope.selected_changed();
    };

    $scope.selected_changed = function () {
        var ids = get_selected_playlist_ids();
        $("#remove-button").prop("disabled", ids.length == 0);
    };

    $scope.remove_selected = function () {
        // Build a list of songids to be removed (those entries that are checked)
        var ids = get_selected_playlist_ids();

        // If anything was checked, remove it with a delete
        if (ids.length > 0) {
            $http.delete('/cpl/playlistentry', {"data" : ids}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    get_current_playlist();
                }).
                error(function(data, status, headers, config) {
                    $scope.error = "Remove songs failed due to server communication error";
                });
        }
    };

    function get_selected_playlist_ids() {
        var ids = [];
        $.each($("[id^='check-']"), function (index, x) {
            if (x.checked) {
                ids.push($(x).attr('songid'));
            }
        });
        return ids;
    };

    // Launches modal dialog to save the current playlist as a named playlist
    $scope.save_playlist = function () {
        $("#save-playlist-dlg").modal('show');
        $scope.enable_save_button();
        // Hack...focus has to be set after this function returns.
        // How long to wait is a guess (500 ms in this case).
        $timeout(function() {
            $("#playlist-name").focus();
        }, 500);
    };

    // Saves the current playlist in the named playlist
    $scope.save_playlist_by_name = function () {
        $http.post('/cpl/namedplaylists', {"data" : {"name" : $scope.playlist_name}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                // Refresh playlist listbox
                get_playlists();
                showMessagebox($scope, "Saved", "The current playlist has been saved as: " + $scope.playlist_name);
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Save playlist failed due to server communication error";
            });
    };

    $scope.enable_save_button = function () {
        // This prevents saving a playlist with an empty name.
        // TODO The playlist name must be a valid file name.
        if ($scope.playlist_name.length > 0) {
            $("#save-playlist-btn").prop("disabled", false);
        }
        else {
            $("#save-playlist-btn").prop("disabled", true);
        }
    };

    $scope.search = function () {
        $("#search-dlg").modal('show');
        //$scope.enable_save_button();
        $("#search-for-btn").prop("disabled", false);
        $("#search-cancel-btn").prop("disabled", false);
        // Hack...focus has to be set after this function returns.
        // How long to wait is a guess (500 ms in this case).
        $timeout(function() {
            $("#search-string").focus();
        }, 500);
    };

    $scope.search_for = function () {
        //search_what = $("input:radio[name='search-collection']:checked").val();
        //alert("Searching..." + $scope.search_collection + " for " + $scope.search_string);
        switch ($scope.search_collection) {
            case "playlists":
                search_for_playlists($scope);
                break;
            case "albums":
                search_for_albums($scope);
                break;
            case "artistalbums":
                search_for_albums_by_artist($scope);
                break;
            case "tracks":
                search_for_tracks($scope);
                break;
        }
    };

    function search_for_playlists($scope) {
        $http.get('/cpl/namedplaylists', {"params" : {"s" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.playlists = data.playlists;
                $scope.playlist_size = $scope.playlists.length > 15 ? 15 : $scope.playlists.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Get for playlists failed due to server error";
            });
    };

    function search_for_albums($scope) {
        $http.get('/cpl/albums', {"params" : {"album" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.albums = data.albums;
                $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Search for albums failed due to server error";
            });
    };

    function search_for_albums_by_artist($scope) {
        $http.get('/cpl/albums', {"params" : {"artist" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.albums = data.albums;
                $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Search for albums failed due to server error";
            });
    };

    function search_for_tracks($scope) {
        $http.get('/cpl/tracks', {"params" : {"track" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.tracks = data.tracks;
                $scope.tracks_size = $scope.tracks.length > 15 ? 15 : $scope.tracks.length;
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Search for albums failed due to server error";
            });
    };

    $scope.reset_search = function () {
        get_playlists();
        get_albums();
    };

    function get_current_playlist() {
        $http.get('/cpl/currentplaylist', {}).
            success(function(data, status, headers, config) {
                $scope.current_playlist = data;
                $scope.error = "";
                if ($scope.current_playlist.playlist.length > 0) {
                    $("#save-button").prop("disabled", false);
                    $("#clear-button").prop("disabled", false);
                }
                else {
                    $("#save-button").prop("disabled", true);
                    $("#clear-button").prop("disabled", true);
                }
                $("#remove-button").prop("disabled", true);
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Server communication error";
            });
    };

    // Menu functions

    $scope.clear_playlist = function() {
        $http.delete('/cpl/playlist', {}).
            success(function(data, status, headers, config) {
                get_current_playlist();
                // showMessagebox($scope, "Clear Playlist", "Playlist has been cleared.");
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Host communication error";
            });
    };

    $scope.menu_playlist_rename = function() {
        alert("Rename has been invoked");
    };

    function showMessagebox($scope, header, body) {
        $scope.messagebox_header = header;
        $scope.messagebox_body = body;
        $("#menu-messagebox").modal('show');
        $("#messagebox-close-btn").focus();
    };

    $scope.show_error = function() {
        // How do you clone this string???
        return $scope.error;
    };

}]);
