var app = angular.module('helptux.admin', ['helptux.api_core', 'helptux.api_type', 'helptux.api_tag',
    'helptux.api_cat', 'helptux.api_post', 'helptux.tagger']);

app.controller('CreateCtrl', ['$scope', '$q', 'ApiCore', 'ApiType', 'ApiTag', 'ApiCat', 'ApiPost', 'HelptuxTagger',
    function($scope, $q, ApiCore, ApiType, ApiTag, ApiCat, ApiPost, HelptuxTagger) {

        /**
         * Reset all errors or one ($scope.errors.action) to their default values
         * @param action optional action parameter (attribute of $scope.errors)
         * @param item_id
         */
        $scope.reset_errors = function(action, item_id) {
            if (action == null) {
                $scope.errors = {
                    post_submit: {},
                    post_remove: {},
                    post_new: {}
                };
            } else {
                $scope.errors[action][item_id] = false;
            }
        };

        /**
         * Reset all success or one ($scope.success.action) to their default values
         * @param action optional action parameter (attribute of $scope.success)
         * @param item_id
         */
        $scope.reset_success = function(action, item_id) {
            if (action == null) {
                $scope.success = {
                    post_submit: {},
                    post_remove: {},
                    post_new: {}
                };
            } else {
                $scope.success[action][item_id] = false;
            }
        };

        /**
         * Reset the submit button for a form (via ng-change)
         * @param action
         * @param item_id
         */
        $scope.reset_submit_button = function(action, item_id) {
            $scope.reset_success(action, item_id);
            $scope.reset_errors(action, item_id);
        };

        /*
        Reset all errors & success
         */
        $scope.reset_errors();
        $scope.reset_success();

        $scope.new_post_id = -1;

        var promises = [];
        /*
        Get all tags
         */
        var a_core = new ApiCore();
        var a_type = new ApiType();
        var a_tag = new ApiTag();
        var a_cat = new ApiCat();
        var a_post = new ApiPost();
        var h_tag = new HelptuxTagger();

        /**
         *
         */
        $scope.cat_to_cats = function(input_cat_name) {
            $scope.post.cats.push(h_tag.add_tags_to_post('cats', input_cat_name, a_cat));
            $scope.input_cat = undefined;
        };

        $scope.tag_to_tags = function(input_tag_name) {
            $scope.post.tags.push(h_tag.add_tags_to_post('tags', input_tag_name, a_tag));
            $scope.input_tag = undefined;
        };

        /**
         *
         */
        $scope.remove_cat = function(input_cat_name) {
            var cat_in_list = $scope.post.cats.indexOf(input_cat_name);
            if(cat_in_list != -1) {
                $scope.post.cats.splice(cat_in_list, 1);
            }
        };

        /**
         *
         * @param input_tag_name
         */
       $scope.remove_tag = function(input_tag_name) {
            var tag_in_list = $scope.post.tags.indexOf(input_tag_name);
            if(tag_in_list != -1) {
                $scope.post.tags.splice(tag_in_list, 1);
            }
        };

        /*
        Set-up
         */
        a_type.list();
        a_tag.list();
        a_cat.list();

        $scope.post = {
            id: $scope.new_post_id,
            title: '',
            type: '',
            content: '',
            cats: [],
            tags: []
        };


        $scope.post_submit = function(input_post){
            console.log(input_post);
            a_post.store(input_post).then(function success(response){
                $scope.post = a_post.prepare_for_display(response);
                $scope.success.post_submit[input_post.id] = true;
                console.log(response);
            }, function error(response) {
                console.log(response);
                $scope.errors.post_submit[input_post.id] = response.data.msg;
            });
        };
    }
]);
