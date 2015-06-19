/**
 * Created by Lucy on 09/05/15.
 */


var app = angular.module('quotes.filter', []);

app.filter("multiWordFilter", function($filter){
    /* filter the quotes based on multiple words (not necessarily the exact text) */
    return function(inputArray, searchText){
        if(searchText == undefined) return inputArray;
        console.log(searchText);
        var wordArray = searchText['$'].toLowerCase().split(/\s+/);
        var wordCount = wordArray.length;
        for(var i=0;i<wordCount;i++){
            inputArray = $filter('filter')(inputArray, wordArray[i]);
        }
        return inputArray;
    }
});

app.filter('newlines', function() {
  // see http://stackoverflow.com/questions/13964735/angularjs-newline-filter-with-no-other-html
  return function(text) {
    return text == undefined ? text : text.split(/\n/g);
  };
});
