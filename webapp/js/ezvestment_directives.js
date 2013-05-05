var app = angular.module('ezvestment-directives', []);

app.directive('slider', function() {
    console.log('# In slider directive');
    return {
        controller: AllocCtrl,
        link: function(scope, element, attrs) {
            element.slider({
                range: true,
                min: 0,
                max: 100,
                values: 50,
                slide: function(event, ui) {
                    console.log(ui.value);
                    scope.slider_value = ui.value;
                    scope.portionBounds = 100 - ui.value;
                    scope.portionStocks = ui.value;
                    scope.$apply();
                }
            });
        }
    };
});

app.directive('tooltip', function() {
    console.log('# In Tooltip directive');
    return {
        restrict:'A',
        require: 'slider',
        link: function(scope, element, attrs) {
            element.tooltip({
                placement: 'top',
                title: 'jdfh'
            });
        }
    };
});

app.directive('chart', function() {
   console.log('# In chart directive');
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.ready(function(){
                var plot1 = $.jqplot ('chart1', [[3,7,9,1,5,3,8,2,5]], {
                    title: 'Main Chart'
                });
            });
        }
    };
});