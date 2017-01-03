var mainApp = angular.module("mainApp", ['ngPrettyJson']);

mainApp.controller("vinSearchController", function($scope, $http) {
    $scope.baseUrl = "http://172.28.32.101:10090/vin/v1";
    //$scope.baseUrl = "http://192.168.1.231:10090/vin/v1";
    $scope.vinCode = "LVSHCAMB1CE054249";
    $scope.result = {};
    $scope.search = function(vinCode) {
        $scope.vinCode = vinCode;
        $http({
            url: $scope.baseUrl + "/" + vinCode,
            method:'GET',
            params:{
                'is_realtime':'true'
            }
        }).success(function(data,header,config,status){
            $scope.result = data;
        }).error(function(data,header,config,status){
            console.log("search VinCode failed");
        });
    }
});
