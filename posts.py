import markdown

import constants
import functions

def getPostsPath():
    posts_path = constants.SOURCE_PATH + 'posts/'
    return posts_path

def getMarkdown():
    md_file_path = getPostsPath() + 'first.md'
    with open(md_file_path, 'r') as md_file:
        md_text = md_file.read()

    md = markdown.Markdown(extensions=['meta'])
    md_html = md.convert(md_text)

    