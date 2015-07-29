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
                get_current_status();
                get_current_playlist();
            }).
            error(function(data, status, headers, config) {
                $scope.status = "Host communication error";
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
});
