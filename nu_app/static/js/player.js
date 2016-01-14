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
app.controller('homeController', ["$scope", "$http", "$interval", "$timeout", function($scope, $http, $interval, $timeout) {
    // Initialization

    $scope.title = "AgentMPD";

    // Menu customization
    $("#menu-player").hide();

    var translate_state = {};
    translate_state['play'] = 'Playing...';
    translate_state['pause'] = 'Paused';
    translate_state['stop'] = 'Stopped';

    var status_update_interval = 10 * 1000; // 10 seconds
    var playlist_update_interval = 30 * 1000; // 30 seconds

    // Scrolling is tracked by the scroll directive
    $scope.manual_scrolling = false;

    $scope.playing = false;
    $scope.current_playlist = {"playlist": []};
    $scope.error = "";

    // Create volume bar slider
    var volumebar = $( "#volumebar" );
    create_slider( "#volumebar", "vertical", 0, 100, 50, on_volumebar_change );

    // Create time bar slider
    var timebar = $("#timebar");
    create_slider( "#timebar", "horizontal", 0, 100, 0, on_timebar_change );

    // Update the status of the transport, now playing and playlist
    function update_status() {
        for (var i = 0; i < $scope.current_playlist.playlist.length; i++)
        {
            var pe = $scope.current_playlist.playlist[i];
            if (pe.pos == $scope.currently_playing.song)
            {
                // Use the Bootstrap class to mark the now playing song
                pe["class"] = "success";
            }
            else
            {
                // Originally, this code managed the striping. Now, we
                // let Bootstrap handle the striping.
                pe["class"] = "";
            }
        }

        $scope.status = translate_state[$scope.currently_playing['state']];
        $scope.playing = ($scope.status == translate_state['play']);
        $scope.volume = parseInt($scope.currently_playing['volume']);
        // This is our best guess at whether a record track or radio station is playing
        $scope.playing_track = $scope.currently_playing['file'].substring(0, 7) != "http://";
        update_volume_bar($scope.volume);
        update_play_time();
        // Options
        $scope.random = parseInt($scope.currently_playing['random']);
        $scope.repeat = parseInt($scope.currently_playing['repeat']);
        $scope.single = parseInt($scope.currently_playing['single']);
        $scope.consume = parseInt($scope.currently_playing['consume']);
        $scope.xfade = parseInt($scope.currently_playing['xfade']);
        // Now playing (only if there is a playlist)
        if (!$scope.manual_scrolling) {
            $scope.show_now_playing($scope.currently_playing["pos"]);
        }
    };

    function update_volume_bar(value) {
        volumebar.slider( "value", value );
    };

    function get_current_status() {
        $http.get('/player/currentstatus', {}).
            success(function(data, status, headers, config) {
                $scope.currently_playing = data;
                update_status();
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.status = "";
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to communicate with host server";
                }
            });
    };

    function get_settings() {
        $http.get("/settings").
            success(function(data, status, headers, config) {
                $scope.host = data["host"];
                $scope.port = data["port"];
                $scope.status_update_interval = data["status_update_interval"];
                $scope.playlist_update_interval = data["playlist_update_interval"];
                $scope.volume_increment = data["volume_increment"];
            }).
            error(function(data, status, headers, config) {
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to communicate with host server";
                }
            });
    }

    $scope.show_error = function() {
        // How do you clone this string???
        return $scope.error;
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
                $scope.status = "";
                $scope.error = "Server communication error";
            });
    };

    function get_current_playlist() {
        $http.get('/cpl/currentplaylist', {}).
            success(function(data, status, headers, config) {
                $scope.current_playlist = data;
                update_status();
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.status = "";
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to get current playlist from host";
                }
            });
    };

    function update_view() {
        get_current_playlist();
    };

    // AJAX calls for transport functions

    function post_transport(url, data) {
        $http.post(url, data).
            success(function(data, status, headers, config) {
                // After post completes, refresh status
                get_current_status();
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.status = "";
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to communicate with host server";
                }
            });
    };

    function put_transport(url, data) {
        $http.put(url, data).
            success(function(data, status, headers, config) {
                // After put completes, refresh status
                get_current_status();
                $scope.error = "";
            }).
            error(function(data, status, headers, config) {
                $scope.status = "";
                if (data && data.message) {
                    $scope.error = data.message;
                }
                else {
                    $scope.error = "Unable to communicate with host server";
                }
            });
    };

    $scope.toggle_playing = function() {
        put_transport('/player/status', {'playstatus':'toggle'});
    };

    $scope.play_stop = function() {
        put_transport('/player/status', {'playstatus':'stop'});
    };

    $scope.play_first = function() {
        put_transport('/player/currentsong/first', {});
    };

    $scope.play_previous = function() {
        put_transport('/player/currentsong/previous', {});
    };

    $scope.play_next = function() {
        put_transport('/player/currentsong/next', {});
    };

    $scope.play_last = function() {
        put_transport('/player/currentsong/last', {});
    };

    $scope.play_song = function(pos) {
        put_transport('/player/currentsong/' + pos, {});
    };

    // Options

    $scope.random_changed = function() {
        put_transport('/player/status', {'random':$scope.random});
    };

    $scope.consume_changed = function() {
        put_transport('/player/status', {'consume':$scope.consume});
    };

    $scope.repeat_changed = function() {
        put_transport('/player/status', {'repeat':$scope.repeat});
    };

    $scope.single_changed = function() {
        put_transport('/player/status', {'single':$scope.single});
    };

    // Menu functions

    $scope.menu_update_database = function() {
        put_transport('/player/musicdatabase', {});
    };

    $scope.menu_playlist_rename = function() {
        alert("Rename has been invoked");
    };

    // User scrolled to the playlist
    $scope.on_scroll = function() {
        //$scope.manual_scrolling = true;
    };

    // t is in seconds (e.g. 300 = 00:05:00)
    $scope.format_time = function(t) {
        var tt = parseInt(String(t).replace(":", "."));

        var hh_part = "";
        var hh = parseInt(tt / 3600);
        if (hh > 0) {
            hh_part = String(hh) + ":";
        }

        var mm = parseInt((tt - (hh * 3600)) / 60);
        var mm_part = String(mm) + ":";
        if (hh_part.length > 0 && mm < 10) {
            mm_part = "0" + mm_part;
        }

        var ss = parseInt(tt % 60);
        var ss_part = String(ss);
        if (ss < 10) {
            ss_part = "0" + ss_part;
        }

        return hh_part + mm_part + ss_part;
    };

    function update_play_time() {
        // TODO This does not work for radio stations.
        // There is no notion of duration for a radio station. As a result,
        // the elapsed time is always >= duration and get_current_status gets
        // called repeatedly.
        if ($scope.playing) {
            var elapsed = parseInt($scope.currently_playing.elapsed);
            var duration = parseInt($scope.currently_playing.time);
            if (duration != parseInt(timebar.slider("option", "max"))) {
                timebar.slider("option", "max", duration);
            }
            timebar.slider("value", elapsed);
        }
    };

    // Called every second...
    function increment_play_time() {
        if ($scope.playing) {
            $scope.currently_playing['elapsed'] = parseFloat($scope.currently_playing['elapsed']) + 1.0;
            if (!$scope.playing_track) {
                $scope.currently_playing['time'] = parseFloat($scope.currently_playing['time']) + 1.0;
            }
            update_play_time();
        }
    };

    // Scroll the playlist table to the given row
    $scope.show_now_playing = function(row_id) {
        try {
            var tr = $("#" + row_id);
            $("#playlist-content").scrollTop(0);
            var vpos = tr.position().top;
            var h = tr.height();
            $("#playlist-content").scrollTop(vpos - h);
        }
        catch(err) {
            $scope.error = err.message;
        }

        $scope.manual_scrolling = false;
    };

    function showMessagebox($scope, header, body) {
        $scope.messagebox_header = header;
        $scope.messagebox_body = body;
        $("#menu-messagebox").modal('show');
    };

	// Create a jQuery UI slider
	function create_slider(id, orientation, min, max, init_value, onslide) {
		// Create slider with initial values for min, max and value
		$(id).slider({
		    "animate": true,
		    "range": "min",
			"orientation": orientation,
		  	"max": max,
			"min": min,
			"value": init_value,
			"slide": onslide
		});
	}

	// Handle volume bar slider changes made by user
	function on_volumebar_change( event, ui ) {
        var v = parseInt(ui.value);
	    if ($scope.volume != v) {
            put_transport('/player/volumelevel', {'amount': v});
        }
	}

    // Handle song time changes made by user
	function on_timebar_change(event, ui) {
	    // The song postion in seconds into the song
        var v = parseInt(ui.value);
        put_transport('/player/songposition', {'time': v});
	}

    // Initialize current status
    get_settings();
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

    // Set up time to advance play time when playing
    $interval(increment_play_time, 1000);

}]);
