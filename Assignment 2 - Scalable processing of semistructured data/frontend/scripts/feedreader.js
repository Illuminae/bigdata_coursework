angular.module('feedreader', [])
.controller('RSSCtrl', function($scope, $http){
	'use strict';
$scope.title2='Tus noticias preferidas - sencillo a filtrar';
$scope.description2='Escoja el rango de fecha para su consulta y realice su búsqueda por alguno de los filtros, después haga click en Filtrar Noticias';
$scope.category = '';
$scope.descripion = '';
$scope.title = '';

$scope.sendData = function (tit, des, cat) {
	//Making sure request contains empty strings in case no filters for title or description are given
	var title = (tit == null ? '' : String(tit));
    var description = (des == null ? '' : String(des));
    var data = {
		'title' : title,
		'description' : description,
		'category' : $scope.category
    };
    //console.log(data);

    $http.post('http://XXX.XXX.XXX.XXX:8080/mashup/rss', data).then(
    	//Extracts the three different element types from the received JSON file so that they can individuall by iterated in the html
	    function successCallback(response) {
	    	console.log(response.data.nofilter);
	    	console.log(response.data.regex);
	    	console.log(response.data.xquery);
	    	var data = response.data;

	    	//Removing duplicates from received data as for some reason Google News contains duplicates
	    	console.log(typeof data.regex);
			var regexFiltered= data.regex.filter(function(item) { 
			   return item.title !== 'Ciencia y Tecnología: Google Noticias';  
			});
			regexFiltered = regexFiltered.filter(function(item) { 
			   return item.title !== 'Economía: Google Noticias';  
			});
			regexFiltered = regexFiltered.filter(function(item) { 
			   return item.title !== 'Espectáculos: Google Noticias';  
			});
			// var xqueryFiltered= data.xquery.filter(function(item) { 
			//    return item.title !== 'Ciencia y Tecnología: Google Noticias';  
			// });
			// xqueryFiltered = xqueryFiltered.filter(function(item) { 
			//    return item.title !== 'Economía: Google Noticias';  
			// });
			// xqueryFiltered = xqueryFiltered.filter(function(item) { 
			//    return item.title !== 'Espectáculos: Google Noticias';  
			// });
			var unfilteredRSS= data.nofilter.filter(function(item) { 
			   return item.title !== 'Ciencia y Tecnología: Google Noticias';  
			});
			unfilteredRSS = unfilteredRSS.filter(function(item) { 
			   return item.title !== 'Economía: Google Noticias';  
			});
			unfilteredRSS = unfilteredRSS.filter(function(item) { 
			   return item.title !== 'Espectáculos: Google Noticias';  
			});

			$scope.regexRSS = regexFiltered;
			$scope.xqueryRSS = data.xquery;
			$scope.unfilteredRSS = unfilteredRSS;
		//Error if no data has been received
	}, function errorCallback(response) {
		alert("Unable to retrieve RSS feeds.")
  	});
    //alert(String(title) + String(description) + String($scope.category));
};

$scope.onChoice = function(input){
    $scope.category = String(input);
};
$scope.stripString = function(s) {
	if (s == null){
    	return '';
	}
	s = s.replace(/[\[\]']+/g, '');
	s = s.replace(/\\t+/g, '');
	s = s.replace(/\s\s+/g, ' ');
	return s;
};

});
