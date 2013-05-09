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
                        label: 'Year'
                    },
                    yaxis : {
                        min: 0,
                        max: 100,
                        label: '% of Return'
                    }
                }
            });

            function redraw(year) {
                var regex = /([0-9]+)\w/;
                var matches = regex.exec(year);

                if (matches) {
                    var durationYear = matches[1];

                    var newData = [];
                    for (i = 1; i < durationYear; i ++) {
                        x = i;
                        y = scope.portionStocks*i/10;
                        newData.push([x, y]);
                    }

                    plot1.series[0].data = newData;
                    // plot1.resetAxesScale();
                    plot1.replot();
                }
            }

            scope.$on('slider-update', function() {
                redraw(scope.mySelection);
            });

            scope.$on('btn-grp-update', function() {
                // console.log('# Duration changed to:', option);
                redraw(scope.mySelection);
            });
        }
    };
});

app.directive('buttonsRadio', function() {
    return {
        restrict: 'E',
        scope: { model: '=', options:'='},
        controller: function($scope, $rootScope) {
            $scope.activate = function(option) {
                $scope.model = option;
                $rootScope.$broadcast('btn-grp-update');
            };
        },
        template: "<button type='button' class='btn' "+
                    "ng-class='{active: option == model}'"+
                    "ng-repeat='option in options' "+
                    "ng-click='activate(option)'>{{option}} "+
                  "</button>"
    };
});