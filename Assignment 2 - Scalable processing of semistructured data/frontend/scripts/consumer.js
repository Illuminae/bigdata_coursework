angular.module('consumer', [])
.controller('MainCtrl', function($scope, $http){
	'use strict';
$scope.title='Personas viculadas a la Universidad de los Andes';
$scope.description='Haga click en Buscar y luego realice el filtro que desee. Realice su búsqueda por alguno de los siguientes filtros';
$scope.SearchData = function () {
            $http.get('http://XXX.XXX.XXX.XXX:8080/uniandesdata')
            .then(function (response) {
                $scope.restData = response.data;
            });
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
