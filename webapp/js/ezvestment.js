var app = angular.module('ezvestment', ['ezvestment-directives']).
    config(function ($routeProvider) {
        $routeProvider.
            when('/', {controller: AllocCtrl, templateUrl: 'alloc.html'}).
            when('/about', {templateUrl: 'about.html'}).
            when('/contact', {templateUrl: 'contact.html'}).
            otherwise({redirectTo: '/'});
    });

function NavCtrl($scope, $location) {
    console.log('# In NavCtrl');
    $scope.navClass = function(page) {
        var currentRoute = $location.path().substring(1) || 'home';
        return page === currentRoute ? 'active' : '';
    };
}

function AllocCtrl($scope) {
    console.log('# In AllocCtrl');

    $scope.portionBounds = 100;
    $scope.portionStocks = 0;
}