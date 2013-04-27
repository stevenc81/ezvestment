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
                    scope.$apply();
                }
            });
        }
    };
});

