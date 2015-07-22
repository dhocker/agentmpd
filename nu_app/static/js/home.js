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

var app = angular.module('home', []);

// Change the interpolation marker from {{ }} to {= =} to avoid
// collision with the Jinga2 template system.
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{=');
    $interpolateProvider.endSymbol('=}');
});

/*
    Home page app controller
*/
app.controller('homeController', function($scope, $http, $interval, $timeout) {
    // Initialization

    $scope.title = "AgentMPD";

    $("#menu-player").hide();

    var translate_state = {};
    translate_state['play'] = 'Playing...';
    translate_state['pause'] = 'Paused';
    translate_state['stop'] = 'Stopped';

    var status_update_interval = 10 * 1000; // 10 seconds
    var playlist_update_interval = 30 * 1000; // 30 seconds

    $scope.playing = false;
    $scope.current_playlist = {"playlist": []};

    // Update the status of each playlist entry by assigning it a CSS
    // class that properly styles it
    function update_status() {
        for (var i = 0; i < $scope.current_playlist.playlist.length; i++)
        {
            var pe = $scope.current_playlist.playlist[i];
            if (pe.pos == $scope.currently_playing.song)
            {
                // Active styling overrides odd/even styling
                // And, a lot of trial and error proved you can't apply both.
                pe["class"] = "playlist-active";
            }
            else
            {
                if (i % 2)
                {
                    // Odd rows
                    // Only mark alt row if it is not the current playlist entry
                    pe["class"] = "alt";
                }
                else
                {
                    // Even rows
                    pe["class"] = "";
                }
            }
        }

        $scope.status = translate_state[$scope.currently_playing['state']];
        $scope.playing = ($scope.status == translate_state['play']);
    };

    function get_current_status() {
        $http.get('/home/current_status', {}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                update_status();
            }).
            error(function(data, status, headers, config) {
                $scope.status = "Host communication error";
            });
    };

    function idle() {
        $http.get('/home/idle', {}).
            success(function(data, status, headers, config) {
                if (data == 'player')
                {
                }
                else if (data == 'playlist')
                {
                }
                // Restart idle. Is this accidentally recursive???
                idle();
            }).
            error(function(data, status, headers, config) {
                $scope.status = "Host communication error";
            });
    };

    function get_current_playlist() {
        $http.get('/home/current_playlist', {}).
            success(function(data, status, headers, config) {
                $scope.current_playlist = data;
                update_status();
            }).
            error(function(data, status, headers, config) {
                $scope.status = "Host communication error";
            });
    };

    function update_view() {
        get_current_playlist();
    };

    // AJAX calls for transport functions

    function post_transport(url, msg) {
        $http.post(url, {'msg':msg}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                update_status();
            }).
            error(function(data, status, headers, config) {
                $scope.status = "Host communication error";
            });
    };

    $scope.toggle_playing = function() {
        post_transport('/home/toggle_play', 'play');
    };

    $scope.play_stop = function() {
        post_transport('/home/stop_play', 'stop');
    };

    $scope.play_first = function() {
        post_transport('/home/play_first', 'first');
    };

    $scope.play_previous = function() {
        post_transport('/home/play_previous', 'previous');
    };

    $scope.play_next = function() {
        post_transport('/home/play_next', 'next');
    };

    $scope.play_last = function() {
        post_transport('/home/play_last', 'last');
    };

    $scope.play_song = function(pos) {
        post_transport('/home/play_song/' + pos, 'play');
    };

    // Initialize current status
    get_current_status();
    get_current_playlist();

    // Polled status update every 10 seconds
    // This isn't very efficient, but for now it will have to do.
    // We'll need to figure out how to use the MPD idle API.
    $interval(get_current_status, status_update_interval);
    // Update the playlist every 30 sec. This is here strictly to
    // catch changes to the playlist made by MPD or by another
    // MPD client app (e.g. Theremin). MPD changes the playlist
    // when it contains radio stations.
    $interval(update_view, playlist_update_interval);
    //idle();
});
