var app = angular.module('ezvestment-directives', []);

app.directive('slider', function() {
    console.log('# In slider directive');
    return {
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

app.directive('tooltip', function () {
    console.log('# In Tooltip directive');
    return {
        restrict:'A',
        link: function(scope, element, attrs)
        {
            element.tooltip({
                placement: 'top',
                title: attrs.tooltip
            });
        }
    };
});