import sys

def append_path(pathToCommon):  
    pythonApplicationLibrariesPath = '../'+pathToCommon[0:len(pathToCommon)-7]+'Python_Application_Libraries/'
    sys.path.append(pythonApplicationLibrariesPath+'application_modules/')
    sys.path.append(pythonApplicationLibrariesPath+'quanser_products/')
    sys.path.append(pythonApplicationLibrariesPath+'utilities/')