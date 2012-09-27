# pelican-comments

This is a plugin for [pelican](http://getpelican.com) to provide static comments.

It was inspired by a [similar plugin for
Jekyll](https://github.com/mpalmer/jekyll-static-comments).

# How It Works

When enabled, the plugin searches a comments directory in your pelican
tree. In that directory, there is one file per comment. Each comment
file has a `post_id` attribute with the slug of the post to which the
comment belongs. The article template will receive a `comments` attribute
which contains the list of comments on the post.

# Installation

Pelican-comments is not part of the default pelican distribution.

Install from github using pip:

    pip install git://github.com/bstpierre/pelican-comments#egg=pelican_comments

In your settings.py, add:

    PLUGINS = ['pelican_comments']
    COMMENTS_DIR = ['comments'] # Optional: 'comments' is the default

In your template, add:

    {% if article.comments %}
        <h2>Comments</h2>
        <ul>
          {% for comment in article.comments %}
            <li>
              <p>{{ comment.author }} said, on {{ comment.date }}:</p>
              {{ comment.content }}
            </li>
          {% endfor %}
        </ul>
    {% endif %}

In your pelican tree, create a comments directory. Add one file per
comment on your blog. Make sure that each comment file has a `post_id`
attribute to tie it to a post. You can also include the comments'
authors and date/time. For example:

    post_id: one-of-my-post-slugs
    Author: some random guy
    Date: 2012-09-27 18:44

    This is a test.

It doesn't matter what the files are named.

# Generating the Comment Files

Script for processing a comment submission form coming soon.

Script to import comments from a wordpress export file coming soon.

See also
[this php
script](https://github.com/mpalmer/jekyll-static-comments/blob/master/commentsubmit.php),
which should be relatively easy to hack into
submission. More discussion [in this blog
post](http://hezmatt.org/~mpalmer/blog/2011/07/19/static-comments-in-jekyll.html).

You'll need some kind of workflow to allow you to move comments from
email or other holding area (I plan to use the filesystem on the webhost)
to your pelican tree.
