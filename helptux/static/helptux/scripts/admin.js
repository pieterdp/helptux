var app = angular.module('helptux', ['helptux.api_core']);

app.controller('CreateCtrl', ['$scope', '$q', 'ApiCore',
    function($scope, $q, ApiCore) {

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
    }
]);
