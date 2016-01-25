var api_tag = angular.module('helptux.api_tag', ['helptux.api_core']);

api_tag.factory('ApiTag', ['$rootScope', 'ApiCore',
    function ($rootScope, ApiCore) {
        var ApiTag = function() {
            this.a_api = new ApiCore();
        };

        ApiTag.prototype.listTags = function() {
            this.a_api.list('tag').then(function success(api_data) {
                $rootScope.available_tags = api_data.data.data;
            });
        };

        return ApiTag;
    }]);