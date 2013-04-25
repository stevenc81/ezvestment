var app = angular.module('ezvestment', ['$strap.directives']).
    config(function ($routeProvider) {
        $routeProvider.
            when('/', {controller: IndexCtrl, templateUrl: 'index.html'});
    });

function IndexCtrl($scope) {
    console.log('# In IndexCtrl');
    $scope.project_name = 'Ezvestment';
}