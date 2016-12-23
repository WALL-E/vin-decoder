var mainApp = angular.module("mainApp", ['ngPrettyJson']);

mainApp.controller("vinSearchController", function($scope, $http) {
    var baseUrl = "http://192.168.1.231:10089/vin/v1/";
    $scope.vinCode = "LVSHCAMB1CE054249";
    $scope.result = {};

    $scope.search = function() {
        $http({
            url: baseUrl + $scope.vinCode,
            method:'GET'
        }).success(function(data,header,config,status){
            $scope.result = data;
        }).error(function(data,header,config,status){
            console.log("search VinCode failed");
        });
    }
});
