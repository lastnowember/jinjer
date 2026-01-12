import os
import json
import shutil
from shutil import copy2
class Site():

    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    SITE_POSTS_PATH = CURRENT_PATH + '/posts/'
    SITE_PATH = CURRENT_PATH + '/site/'
    POSTS_PATH = 'posts/'
    TEMPLATES_PATH = CURRENT_PATH + '/templates/jerryko/'
    TEMPLATE_POST = 'post.txt'
    TEMPLATE_INDEX = 'index.txt'
    TEMPLATE_POSTS = 'posts.txt'
    EXT_HTML = 'html'
    INDEX_FILE = 'index'

    style_file = 'style.css'
    script_file = 'script.js'

    # Теги блока постов в основном html-файле 
    INDEX_TAGS = {
                    'up_ul' : '<ul><li>', 
                    'down_ul' : '</ul>',
                    'up_date' : '<div class="date">',
                    'up_category' : '<li><div class="category">',
                    'down_div' : '</div></li>',
                    'up_li_posts' : '<li><h2>',
                    'down_li_posts' : '</h2></li>',
                    'up_link_a_posts' : '<a href="',
                    'down_link_a_posts' : '">',
                    'down_link_posts' : '</a>'
                }

    def createFile(self, name, extention, path, file_list):
        self.file_name = path + '/' + name + '.' + extention
        self.new_file = open(self.file_name, 'w')
        for index in file_list:
            self.new_file.write(index)
        self.new_file.close()

    def copyFile(self, src, dist):
        copy2(src, dist)

    def createFolder(self, folder_name):
        try:
            os.mkdir(folder_name)
        except FileExistsError:
            shutil.rmtree(folder_name)
            os.mkdir(folder_name)

    def checkFolder(self, path_name):
        self.folder_exist = False
        if os.path.exists(path_name):
            self.folder_exist = True
        return self.folder_exist

    def transliterate(self, name):
        # Слоаврь с заменами
        slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo',
            'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
            'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
            'ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
            'ю':'u','я':'Ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'Yo',
            'Ж':'Zh','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
            'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
            'Ц':'C','Ч':'Ch','Ш':'Sh','Щ':'Sch','Ъ':'','Ы':'y','Ь':'','Э':'E',
            'Ю':'U','Я':'Ya',',':'','?':'',' ':'-','~':'','!':'','@':'','#':'',
            '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'-','=':'','+':'',
            ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
            '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
            'Є':'e', '—':''}
                
        # Циклически заменяем все буквы в строке
        for key in slovar:
            name = name.replace(key, slovar[key])
        return name

    def getFolderList(self, path):
        self.posts = []
        with os.scandir(path) as listOfEntries:  
            for entry in listOfEntries:
            # печать всех записей, являющихся файлами
                if entry.is_file():
                    self.posts.append(entry.name)
        return self.posts
    
    def getPostData(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.post = json.load(f)
        return self.post

    def readTemplate(self, template):
        with open(template) as f:
            self.my_lines = f.readlines()
        return self.my_lines

    def getEnv(self, line):
        line = line[2:-3]
        return line

    def addPosts(self, title, date, trans_title, category):
        self.link_html = self.POSTS_PATH + trans_title + '/index.html'
        self.result = self.INDEX_TAGS['up_ul'] + self.INDEX_TAGS['up_date'] + date + self.INDEX_TAGS['down_div'] + self.INDEX_TAGS['up_li_posts'] + self.INDEX_TAGS['up_link_a_posts'] + self.link_html + self.INDEX_TAGS['down_link_a_posts'] + title + self.INDEX_TAGS['down_link_posts'] + self.INDEX_TAGS['down_li_posts'] + self.INDEX_TAGS['up_category'] + category + self.INDEX_TAGS['down_div'] + self.INDEX_TAGS['down_ul']
        return self.result

    def getPosts(self, post_json):
        self.temp_file = self.TEMPLATES_PATH + self.TEMPLATE_POSTS
        self.temp_list = self.readTemplate(self.temp_file)
        self.post = self.getPostData(self.post_json)
        self.html_list = []
        self.trans_title = self.transliterate(self.post["title"]) 
        self.link_html = self.POSTS_PATH + self.trans_title + '/index.html'
        for tpl in self.temp_list:
            if (tpl[:2] == '{{'):
                self.env = self.getEnv(tpl)
                if (self.env == 'post_link'):
                    tpl = self.link_html
                else:
                    tpl = self.post[self.env]
            self.html_list.append(tpl)
        return self.html_list
       

    def generatePosts(self): 
        self.posts = self.getFolderList(self.SITE_POSTS_PATH)
        self.posts_folder = self.SITE_PATH + self.POSTS_PATH
        self.createFolder(self.posts_folder)
        self.temp_file = self.TEMPLATES_PATH + self.TEMPLATE_POST
        self.html_list = []
        for js in self.posts:
            self.post_json = self.SITE_POSTS_PATH + js
            self.post = self.getPostData(self.post_json)
            self.title = self.transliterate(self.post["title"])
            self.post_path = self.posts_folder + self.title
            self.createFolder(self.post_path)
            self.temp_list = self.readTemplate(self.temp_file)
            for tpl in self.temp_list:
                if (tpl[:2] == '{{'):
                    self.env = self.getEnv(tpl)
                    tpl = self.post[self.env]
                self.html_list.append(tpl)
            self.createFile(self.INDEX_FILE, self.EXT_HTML, self.post_path, self.html_list)
            self.html_list = [] 
    
    # Функция генерации основного index-файла
    def generateIndex(self):
        self.style = self.TEMPLATES_PATH + self.style_file
        self.script = self.TEMPLATES_PATH + self.script_file 
        self.posts = self.getFolderList(self.SITE_POSTS_PATH)
        self.temp_file = self.TEMPLATES_PATH + self.TEMPLATE_INDEX
        self.posts_folder = self.SITE_PATH + self.POSTS_PATH
        self.temp_list = self.readTemplate(self.temp_file)  
        self.html_next = []
        self.html_posts = []
        for tpl in self.temp_list:
            if (tpl[:2] == '{{'):
                self.env = self.getEnv(tpl)
                if (self.env == 'get_posts'):
                    for js in self.posts:
                        self.post_json = self.SITE_POSTS_PATH + js
                        self.html_posts = self.getPosts(self.post_json)
                        for x in self.html_posts:
                            self.html_next.append(x)
            else:
                # Продолжаем добавлять теги
                self.html_next.append(tpl)
        
        # Создаем index.html в папке site
        self.createFile(self.INDEX_FILE, self.EXT_HTML, self.SITE_PATH, self.html_next)     

        self.copyFile(self.style, self.SITE_PATH)
        self.copyFile(self.script, self.SITE_PATH)

start = Site()

start.generateIndex()
start.generatePosts()





