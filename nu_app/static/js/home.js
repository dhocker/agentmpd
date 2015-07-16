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

app.controller('homeController', function($scope, $http, $interval) {
    // Initialization

    $scope.title = "AgentMPD";

    var translate_state = {};
    translate_state['play'] = 'Playing...';
    translate_state['pause'] = 'Paused';
    translate_state['stop'] = 'Stopped';

    var status_update_interval = 10 * 1000; // 10 seconds

    $scope.playing = false;

    function update_status() {
        // Remove existing marking. Note there is only one element
        // with the playlist-active class.
        $(".playlist-entry").removeClass("playlist-active");
        if ($(".xalt"))
        {
            // Restore alt class
            $(".xalt").removeClass("xalt").addClass("alt");
        }

        // Mark current song in playlist
        var active = $("#" + String($scope.currently_playing.song));
        // If the target element has the alt class, it must be removed.
        // For whatever reason, it cannot coexist with the active class.
        if (active.hasClass("alt"))
        {
            // Change alt to xalt so we can find it later
            active.removeClass("alt").addClass("xalt");
        }
        active.addClass("playlist-active");

        // Update transport controls status
        // TODO Refactor/improve this constant
        $scope.playing = ($scope.status == 'Playing...');
    };

    function get_current_status() {
        $http.get('/home/current_status', {}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                // Update current marking
                update_status();
            }).
            error(function(data, status, headers, config) {
                $scope.status = "unknown";
            });
    };

    function get_current_playlist() {
        $http.get('/home/current_playlist', {}).
            success(function(data, status, headers, config) {
                $scope.current_playlist = data;
                console.log("Get current playlist success");
            }).
            error(function(data, status, headers, config) {
            });
    };

    function update_view() {
        // This just doesn't work because of race conditions.
        // The call to get_current_playlist returns before the
        // http call completes. Therefore we actually exit this
        // function before the http request completes.
        // Candidate solution: Mark the playlist entry with a
        // class that indicates if the entry is/isnot the current entry.
        get_current_playlist();
        update_status();
        console.log("Update view exiting");
    };

    // AJAX calls for transport functions

    $scope.toggle_playing = function() {
        $scope.playing = !$scope.playing;
        $http.post('/home/toggle_play', {msg:'play'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_stop = function() {
        $http.post('/home/stop_play', {msg:'stop'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_first = function() {
        $http.post('/home/play_first', {msg:'first'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_previous = function() {
        $http.post('/home/play_previous', {msg:'previous'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_next = function() {
        $http.post('/home/play_next', {msg:'next'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_last = function() {
        $http.post('/home/play_last', {msg:'last'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_song = function(pos) {
        $http.post('/home/play_song/' + pos).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                // Update current marking
                update_status();
            }).
            error(function(data, status, headers, config) {
            });
    };

    // Initialize current status
    get_current_playlist();
    get_current_status();

    // Polled status update every 10 seconds
    // This isn't very efficient, but for now it will have to do.
    // We'll need to figure out how to use the MPD idle API.
    $interval(get_current_status, status_update_interval);
    $interval(update_view, 30 * 1000);
});
