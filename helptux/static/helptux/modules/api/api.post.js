var api_post = angular.module('helptux.api_post', ['helptux.api_core']);

api_post.factory('ApiPost', ['$rootScope', 'ApiCore',
    function ($rootScope, ApiCore) {
        var ApiPost = function() {
            this.a_api = new ApiCore();
        };

        ApiPost.prototype.show = function(post_id) {
            return this.a_api.read(post_id, 'post');
        };

        ApiPost.prototype.list = function() {
            this.a_api.list('post').then(function success(api_data) {
                $rootScope.available_posts = api_data.data.data;
            });
        };

        /**
         * Store - returns a $promise
         * @param input_data
         * @return:
         */
        ApiPost.prototype.store = function(input_data) {
            /*tag = {tag: tag} etc.*/
            var submit_post = {
                title: input_data.title,
                content: input_data.content,
                type_id: input_data.type.id,
                creation_time: input_data.creation_time
            };
            /* Parse tags */
            var submit_tags = [];
            for(var i = 0; i < input_data.tags.length; i++) {
                submit_tags.push({tag: input_data.tags[i]});
            }
            submit_post.tags = submit_tags;

            /* Parse categories */
            var submit_cats = [];
            for(i = 0; i < input_data.cats.length; i++) {
                submit_cats.push({category: input_data.cats[i]});
            }
            submit_post.categories = submit_cats;

            var api_promise;
            if (input_data.id < 0) {
                /* The ID of a new post is always negative, e.g. -1; if we're editing a post, we get the correct id
                Attempting to edit a post with a negative id will result in errors */
                api_promise = this.a_api.create(submit_post, 'post');
            } else {
                /* Edit */
                api_promise = this.a_api.update(input_data.id, submit_post, 'post');
            }

            return api_promise;
        };

        /**
         * Prepare raw API response for display. The data is in data.data. Mostly parsing cats, tags and types.
         * @param api_data
         */
        ApiPost.prototype.prepare_for_display = function(api_data) {
            var api_post = angular.copy(api_data.data.data);
            var view_post = {
                id: api_post.id,
                title: api_post.title,
                content: api_post.content,
                tags: [],
                cats: []
            };

            /* Parse type */
            for(var i = 0; i < $rootScope.available_types.length; i++) {
                var av_type = $rootScope.available_types[i];
                if(av_type.id == api_post.type_id) {
                    view_post.type = av_type;
                    break;
                }
            }

            /* Parse tags */
            for(i = 0; i < api_post.tags.length; i++) {
                view_post.tags.push(api_post.tags[i].tag);
            }

            /* Parse categories */
            for(i = 0; i < api_post.categories.length; i++) {
                view_post.cats.push(api_post.categories[i].category);
            }

            return view_post;
        };

        return ApiPost;
    }]);
