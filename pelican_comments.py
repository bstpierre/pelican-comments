# -*- coding: utf-8 -*-
# Copyright (c) 2012, Brian St. Pierre

"""
Static comments plugin for Pelican
================================

Adds comments variable to article's context

Settings
--------

To enable, add:

    from pelican_comments import comments
    PLUGINS = [comments]

to your settings.py.

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


class Comment(object):
    def __init__(self, content, metadata):
        self.content = content

        properties = [
            'author',
            'date',
            ]

        for property in properties:
            setattr(self, property, metadata.get(property, ''))

    def __cmp__(self, other):
        """
        Comment comparison is by date. This is so that a comment list
        can easily be sorted by date.
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

        comments_dir = generator.settings.get('COMMENTS_DIR', 'comments')
        comment_filenames = generator.get_files(comments_dir)
        for comment_filename in comment_filenames:
            content, metadata = readers.read_file(comment_filename)
            if 'post_id' not in metadata:
                raise Exception("comment %s does not have a post_id" % (
                    comment_filename, ))

            comment = Comment(content, metadata)
            self._comments[metadata['post_id']].append(comment)

        for slug, comments in self._comments.items():
            comments.sort()
            

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
    signals.article_generate_context.connect(add_comments)
