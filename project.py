import os
import constants
import errors
import functions
import shutil

# Создаем проект
def createProject(project_name):
    
    project_id = functions.createId()
    data = {"project_id":project_id,"project_name":project_name}
    project_folder = constants.PROJECT_PATH + project_name
    check_current_project = functions.checkElementJson('projects', constants.PROJECTS_FILE)
    functions.addElementJson('projects', constants.PROJECTS_FILE, data)

    if check_current_project == False:
        functions.setCurrentProject()

    if not functions.checkFolder(project_folder):
        os.mkdir(project_folder)
        shutil.copytree(constants.SOURCE_PATH, project_folder, dirs_exist_ok=True)
    else:
        print(errors.folder_exists)
    

def deleteProject(project_name):
    
    project_folder = constants.PROJECT_PATH + project_name
    functions.deleteElementJson('projects', constants.PROJECTS_FILE, 'project_name', project_name)
    if functions.checkFolder(project_folder):
        shutil.rmtree(project_folder)
    else:
        print(errors.folder_not_exists)

def projectsList():
    functions.jsonElementsList('projects', constants.PROJECTS_FILE, ['id', 'name'])

def getCurrentProjec():
    functions.jsonElementsList('current_project', constants.CURRENT_PROJECT_FILE, ['id', 'name'])



