var app = angular.module('ezvestment', ['$strap.directives']).
    config(function ($routeProvider) {
        $routeProvider.
            when('/', {controller: AllocCtrl, templateUrl: 'alloc.html'}).
            otherwise({redirectTo: '/'});
    });

function AllocCtrl($scope) {
    console.log('# In IndexCtrl');
    $scope.project_name = 'Ezvestment';
}