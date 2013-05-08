var app = angular.module('ezvestment-directives', []);

app.directive('slider', function() {
    console.log('# In slider directive');
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.slider({
                range: true,
                min: 0,
                max: 100,
                values: 50,
                slide: function(event, ui) {
                    scope.portionBounds = 100 - ui.value;
                    scope.portionStocks = ui.value;

                    scope.$broadcast('slider-update');
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
        // require: 'slider',
        link: function(scope, element, attrs) {
            element.tooltip({
                placement: 'top',
                title: 'testing tooltip'
            });
        }
    };
});

app.directive('chart', function() {
   console.log('# In chart directive');
    return {
        link: function(scope, element, attrs) {
            var plot1 = $.jqplot ('chart1', [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], {
                    title: 'Main Chart',
                    axesDefaults: {
                        labelRenderer: $.jqplot.CanvasAxisLabelRenderer
                    },
                    series: [{
                        showMarker: false
                    }],
                    axes: {
                        xaxis: {
                            min: 0,
                            max: 10,
                            numberTicks: 11,
                            label: '% of Return'
                        },
                        yaxis : {
                            min: 0,
                            max: 100,
                            label: 'Year'
                        }
                    }
                });

            scope.$on('slider-update', function() {

                var newData = [];
                for (i = 1; i < 10; i++) {
                    x = i;
                    y = scope.portionStocks*i/10;
                    newData.push([x, y]);
                }

                plot1.series[0].data = newData;
                // scope.plot1.resetAxesScale();
                plot1.replot();

            });

            scope.$on('duration-update', function() {
                console.log('# duration for plot: ');
            });
        }
    };
});

app.directive('buttonsRadio', function() {
    return {
        restrict: 'E',
        scope: { model: '=', options:'='},
        controller: function($scope) {
            $scope.activate = function(option){
                $scope.model = option;
                                // $scope.$broadcast('duration-update');
                // $scope.$apply();
            };
        },
        link: function(scope, element, attrs) {
            element.bind('click', function(e) {
                // console.log('# duration for plot: ');
                scope.$broadcast('duration-update');
                scope.$apply();
            });
        },
        template: "<button type='button' class='btn' "+
                    "ng-class='{active: option == model}'"+
                    "ng-repeat='option in options' "+
                    "ng-click='activate(option)'>{{option}} "+
                  "</button>"
    };
});