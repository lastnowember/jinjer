import os
import json
import random
import constants
import hashlib
import markdown
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def checkFolder(path_name:str):

    folder_exist = False
    if os.path.exists(path_name):   
        folder_exist = True
    return folder_exist

def checkElementJson(json_file:str, json_file_path:str):

    with open(json_file_path, 'r+') as file:
        data_json = json.load(file)
    
    if len(data_json[json_file]) >= 1:
        return True
    else:
        return False
    
def setCurrentProject():
    
    with open(constants.PROJECTS_FILE, 'r+') as file:
        data_json = json.load(file)
        current_project =data_json['projects'][0]
        addElementJson('current_project', constants.CURRENT_PROJECT_FILE, current_project)

def addElementJson(json_file:str, json_file_path:str, json_data):

    with open(json_file_path, 'r+') as file:
        data_json = json.load(file)
        data_json[json_file].append(json_data)
        file.seek(0)
        json.dump(data_json, file, indent=4, ensure_ascii=False)

def getValueJson(json_file:str, json_file_path:str, element_key:str):

    with open(json_file_path, 'r+') as file:
        data_json = json.load(file)

    value = data_json[json_file][0].get(element_key)

    return value

def deleteElementJson(json_file:str, json_file_path:str, element_key:str, element_value:str):

    with open(json_file_path, 'r+') as file:
        data_json = json.load(file)
        
        data_json[json_file] = list(
            filter(
                lambda x: x.get(element_key) != element_value, 
                data_json.get(json_file, [])
            )
        )
    with open(json_file_path, 'w') as file:   
        json.dump(data_json, file, indent=4, ensure_ascii=False)

def jsonElementsList(json_file:str, json_file_path:str, heads:list):

    with open(json_file_path, 'r+') as file:
        data_json = json.load(file)

        table = PrettyTable()

        table.field_names = heads

        for dict in data_json[json_file]:
            values = []
            for key, value in dict.items():
                values.append(value)
            table.add_row(values)
        print(table)

def getCurrentProjectName():
    value = getValueJson('current_project', constants.CURRENT_PROJECT_FILE, 'project_name')
    return value

def getHashFile(file_path:str):

    path_file = Path(file_path)
    data = path_file.read_bytes()
    hash = hashlib.sha1(data).hexdigest()

    return hash

def addHash(md_file:str):

    hashes = {}
    project_path = constants.SOURCE_PATH + type + '/'

    for file in os.listdir(project_path):
        md_file = project_path + file
        name = file[:-3]
        hash = getHashFile(md_file)
        hashes[name] = hash

    print(hashes)

def getDate():
    date = datetime.now().date()
    return date

def getTheme():

    value = getValueJson('settings', constants.SETTINGS_FILE, 'theme')
    return value

def loadTemplate():

    theme_path = constants.THEMES_PATH + '/' + getTheme() + '/'
    env = Environment(loader=FileSystemLoader(theme_path))
    return env

def createData(income_data:tuple) -> dict:

    data = {}
    meta = income_data[0]
    text = income_data[1]
    
    data['title'] = meta['title'][0]
    data['url'] = meta['url'][0]
    data['description'] = meta['description'][0]
    data['keywords'] = meta['keywords'][0]
    data['text'] = text
    data['date'] = meta['date'][0]
    data['category'] = meta['category'][0]
   
    return data

def createCategoryData(category):
    pass

def sortPostsDate(posts):

    # Преобразуем словарь в список кортежей и сортируем
    sorted_items = sorted(
        posts.items(),
        key=lambda x: datetime.strptime(x[1][0]['date'], '%d-%m-%Y'),
        reverse=True  # для убывания
    )

    # Преобразуем обратно в словарь (Python 3.7+ сохраняет порядок)
    sorted_posts = dict(sorted_items)
    return sorted_posts

def createHtmlFiles(data, type:str, cat_key = ''):

    env = loadTemplate()
    blog_title = getValueJson('settings', constants.SETTINGS_FILE, 'blog_title')
    
    match type:
        case 'index':
            template = env.get_template('index.html')
            html_file = constants.BLOG_PATH + 'index.html'
            html = template.render(data=data, title_blog=blog_title, menu=generateMenu())
        case 'category':
            template = env.get_template('category.html')
            html_file = constants.BLOG_PATH + cat_key + '.html'
            html = template.render(data=data, category=cat_key, title_blog=blog_title, menu=generateMenu())
        case 'article':
            template = env.get_template('article.html')
            html_file = constants.BLOG_PATH + data['url'] + '.html'
            html = template.render(data, title_blog=blog_title, menu=generateMenu())
        case _:
            print('Error, no type of File')
        
    
    with open(html_file, 'w') as file:
        file.write(html)
        

