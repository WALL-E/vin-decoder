var mainApp = angular.module("mainApp", ['ngPrettyJson']);

mainApp.controller("vinSearchController", function($scope, $http) {
    var baseUrl = "http://172.28.32.101:10090/vin/v1/";
    $scope.vinCode = "LVSHCAMB1CE054249";
    $scope.result = {};
    $scope.search = function(vinCode) {
        $scope.vinCode = vinCode;
        $http({
            url: baseUrl + vinCode,
            method:'GET'
        }).success(function(data,header,config,status){
            $scope.result = data;
        }).error(function(data,header,config,status){
            console.log("search VinCode failed");
        });
    }
});
