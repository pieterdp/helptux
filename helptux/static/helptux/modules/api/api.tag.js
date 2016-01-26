var api_tag = angular.module('helptux.api_tag', ['helptux.api_core']);

api_tag.factory('ApiTag', ['$rootScope', 'ApiCore',
    function ($rootScope, ApiCore) {
        var ApiTag = function() {
            this.a_api = new ApiCore();
        };

        ApiTag.prototype.list = function() {
            this.a_api.list('tag').then(function success(api_data) {
                $rootScope.available_tags = api_data.data.data;
            });
        };
        
        ApiTag.prototype.store = function(tag_name) {
            var tag = {
                tag: tag_name
            };
            var self = this;
            this.a_api.create(tag, 'tag').then(function success(){
                self.list();
            }, function error(data){
                console.log(data);
            });
        };

        ApiTag.prototype.exists = function(tag_name) {
            for(var i = 0; i < $rootScope.available_tags.length; i++) {
                if($rootScope.available_tags[i].tag == tag_name) {
                    return true;
                }
            }
            return false;
        };

        return ApiTag;
    }]);