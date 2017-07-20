angular.module('tweetreader', [])
    .controller('TweetCtrl', function($scope, $http) {
        'use strict';
        $scope.title = 'Análisis de Sentimientos Twitter';
        $scope.description = 'Haga click en la variable que desea analizar';

        $scope.showPol = false;
        $scope.showSent = false;
        $scope.showRob = false;
        $scope.showRob2 = false;
        $scope.showExam = false;

        //Produce a random number between 0 and 9 to
        //obtain a random tweet from the example list
        function generateRandomIndex(){
            return Math.floor(Math.random() * 9)  
        }

        $scope.SearchPol = function() {

            $scope.showPol = true;
            $scope.showSent = false;
            $scope.showRob = false;
            $scope.showRob2 = false;
            $scope.showExam = false;
 
            $http.get('http://XXX.XXX.XXX.XXX:8080/twitter/polarity')
                .then(function(response) {
                    $scope.restDataPol = response.data;
                })
        }
        $scope.SearchSent = function() {

            $scope.showPol = false;
            $scope.showSent = true;
            $scope.showRob = false;
            $scope.showRob2 = false;
            $scope.showExam = false;
 
            $http.get('http://XXX.XXX.XXX.XXX:8080/twitter/sentiment')
                .then(function(response) {
                    $scope.restDataSent = response.data;
                    $scope.nombre2="Personaje";
                    $scope.neg="Negativo";
                    $scope.cero="Neutro";
                    $scope.pos="Positivo";
                })
        }


        $scope.SearchRob = function() {

            $scope.showPol = false;
            $scope.showSent = false;
            $scope.showRob = true;
            $scope.showRob2 = false;
            $scope.showExam = false;

            $http.get('http://XXX.XXX.XXX.XXX:8080/twitter/robots')
                .then(function(response) {
                    $scope.restDataRob = response.data["robot-by-followers-and-favourites"];
                })
        }

        $scope.SearchRob2 = function() {

            $scope.showPol = false;
            $scope.showSent = false;
            $scope.showRob = false;
            $scope.showRob2 = true;
            $scope.showExam = false;

            $http.get('http://XXX.XXX.XXX.XXX:8080/twitter/robots')
                .then(function(response) {
                    $scope.restDataRob2 = response.data["robots-by-rt-to-same-account"];
                })
        }


        $scope.SearchExam = function() {

            $scope.showPol = false;
            $scope.showSent = false;
            $scope.showRob = false;
            $scope.showRob2 = false;
            $scope.showExam = true;

            $http.get('http://XXX.XXX.XXX.XXX:8080/twitter/example')
                .then(function(response) {

                    var tweetNO = {}
                    tweetNO['type'] = 'Objetivo Negativo';
                    tweetNO['content'] = 
                        response.data['polarity-negative-objective'][generateRandomIndex()].text;

                    var tweetNS = {}
                    tweetNS['type'] = 'Subjetivo Negativo';
                    tweetNS['content'] = 
                        response.data['polarity-negative-subjetive'][generateRandomIndex()].text;

                    var tweetPN = {}
                    tweetPN['type'] = 'Polaridad Neutral';
                    tweetPN['content'] = 
                        response.data['polarity-neutral'][generateRandomIndex()].text;

                    var tweetPO = {}
                    tweetPO['type'] = 'Objetivo Positivo';
                    tweetPO['content'] = 
                        response.data['polarity-positive-objective'][generateRandomIndex()].text;

                    var tweetPS = {}
                    tweetPS['type'] = 'Subjetivo Positivo';
                    tweetPS['content'] = 
                        response.data['polarity-positive-subjetive'][generateRandomIndex()].text;
                    
                    var tweetN = {}
                    tweetN['type'] = 'Sentimiento Negativo';
                    tweetN['content'] = 
                        response.data['sentiment-negative'][generateRandomIndex()].text;

                    var tweetSN = {}
                    tweetSN['type'] = 'Sentimiento Neutro';
                    tweetSN['content'] = 
                        response.data['sentiment-neutral'][generateRandomIndex()].text;
                    
                    var tweetSP = {}
                    tweetSP['type'] = 'Sentimiento Positivo';
                    tweetSP['content'] = 
                        response.data['sentiment-positive'][generateRandomIndex()].text;

                    var tweets = [];

                    tweets.push(tweetNO);
                    tweets.push(tweetNS);
                    tweets.push(tweetPN);
                    tweets.push(tweetPO);
                    tweets.push(tweetPS);
                    tweets.push(tweetN);
                    tweets.push(tweetSN);
                    tweets.push(tweetSP);
                    
                    $scope.tweets = tweets;
                })
        }
    });

