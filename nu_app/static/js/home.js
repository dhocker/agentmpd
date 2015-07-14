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
    $scope.title = "AgentMPD";

    // AJAX calls for transport functions

    translate_state = {};
    translate_state['play'] = 'Playing...';
    translate_state['pause'] = 'Paused';
    translate_state['stop'] = 'Stopped';

    $scope.get_current_status = function() {
        $http.post('/home/current_status', {}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
            }).
            error(function(data, status, headers, config) {
                $scope.status = "unknown";
            });
    };

    $scope.get_current_playlist = function() {
        $http.post('/home/current_playlist', {}).
            success(function(data, status, headers, config) {
                $scope.current_playlist = data;
            }).
            error(function(data, status, headers, config) {
                $scope.status = "unknown";
            });
    };

    $scope.playing = false;
    $scope.toggle_playing = function() {
        $scope.playing = !$scope.playing;
        $http.post('/home/toggle_play', {msg:'play'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_stop = function() {
        $http.post('/home/stop_play', {msg:'stop'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                $scope.playing = false;
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_first = function() {
        $http.post('/home/play_first', {msg:'first'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                $scope.playing = false;
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_previous = function() {
        $http.post('/home/play_previous', {msg:'previous'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                $scope.playing = false;
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_next = function() {
        $http.post('/home/play_next', {msg:'next'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                $scope.playing = false;
            }).
            error(function(data, status, headers, config) {
            });
    };

    $scope.play_last = function() {
        $http.post('/home/play_last', {msg:'last'}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                $scope.status = translate_state[data['state']];
                $scope.playing = false;
            }).
            error(function(data, status, headers, config) {
            });
    };

    // Initialize current status
    $scope.get_current_status();
    $scope.get_current_playlist();

    // Polled status update every 10 seconds
    $interval($scope.get_current_status, 10 * 1000)
});
