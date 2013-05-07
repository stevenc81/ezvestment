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

    $scope.navItems = [
        {'name': 'Home', 'url': 'home'},
        {'name': 'About', 'url': 'about'},
        {'name': 'Contact', 'url': 'contact'}
    ];

    $scope.navClass = function(page) {
        var currentRoute = $location.path().substring(1) || 'home';
        return page === currentRoute ? 'active' : '';
    };
}

function AllocCtrl($scope) {
    console.log('# In AllocCtrl');

    $scope.portionBounds = 100;
    $scope.portionStocks = 0;

    $scope.myOptions = ['1y', '5y', '10y', 'Set Target'];
    $scope.myModel = '10y';

    $scope.$watch('myModel', function(v){
        console.log('# Duration changed to:', v);
    });
}