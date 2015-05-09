/**
 *
 * @author: Lucy Linder
 * @date: 06.05.2015
 */


var app = angular.module('quotes.controller', []);


app.controller('QuotesController',
        ['$scope', 'QuotesFactory', // dependancy injection
        function ($scope, Factory) { // constructor: parameters must match dependancies !


            //call to the service
            $scope.refresh = function () {
                // get the quotes
                $scope.quotes = Factory.getall(function () {

                    $scope.qquotes = [];

                    function logArrayElements(element, index, array) {
                        var elt = {
                            date: new Date(element[0]).toDateString(),
                            author: element[1],
                            quote: element[2],
                            index: index
                        };

                        $scope.qquotes.push(elt);
                    }

                    $scope.quotes.forEach(logArrayElements);
                    $scope.getRandomQuote();
                });
            };

            $scope.addQuote = function (q) {

                callback = function(r) {
                    console.log(r);
                    if(r != "ERROR"){
                        $('#reset_add_form').click();
                        //$('#toggle_add_button').click();
                        //$('#toggle_add_button').removeClass('active');
                        $scope.refresh();
                    }
                };

                console.log(q);
                Factory.create(q, callback);
            };

            $scope.deleteQuote = function(q){
                console.log(q);
                console.log($scope.quotes[q['index']][0]);
                Factory.delete({id: $scope.quotes[q['index']][0]}, $scope.refresh)

            };

            $scope.showEditModal = function(q){
                console.log(q);
                $scope.cur_item = q;
                $('#modal_button').click();
            };

            $scope.editQuote = function(q){

                callback = function(){
                    $('#modal_button').click();
                    $scope.refresh();
                 };

                 var quote = $scope.quotes[q['index']];
                 quote[1] = q['author'];
                 quote[2] = q['quote'];
                 console.log(quote);

                 Factory.update(quote, callback);

            };

            $scope.getRandomQuote = function(){
                var index = Math.floor(Math.random() * $scope.quotes.length);
                $scope.randomQuote = $scope.qquotes[index];
            };

            $scope.refresh();
            $scope.show_add_button = false;
}]);
