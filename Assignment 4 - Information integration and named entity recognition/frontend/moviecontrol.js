'use strict';

/**
 * @ngdoc function
 * @name projectAngularApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the projectAngularApp
 */
angular.module('projectAngularApp',[])
  .controller('MovieCtrl', function () {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
