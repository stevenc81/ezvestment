var app = angular.module('ezvestment', ['ezvestment-directives']).
    config(function ($routeProvider) {
        $routeProvider.
            when('/', {activetab: 'Home', controller: AllocCtrl, templateUrl: 'alloc.html'}).
            when('/About', {activetab: 'About', templateUrl: 'about.html'}).
            when('/Contact', {activetab: 'Contact', templateUrl: 'contact.html'}).
            otherwise({redirectTo: '/'});
    });

function NavCtrl($scope, $route) {
    console.log('# In NavCtrl');

    $scope.navItems = ['Home', 'About', 'Contact'];
    $scope.$route = $route;
}

function AllocCtrl($scope) {
    console.log('# In AllocCtrl');

    $scope.portionBounds = 100;
    $scope.portionStocks = 0;

    $scope.durations = ['1y', '5y', '10y', 'Set Target'];
    $scope.duration = '10y';

    // $scope.$watch('duration', function(v){
    //     console.log('# COntyroller - Duration changed to:', v);
    // });
}