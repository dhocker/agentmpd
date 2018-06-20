/*
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
*/

/*
    Home page app controller
*/
app.controller('playlistController', ["$scope", "$http", "$timeout", "UrlService", function($scope, $http, $timeout, UrlService) {
    // Initialization
    $scope.error = "";
    $scope.playlists = ["one"];
    $scope.playlist_name = "";
    $scope.search_collection = "albums"
    // Default to ascending sorts
    $scope.sort_seq_desc = false;
    $scope.sort_title_desc = false;
    $scope.sort_album_desc = false;
    $scope.sort_artist_desc = false;
    $("#load-button").prop("disabled", true);
    $("#load-albums-button").prop("disabled", true);
    $("#load-tracks-button").prop("disabled", true);
    $("#load-all-tracks-button").prop("disabled", true);
    $("#add-uri-button").prop("disabled", true);
    $("#remove-button").prop("disabled", true);
    $("#search-button").prop("disabled", false);
    $("#reset-button").prop("disabled", false);
    // Initialize Bootstrap popovers, if there are any
    $('[data-toggle="popover"]').popover({
        container: 'body'
    });
    get_playlists();
    get_artists();
    get_current_playlist();
    get_albums();

    function get_playlists() {
        $http.get(UrlService.url_with_prefix('/cpl/namedplaylists'), {}).
            success(function(data, status, headers, config) {
                $scope.playlists = data.playlists;
                $scope.playlist_size = $scope.playlists.length > 15 ? 15 : $scope.playlists.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    function get_artists() {
        $http.get(UrlService.url_with_prefix('/cpl/artists'), {}).
            success(function(data, status, headers, config) {
                $scope.artists = data.artists;
                $scope.artist_size = $scope.artists.length > 15 ? 15 : $scope.artists.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    function get_albums() {
        $http.get(UrlService.url_with_prefix('/cpl/albums'), {}).
            success(function(data, status, headers, config) {
                $scope.albums = data.albums;
                $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    $scope.playlist_selected = function () {
        if ($("#available-playlists option:selected").length > 0) {
            $("#load-button").prop("disabled", false);
            // Remember name of selected playlist as the suggestion for saving playlist
            var playlists = $("#available-playlists").val() || [""];
            $scope.playlist_name = playlists[0];
        }
        else {
            $("#load-button").prop("disabled", true);
            $scope.playlist_name = "";
        }
    };

    $scope.artist_selected = function () {
        if ($("#available-artists option:selected").length > 0) {
            // Get albums for selected artists
            var arg_list = $("#available-artists").val() || [];

            $http.get(UrlService.url_with_prefix('/cpl/albums'), {"params" : {"artists" : [arg_list]}, "xmessage":"Error getting albums for artist"}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    $scope.albums = data.albums;
                    $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                }).
                error(http_error);
        }
        else {
        }
    };

    $scope.album_selected = function () {
        if ($("#available-albums option:selected").length > 0) {
            $("#load-albums-button").prop("disabled", false);
            // Get tracks for selected albums
            var arg_list = $("#available-albums").val() || [];

            $http.get(UrlService.url_with_prefix('/cpl/album/tracks'), {"params" : arg_list}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    $scope.tracks = data.tracks;
                    $scope.tracks_size = $scope.tracks.length > 15 ? 15 : $scope.tracks.length;
                    if ($scope.tracks.length > 0) {
                        $("#load-all-tracks-button").prop("disabled", false);
                    }
                }).
                error(http_error);
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

        $http.post(UrlService.url_with_prefix('/cpl/playlist'), {"data" : {"playlists" : arg_list}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(http_error);
    };

    $scope.load_selected_tracks = function() {
        var arg_list = $("#available-tracks").val() || [];
        var c = arg_list.length;

        $http.post(UrlService.url_with_prefix('/cpl/playlist'), {"data" : {"uris" : arg_list}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(http_error);
    };

    $scope.load_all_tracks = function() {
        var all_tracks = []
        for (i = 0; i < $scope.tracks.length; i++) {
            all_tracks.push($scope.tracks[i].uri)
        }
        $http.post(UrlService.url_with_prefix('/cpl/playlist'), {"data" : {"uris" : all_tracks}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(http_error);
    };

    $scope.add_manual_uri = function() {
        $http.post(UrlService.url_with_prefix('/cpl/playlist'), {"data" : {"uris" : [$scope.manual_uri]}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                get_current_playlist();
            }).
            error(http_error);

    };

    $scope.select_all = function () {
        // Invert selection
        $.each($("[id^='check-']"), function (index, x) {
            x.checked = !x.checked;
        });
        $scope.selected_changed();
    };

    $scope.sort_by_seq = function() {
        $scope.current_playlist.playlist.sort(sort_array_by("pos1", $scope.sort_seq_desc));
        $scope.sort_seq_desc = !$scope.sort_seq_desc;
        update_playlist($scope.current_playlist.playlist);
    };

    $scope.sort_by_title = function() {
        $scope.current_playlist.playlist.sort(sort_array_by("track", $scope.sort_title_desc));
        $scope.sort_title_desc = !$scope.sort_title_desc;
        update_playlist($scope.current_playlist.playlist);
    };

    $scope.sort_by_album = function() {
        $scope.current_playlist.playlist.sort(sort_array_by("album", $scope.sort_album_desc));
        $scope.sort_album_desc = !$scope.sort_album_desc;
        update_playlist($scope.current_playlist.playlist);
    };

    $scope.sort_by_artist = function() {
        $scope.current_playlist.playlist.sort(sort_array_by("artist", $scope.sort_artist_desc));
        $scope.sort_artist_desc = !$scope.sort_artist_desc;
        update_playlist($scope.current_playlist.playlist);
    };

    function update_playlist(pl) {
        // Replace the entire mpd playlist with an updated
        // playlist. Typically, the playlist will be sorted.
        // Clear the mpd playlist
        $http.delete(UrlService.url_with_prefix('/cpl/playlist'), {}).
            success(function(data, status, headers, config) {
                // Send the updated playlist
                var all_tracks = []
                for (i = 0; i < pl.length; i++) {
                    all_tracks.push(pl[i].file || pl[i].uri);
                }
                $http.post(UrlService.url_with_prefix('/cpl/playlist'), {"data" : {"uris" : all_tracks}}).
                    success(function(data, status, headers, config) {
                        $scope.error = "";
                        // Reload the displayed playlist
                        get_current_playlist();
                    }).
                    error(http_error);
            }).
            error(http_error);
    }

    $scope.selected_changed = function () {
        var ids = get_selected_playlist_ids();
        $("#remove-button").prop("disabled", ids.length == 0);
    };

    $scope.remove_selected = function () {
        // Build a list of songids to be removed (those entries that are checked)
        var ids = get_selected_playlist_ids();

        // If anything was checked, remove it with a delete
        if (ids.length > 0) {
            $http.delete(UrlService.url_with_prefix('/cpl/playlistentry'), {"data" : ids}).
                success(function(data, status, headers, config) {
                    $scope.error = "";
                    get_current_playlist();
                }).
                error(http_error);
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
        $http.post(UrlService.url_with_prefix('/cpl/namedplaylists'), {"data" : {"name" : $scope.playlist_name}}).
            success(function(data, status, headers, config) {
                $scope.error = "";
                // Refresh playlist listbox
                get_playlists();
                showMessagebox($scope, "Saved", "The current playlist has been saved as: " + $scope.playlist_name);
            }).
            error(http_error);
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
        $http.get(UrlService.url_with_prefix('/cpl/namedplaylists'), {"params" : {"s" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.playlists = data.playlists;
                $scope.playlist_size = $scope.playlists.length > 15 ? 15 : $scope.playlists.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    function search_for_albums($scope) {
        $http.get(UrlService.url_with_prefix('/cpl/albums'), {"params" : {"album" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.albums = data.albums;
                $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    function search_for_albums_by_artist($scope) {
        $http.get(UrlService.url_with_prefix('/cpl/albums'), {"params" : {"artist" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.albums = data.albums;
                $scope.albums_size = $scope.albums.length > 15 ? 15 : $scope.albums.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    function search_for_tracks($scope) {
        $http.get(UrlService.url_with_prefix('/cpl/tracks'), {"params" : {"track" : $scope.search_string}}).
            success(function(data, status, headers, config) {
                $scope.tracks = data.tracks;
                $scope.tracks_size = $scope.tracks.length > 15 ? 15 : $scope.tracks.length;
                $scope.error = "";
            }).
            error(http_error);
    };

    $scope.reset_search = function () {
        get_playlists();
        get_albums();
    };

    function get_current_playlist() {
        $http.get(UrlService.url_with_prefix('/cpl/currentplaylist'), {}).
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
            error(http_error);
    };

    // Menu functions

    $scope.clear_playlist = function() {
        $http.delete(UrlService.url_with_prefix('/cpl/playlist'), {}).
            success(function(data, status, headers, config) {
                get_current_playlist();
                // showMessagebox($scope, "Clear Playlist", "Playlist has been cleared.");
            }).
            error(http_error);
    };

    $scope.menu_playlist_edit = function() {
        showMessagebox($scope, "Edit", "Edit has been invoked");
    };

    $scope.menu_playlist_rename = function() {
        showMessagebox($scope, "Rename", "Rename has been invoked");
    };

    function showMessagebox($scope, header, body) {
        $scope.messagebox_header = header;
        $scope.messagebox_body = body;
        $("#menu-messagebox").modal('show');
        $("#messagebox-close-btn").focus();
    };

    // Standard http error handling
    function http_error(data, status, headers, config) {
        if (data && data.message) {
            $scope.error = data.message;
        }
        else {
            if (config.xmessage) {
                $scope.error = config.xmessage;
            }
            else {
                $scope.error = "Server communication error";
            }
        }
    }

    $scope.show_error = function() {
        // How do you clone this string???
        return $scope.error;
    };

    /*
    Returns a comparator function that compares the specified
    property of an object. This is useful for sorting an
    array of objects by an object property.
    */
    function sort_array_by(propname, desc) {
        var reverse = 1;
        // If desc is truthy, the sort is descending or reversed
        if (typeof(desc) != 'undefined') {
            reverse = (desc) ? -1 : 1;
        }
        return function(a, b) {
            // Make the sort case insensitive
            if (typeof(a[propname]) != 'string') {
                a = a[propname];
                b = b[propname];
            }
            else {
                a = a[propname].toLowerCase();
                b = b[propname].toLowerCase();
            }
            if (a < b) {
                return reverse * -1;
            }
            if (a > b) {
                return reverse * 1;
            }
            return 0;
        }
    }

}]);
