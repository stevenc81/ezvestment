var app = angular.module('ezvestment', ['$strap.directives', 'ezvestment-directives']).
    config(function ($routeProvider) {
        $routeProvider.
            when('/', {controller: AllocCtrl, templateUrl: 'alloc.html'}).
            otherwise({redirectTo: '/'});
    });

function HeaderCtrl($scope) {
    console.log('# In HeaderCtrl');
}

function AllocCtrl($scope) {
    console.log('# In AllocCtrl');
}