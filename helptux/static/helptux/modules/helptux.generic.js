var generic = angular.module('helptux.generic', ['helptux.api_core', 'helptux.api_type', 'helptux.api_tag',
    'helptux.api_cat', 'helptux.api_post', 'helptux.tagger']);

generic.factory('HelptuxGeneric', ['$rootScope', 'ApiCore', 'ApiType', 'ApiTag', 'ApiCat', 'ApiPost', 'HelptuxTagger',
    function ($rootScope, ApiCore, ApiType, ApiTag, ApiCat, ApiPost, HelptuxTagger) {
        var HelptuxGeneric = function() {
            this.a_type = new ApiType();
            this.a_tag = new ApiTag();
            this.a_cat = new ApiCat();
            this.a_post = new ApiPost();
            this.h_tag = new HelptuxTagger();
        };


        HelptuxGeneric.prototype.reset_errors = function(action, item_id) {
            if (action == null) {
                $rootScope.errors = {
                    post_submit: {},
                    post_remove: {},
                    post_new: {}
                };
            } else {
                $rootScope.errors[action][item_id] = false;
            }
        };

        HelptuxGeneric.prototype.reset_success = function(action, item_id) {
            if (action == null) {
                $rootScope.success = {
                    post_submit: {},
                    post_remove: {},
                    post_new: {}
                };
            } else {
                $rootScope.success[action][item_id] = false;
            }
        };


        return HelptuxGeneric;
    }]);