def getMarkdown(markdown_file:str):

    md_file_path = constants.POSTS_PATH + markdown_file
    with open(md_file_path, 'r') as md_file:
        md_text = md_file.read()

    md = markdown.Markdown(extensions=['meta', 'md_in_html'])
    md_html = md.convert(md_text)
    meta = md.Meta

    return meta, md_html

def generateMenu():
    with open(constants.MENU_FILE, 'r+') as file:
        data_json = json.load(file)

    return data_json

def copyImages(post_name):
    post_images_path = constants.POSTS_IMAGES + post_name
    blog_images_path = constants.BLOG_IMAGES + post_name
    

    if os.path.exists(post_images_path):

        post_images = os.listdir(post_images_path)

        if not os.path.exists(blog_images_path):
            os.makedirs(blog_images_path)
        
        blog_images = os.listdir(blog_images_path)

        for file in post_images:
            if file in blog_images:
                continue
            else:
                file_posts = post_images_path + '/' + file
                file_blog = blog_images_path + '/' + file
                shutil.copy(file_posts, file_blog)
    else:
        error_folder_image = 'Images folder article - ' + post_name + ' - not exists' 
        print(error_folder_image)
            

# Copy source files from theme folder in blog folder

def copySource():
    theme_path = constants.THEMES_PATH + '/' + getTheme() + '/'
    source_folder = 'source/'
    theme_source = theme_path + source_folder
    blog_source = constants.BLOG_PATH + source_folder

    if os.path.exists(blog_source):
        shutil.rmtree(blog_source)

    shutil.copytree(theme_source, blog_source)

def generateBlog():
    types = ['posts']

    index_data = {}
    category_data = {}
    category_list = {}
    

    for type in types:
        type_path = constants.SOURCE_PATH + type + '/'
        files = os.listdir(type_path)
        for file in files:
            file_path = constants.POSTS_PATH + file
            if os.path.isdir(file_path):
                continue
            create_data = createData(getMarkdown(file))

             # copy images
            copyImages(create_data['url'])

            urls = './' + create_data['url'] + '.html'
            try:
                category_data[create_data['category']].append({'title': create_data['title'], 'url': urls, 'date': create_data['date']})
            except KeyError:
                category_data[create_data['category']] = []
                category_data[create_data['category']].append({'title': create_data['title'], 'url': urls, 'date': create_data['date']})

            index_data[create_data['title']] = [{'url': urls, 'date': create_data['date'], 'category':create_data['category'], 'description':create_data['description']}]
            createHtmlFiles(create_data, 'article')

    # generate category pages
    cat_list = list(category_data.keys())
    for key in cat_list:
        for item in category_data[key]:
            category_list[item['title']] = [{'url': item['url'], 'date': item['date']}]
        createHtmlFiles(category_list, 'category', cat_key=key)
        category_list = {}

    # copy source/ folder
    copySource()

    # sort posts py date
    index_posts = sortPostsDate(index_data)
    
    # generate index.html
    createHtmlFiles(index_posts, 'index')







def createId() -> str:

    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['1','2','3','4','5','6','7','8','9']
    id = ''
    sym = ''
    n = 1
    while (n <= 6):
        if n % 2 == 0:
            sym = random.choice(alpha)
        else:
            sym = random.choice(numbers)
        id += sym
        n = n + 1
    return id


# Test defs
def projectsUp():
    data = {"projects":[]}
    with open(constants.PROJECTS_FILE, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


#lenArgs('1','2','3')
#lenJson()
#HEADS = ['ID', 'NAME']
#jsonElementsList('projects', constants.PROJECTS_FILE, HEADS)
#print('project_name = ' + getValueJson('current_project', constants.CURRENT_PROJECT_FILE, 'project_name'))
#setCurrentProject()
#print(getMarkdown('mark.md')[0])
#createPostHtml(createData(getMarkdown('mark.md')))
generateMenu()
