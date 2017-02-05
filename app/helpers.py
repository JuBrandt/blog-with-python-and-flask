import re

from config import SNIPPET_LENGTH


def make_snippet(text):
    # Makes a snippet of text / features for use on the index page

    lines = text[:SNIPPET_LENGTH].split('\n')
    can_have_image = True
    snippet = []

    for line in lines:
        # Check for 0 length and add newline if found -- for Markdown
        if len(line) > 0:
            # If line starts with '!' most likely an image
            if line[0] == '!':
                # Restrict the amount of images on the index page
                if can_have_image:
                    snippet.append(line)
                    can_have_image = False
            else:
                snippet.append(line)
        else:
            snippet.append('\n')

    # Remove broken html

    if snippet[-1].count('>') % 2 != 0:
        del snippet[-1]

    snippet = '\n'.join(snippet)

    # Decide whether to add '...' if incomplete sentence

    if snippet[-1] != '.':
        snippet += '...'

    return snippet


def make_address(title):
    pattern = re.compile('[a-z0-9A-Z]+')
    address = ' '.join(re.findall(pattern, title)).replace(' ', '-').lower()
    return address
