var app = angular.module('helptux.admin', ['helptux.api_core', 'helptux.api_type', 'helptux.api_tag',
    'helptux.api_cat']);

app.controller('CreateCtrl', ['$scope', '$q', 'ApiCore', 'ApiType', 'ApiTag', 'ApiCat',
    function($scope, $q, ApiCore, ApiType, ApiTag, ApiCat) {

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

        /**
         *
         */
        $scope.cat_to_cats = function(input_cat) {
            if(typeof(input_cat) != 'undefined') {
                if($scope.available_cats.indexOf(input_cat) == -1) {
                    /* We have to store it, as it didn't exist */
                    a_cat.storeCat(input_cat);
                }
                $scope.post.cats.push(input_cat);
                $scope.input_cat = undefined;
            }
        };

        /**
         *
         */
        $scope.remove_cat = function(cat) {};

        /**
         *
         */
        $scope.json_api = function() {
            $scope.post.cat = JSON.stringify($scope.post.cats);
        };


        /*
        Set-up
         */
        a_type.listTypes();
        a_tag.listTags();
        a_cat.listCats();

        $scope.post = {
            title: '',
            type: '',
            content: '',
            cat: '',
            cats: [],
            tag: '',
            tags: []
        };


        $scope.post_submit = function(input_post){
            console.log(input_post);
        };

        console.log($scope.post);
    }
]);
