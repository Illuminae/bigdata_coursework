angular.module('graphread', [])
.controller('GRAPHCtrl', function($scope, $http){
	'use strict';
$scope.title2='Relaciones Wikipedia';
$scope.description2='Elija el rango de fechas para su consulta y realice la búsqueda por algúno de los filtros, después haga click en Generar Grafo';
$scope.persona = '';
$scope.pais = '';
$scope.ciudad = '';


$(function() {
        //for displaying datepicker
        $('.date1').datepicker({
            format: 'yyyy-mm-dd',
            language:'fa'
        });
        //for getting input value
        $('.date1').on("changeDate", function() {
            $scope.fechain = $(".date1").val();
        });

     });


$(function() {
        //for displaying datepicker
        $('.date2').datepicker({
            format: 'yyyy-mm-dd',
            language:'fa'
        });
        //for getting input value
        $('.date2').on("changeDate", function() {
            $scope.fechafin = $(".date2").val();
        });

     });


$scope.sendData = function (per, pai, ciu, fei,fef) {
	//Making sure request contains empty strings in case no filters for title or description are given
	var persona = (per == null ? '' : String(per));
    var pais = (pai == null ? '' : String(pai));
    var ciudad = (ciu == null ? '' : String(ciu));
    
    var data = {
		'persona' : persona,
		'pais' : pais,
		'ciudad': ciudad, 
        'fechain': $scope.fechain,
		'fechafin': $scope.fechafin
    };


        //for displaying datepicker

    //console.log(data);

    $http.post('http://localhost:3000/db', data).then(
    	//Extracts the three different element types from the received JSON file so that they can individuall by iterated in the html
	    function successCallback(response) {
	    	$scope.restdata = response.data;
	//Error if no data has been received
	}, function errorCallback(response) {
		alert("Imposible recibir archivo.")
  	});
  
    //alert(String(title) + String(description) + String($scope.category));
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
