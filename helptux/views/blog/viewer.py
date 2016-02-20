import markdown
from flask import Markup


class ViewPost:

    def post_to_html(self, post_content):
        """
        Convert the post that is stored in MD to html
        :param post_content:
        :return:
        """
        return markdown.markdown(post_content, output_format='html5')

    def post_to_output_obj(self, post):
        """
        Convert a post from the way it is stored in the DB to something our template will accept
        :param post:
        :return:
        """
        # Completely ununderstandable bug
        print(post)
        return {
            'title': post.title,
            'slug': post.slug,
            'formatted_date': post.last_modified.strftime('%d-%m-%Y'),
            'author': post.author.username,
            'formatted_content': Markup(self.post_to_html(post.content)),
            'formatted_abstract': Markup(self.post_to_output_obj(post.abstract)),
            'tags': post.tags
        }
