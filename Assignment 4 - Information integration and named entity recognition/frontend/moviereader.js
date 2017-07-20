angular.module('moviereader', ['ngGoogleMaps'])
  .controller('MovieCtrl', function($scope, $http) {
    'use strict';
    $scope.title = 'Análisis de contenido sobre entreteniemiento';
    $scope.description = 'Ingrese el contenido que desea buscar luego haga click en Datos para conocer información relacionada y comentarios o en Ubicación para ver el mapa';
    $scope.busqueda = '';


$scope.sendData = function () {
  //Making sure request contains empty strings in case no filters for title or description are given
  
  var query = ($scope.busqueda == null ? '' : String($scope.busqueda));
  
  //Stripping HTML from Strings
  function strip(html)  {
     var tmp = document.createElement("DIV");
     tmp.innerHTML = html;
     return tmp.textContent || tmp.innerText || "";
  }

  var data = {
  'text' : query
  };

  //Retrieving all enriched question information that match the search term

  $http.post('http://XXX.XXX.XXX.XXX:8080/movies/search', data).then(
    function successCallback(response) {
      $scope.restdata = [];
      //Check if value null, if not iterate through all results for processing
      if(response.data.list){
        for (var i = 0; i < response.data.list.length; i++){
          var obj = response.data.list[i];
          //Create new entry and strip question from HTML tags
          var entry = {
            "summary" : strip(obj.summary),
            "name"    : "",
            "relatives": "",
            "places"  : "",
            "coordinates": [],
            "entities" : ""
          };
          //alert("Entering for loop round " + i + " out of " + response.data.list.length);
          for (var j = 0; j<obj.entities.entity_list.length; j++){
            //alert("Entry loop2 number " + j + " of total of " + obj.entities.entity_list.length);
            //Check if the enriched entity has a type to identify it
            if (obj.entities.entity_list[j].resume !== undefined && obj.entities.entity_list[j].resume.type !== undefined){
              switch(obj.entities.entity_list[j].resume.type){
                //Type 0: Person, so we extract name, birthplace, birthdate and potential relatives/partners 
                case 0:
                  entry.name += obj.entities.entity_list[j].resume.name;
                  if (obj.entities.entity_list[j].resume.birthdate){
                    entry.name += " born " + obj.entities.entity_list[j].resume.birthdate;
                  }
                  if (obj.entities.entity_list[j].resume.birthplace){
                    entry.name += " in " + obj.entities.entity_list[j].resume.birthplace;
                  }
                  entry.name += " | "
                  if (obj.entities.entity_list[j].resume.partners){
                    entry.relatives += "Partners of " + obj.entities.entity_list[j].resume.name + ": " + obj.entities.entity_list[j].resume.partners;
                  }
                  if (obj.entities.entity_list[j].resume.relatives){
                    entry.relatives += "Relatives of " + obj.entities.entity_list[j].resume.name + ": " + obj.entities.entity_list[j].resume.relatives;
                  }
                  break;
                case 1:
                  entry.places += obj.entities.entity_list[j].resume.name;
                  if (obj.entities.entity_list[j].resume.capital){
                    entry.places += " [capital: " + obj.entities.entity_list[j].resume.capital + "]";
                  }
                  if (obj.entities.entity_list[j].resume.country){
                    entry.places += " is located in " + obj.entities.entity_list[j].resume.country;
                  }
                  entry.places += " | ";
                  if (obj.entities.entity_list[j].resume.lat && obj.entities.entity_list[j].resume.lon){
                    entry.coordinates.push({
                      "lat" : obj.entities.entity_list[j].resume.lat,
                      "lon" : obj.entities.entity_list[j].resume.lon
                    })
                  }
                  break;
                case 2:
                  entry.entities += obj.entities.entity_list[j].resume.name;
                  if (obj.entities.entity_list[j].resume.dbptype){
                    entry.entities += " [" + obj.entities.entity_list[j].resume.dbptype + "]";
                  }
                  if (obj.entities.entity_list[j].resume.city){
                    entry.entities += " in " + obj.entities.entity_list[j].resume.city;
                  }
                  if (obj.entities.entity_list[j].resume.country){
                    entry.entities += " in " + obj.entities.entity_list[j].resume.country;
                  }
                  if (obj.entities.entity_list[j].resume.semtype){
                    entry.entities += " | Categorization: " + obj.entities.entity_list[j].resume.semtype;
                  }
                  entry.entities += "; ";
                  break;
              }
            } else { 
              //skip empty entry
            }
          }
        $scope.restdata.push(entry)
        }
      } else {
        alert("Could not strip HTML tags from data")
      }
    //Error if no data has been received
    }, function errorCallback(response) {
      alert("Imposible recibir archivo.")
      });

    //alert(String(title) + String(description) + String($scope.category));
};


//Initializing the Map over Bogota
  $scope.initMap = function() {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 5,
      center : {lat : 4.7110 , lng : -74.0721}
    });
//On Buttonclick, update the map and paint all the Markers that have been found.
  $scope.updateMap = function(){
    var bounds = new google.maps.LatLngBounds();
    console.log($scope.selectedEntry);
    if($scope.selectedEntry !== undefined && $scope.selectedEntry.coordinates.length != 0){

      for(var i = 0; i < $scope.selectedEntry.coordinates.length; i++){
        console.log($scope.selectedEntry);
            var position = new google.maps.LatLng($scope.selectedEntry.coordinates[i].lat, $scope.selectedEntry.coordinates[i].lon);
            bounds.extend(position);
            var marker = new google.maps.Marker({
              position: position,
              map: map,
            });
      }
      map.fitBounds(bounds);
      var listener = google.maps.event.addListenerOnce(map, "idle", function() { 
      if (map.getZoom() > 16) map.setZoom(10); 
      });
  } else {alert("No coordinates are associated with this question.")}
}
      

}

});

