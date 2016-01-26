var tagger = angular.module('helptux.tagger', []);

tagger.factory('HelptuxTagger', ['$rootScope',
    function ($rootScope) {
        var HelptuxTagger = function() {
        };

        /**
         * Add a tag of tag_type to $rootScope.post.'tag_type'. tag_type is created/modified via
         * api_inst (e.g. ApiTag)
         * @param tag_type
         * @param tag_value
         * @param api_inst
         */
        HelptuxTagger.prototype.add_tags_to_post = function(tag_type, tag_value, api_inst) {
            if(typeof(tag_value) != 'undefined') {
                /* Using onKeyPress may result in an undefined value being processed. We don't want that */
                if(!api_inst.exists(tag_value)) {
                    /* Store it in the DB if it doesn't exist */
                    api_inst.store(tag_value);
                }
                return tag_value;
            }
        };

        return HelptuxTagger;
    }]);/**
 * Created by pieter on 26/01/16.
 */
