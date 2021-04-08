#!/usr/bin/env python3

from flask import Flask, request
from micropub_utils import make_xml_tree, get_components, fake_success, get_tags, make_post
app = Flask(__name__)

"""
if you run this on a not-local server you deserve pain
"""

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/micropub', methods=['POST'])
def do_post():
    """
    this handles posting a new entry. It doesn't support all of xmlrpc. Just enough to
    let me post with MarsEdit.
    """
    post_xml = request.get_data(as_text=True)
    tree = make_xml_tree(post_xml)
    post_type = tree.getchildren()[0].text.split('.')[-1]
    if post_type == 'getPost':
        return fake_success()
    if post_type == 'deletePost':
        return fake_success()
    (post_title, bodytext) = get_components(tree)
    tags = get_tags(bodytext)
    make_post(post_title, bodytext, tags)
    return fake_success()
