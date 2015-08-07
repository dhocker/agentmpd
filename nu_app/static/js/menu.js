/*
    Common menu controller
*/
app.controller('menuController', function($scope, $http) {
    // Initialization

    // Menu customization

    // Menu functions

    $scope.menu_playlist_clear = function() {
        $http.put('/playlist/clear', {}).
            success(function(data, status, headers, config) {
                // These functions are out of scope
                //get_current_status();
                //get_current_playlist();
                showMessagebox($scope, "Clear Playlist", "Playlist has been cleared.");
            }).
            error(function(data, status, headers, config) {
                $scope.error = "Host communication error";
            });
    };

    $scope.menu_playlist_load = function() {
        alert("Load/Append has been invoked");
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
});
