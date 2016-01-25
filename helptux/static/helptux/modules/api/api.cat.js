var api_cat = angular.module('helptux.api_cat', ['helptux.api_core']);

api_cat.factory('ApiCat', ['$rootScope', 'ApiCore',
    function ($rootScope, ApiCore) {
        var ApiCat = function() {
            this.a_api = new ApiCore();
        };

        ApiCat.prototype.listCats = function() {
            this.a_api.list('category').then(function success(api_data) {
                var available_cats = api_data.data.data;
                $rootScope.available_cats = [];
                for(var i = 0; i < available_cats.length; i++) {
                    var cat = available_cats[i];
                    $rootScope.available_cats.push(cat.category);
                }
            });
        };

        ApiCat.prototype.storeCat = function(cat_name) {
            var cat = {
                category: cat_name
            };
            var self = this;
            this.a_api.create(cat, 'category').then(function success(){
                self.listCats();
            }, function error(data){
                console.log(data);
            });
        };

        return ApiCat;
    }]);