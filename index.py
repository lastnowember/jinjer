import sys
import functions

def getCommand(command: list):
    match command[1]:
        case 'generate':
            functions.generateBlog()
        case _:
            return "no command"

getCommand(sys.argv)


