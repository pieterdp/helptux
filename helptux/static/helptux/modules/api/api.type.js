var api_type = angular.module('helptux.api_type', ['helptux.api_core']);

api_type.factory('ApiType', ['$rootScope', 'ApiCore',
    function ($rootScope, ApiCore) {
        var ApiType = function() {
            this.a_api = new ApiCore();
        };

        ApiType.prototype.list = function() {
            this.a_api.list('type').then(function success(api_data) {
                $rootScope.available_types = api_data.data.data;
            });
        };

        return ApiType;
    }]);