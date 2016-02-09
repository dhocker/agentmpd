
/*
    AgentMPD page app
*/

var app = angular.module('agentmpd', []);

// Change the interpolation marker from {{ }} to {= =} to avoid
// collision with the Jinga2 template system.
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{=');
    $interpolateProvider.endSymbol('=}');
});

// ta-scroll
// Track scrolling on an element
app.directive('taScroll', ['$parse', function($parse) {
  return {
    link: function(scope, element, attr) {
      element.on('scroll', function(event) {
        if (attr['taScroll']) {
            // ta-scroll="call_fn()"
            // Execute to attribute value
            $parse(attr['taScroll'])(scope);
        }
        else {
            // ta-scroll
            // Defaults to fixed call as if it were ta-scroll="on_scroll()"
            scope.on_scroll();
        }
      });
    }
  };
}]);

// Service for managing urls used in AJAX calls
app.factory('UrlService', function() {
    var factory = {};

    // Apply prefix to given url
    factory.url_with_prefix = function(url) {
       return "/mpd" + url;
    }
    return factory;
});
