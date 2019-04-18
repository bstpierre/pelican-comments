# -*- coding: utf-8 -*-
# Copyright (c) 2012, Brian St. Pierre

"""
Static comments plugin for Pelican
================================

Adds comments variable to article's context. Comments by default should be
in a comments subdirectory of your content directory.

Settings
--------

To enable, add:

    PLUGINS = ['pelican_comments']

to your pelicanconf.py. If you get warnings about slugs, also add the
following to prevent pelican trying to treat comment files as articles:

    ARTICLE_EXCLUDES = ['comments', 'pages']

Usage
-----
    {% if article.comments %}
        <h2>Comments</h2>
        <ul>
        {% for comment in article.comments %}
            <li>{{ comment.author }} said: {{ comment.content }}</li>
        {% endfor %}
        </ul>
    {% endif %}


"""

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of version 3 of the GNU Affero General Public
#    License as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#    See the file LICENSE.



import collections

import pelican.signals as signals
import pelican.generators as generators
import pelican.readers as readers

from pelican.contents import Content

class Comment(Content):
    mandatory_properties = ('post_id', 'author')
    default_template = 'comment' # this is required, but not used
    default_status = 'published'

    def __cmp__(self, other):
        """
        Comment comparison is by date. This is so that a comment list
        can easily be sorted by date. The date attribute will be
        automatically set from metadata by Content base class
        """
        if self.date == other.date:
            return 0
        elif self.date < other.date:
            return -1
        else:
            return 1


class CommentReader(object):
    def __init__(self, generator):
        self._comments = collections.defaultdict(list)
        reader = readers.Readers(settings=generator.settings)

        comments_dir = generator.settings.get('COMMENTS_DIR', 'comments')
        comment_filenames = generator.get_files(comments_dir)

        for comment_filename in comment_filenames:
            comment = reader.read_file(
                base_path=generator.settings['PATH'],
                path=comment_filename,
                content_class=Comment,
                context=generator.context)

            if 'post_id' not in comment.metadata:
                raise Exception("comment %s does not have a post_id" % (
                    comment_filename, ))
            self._comments[comment.metadata['post_id']].append(comment)

        for slug, comments in self._comments.items():
            comments.sort()
            for n, comment in enumerate(comments):
                comment.cid = n

    def get_comments(self, slug):
        return self._comments[slug]


def comment_initialization(generator):
    """
    Set up the comment plugin.
    """
    generator.plugin_instance = CommentReader(generator)


def add_comments(generator, metadata):
    metadata["comments"] = generator.plugin_instance.get_comments(
        metadata['slug'])


def register():
    signals.article_generator_init.connect(comment_initialization)
    signals.article_generator_context.connect(add_comments)
