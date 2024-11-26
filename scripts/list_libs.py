import json
import os

import scripts.plot_top10 as plot

arr = []
arr_py = []
repos = []
libs = []
projectsDict = {}

def list_save_projects_libs(dirName, projects, project_dict):
    for p in projects:
        project_path = dirName+'/'+p
        read_requirements(project_path, p)

    ext_libs,std_libs = count_libs()
    ext_desired_libs,std_desired_libs = count_desired_libs()
    projectsReturn = []
    
    ext_libs = sorted(ext_libs, key=lambda x: x["amount"], reverse=True)
    ext_desired_libs = sorted(ext_desired_libs, key=lambda x: x["amount"], reverse=True)
    std_desired_libs = sorted(std_desired_libs, key=lambda x: x["amount"], reverse=True)
    std_libs = sorted(std_libs, key=lambda x: x["amount"], reverse=True)
    globalFiles = 0 
    interestFiles = 0

    for lib in projectsDict.keys():
        globalFiles += project_dict[lib]
        if (len(projectsDict[lib]) > 0): 
            interestFiles += project_dict[lib]
            projectsReturn.append({"name":lib, "libs": projectsDict[lib], "total_of_files": project_dict[lib]})
        else: continue
        
    projectsReturn = sorted(projectsReturn, key=lambda x: x["total_of_files"], reverse=True)
    #Creating json file
    if 'my_repo' in dirName:
        with open('./returns/my_project/libs.json', 'w', encoding='utf-8') as f:
            json.dump(ext_libs, f, ensure_ascii=False, indent=4)

        with open('./returns/my_project/libs_Py.json', 'w', encoding='utf-8') as f:
            json.dump(std_libs, f, ensure_ascii=False, indent=4)
    elif 'my_example' in dirName:
        with open('./test/returns/my_project/libs.json', 'w', encoding='utf-8') as f:
            json.dump(ext_libs, f, ensure_ascii=False, indent=4)

        with open('./test/returns/my_project/libs_Py.json', 'w', encoding='utf-8') as f:
            json.dump(std_libs, f, ensure_ascii=False, indent=4)
    elif 'examples' in dirName:
        with open('./test/returns/all_projects/libs.json', 'w', encoding='utf-8') as f:
            json.dump(ext_libs, f, ensure_ascii=False, indent=4)

        with open('./test/returns/all_projects/libs_Py.json', 'w', encoding='utf-8') as f:
            json.dump(std_libs, f, ensure_ascii=False, indent=4)
    else:
        with open('./returns/all_projects/libs.json', 'w', encoding='utf-8') as f:
            json.dump(ext_libs, f, ensure_ascii=False, indent=4)

        with open('./returns/all_projects/libs_Py.json', 'w', encoding='utf-8') as f:
            json.dump(std_libs, f, ensure_ascii=False, indent=4)

    with open('./returns/all_projects/info_data.json', 'w', encoding='utf-8') as f:
            json.dump({
                "total":{
                    "global":len(projects), 
                    "interest": len(projectsReturn),
                    "global_number_of_files": globalFiles,
                    "interest_number_of_files": interestFiles
                }, 
                "count":{
                    "global": {
                        "standart_libs": std_libs,
                        "external_libs": ext_libs
                    },
                    "interest": {
                        "standart_libs": std_desired_libs,
                        "external_libs": ext_desired_libs
                    }
                }, 
                "repos": projectsReturn
            }, f, ensure_ascii=False, indent=4)
        
    with open('./returns/all_projects/interest_repos.json', 'w', encoding='utf-8') as f:
        json.dump(projectsReturn, f, ensure_ascii=False, indent=4)
    
    with open('./returns/all_projects/interest_libs.json', 'w', encoding='utf-8') as f:
            json.dump(ext_desired_libs, f, ensure_ascii=False, indent=4)

    with open('./returns/all_projects/interest_libs_Py.json', 'w', encoding='utf-8') as f:
        json.dump(std_desired_libs, f, ensure_ascii=False, indent=4)

def read_requirements(path, projectName):
    auxList = []
    for filename in os.listdir(path):
        if filename == ("requirements.txt"):
            name = path+'/'+str(filename)
            with open(name) as infile:
                for line in infile:
                    lib = line.split('==')
                    lib_name = lib[0]
                    if lib_name != '\n':
                        arr.append(lib_name)
                        auxList.append(lib_name)
        elif filename == ("packages_python.txt"):
            name = path+'/'+str(filename)
            with open(name) as infile:
                for line in infile:
                    lib = line.split('==')
                    lib_name = lib[0]
                    if lib_name != '\n':
                        lib_name = lib_name.replace('\n','')
                        arr_py.append(lib_name)
                        auxList.append(lib_name)

    libs = libs_filter("desiredLibs.txt")
    projectsDict[projectName] = [x for x in auxList if x in libs]

def count_libs():
    myDict = {}
    myDictPy = {}
    myDictReturn = []
    myDictPyReturn = []
    for lib in arr:
        if not lib:
            continue
        elif lib not in myDict.keys():
            myDict[lib] = 1
        else:
            myDict[lib] += 1
    for lib in myDict.keys():
        myDictReturn.append({
            "name": lib,
            "amount": myDict[lib]
        })

    for lib in arr_py:
        if not lib:
            continue
        elif lib not in myDictPy.keys():
            myDictPy[lib] = 1
        else:
            myDictPy[lib] += 1
    for lib in myDictPy.keys():
        myDictPyReturn.append({
            "name": lib,
            "amount": myDictPy[lib]
        })

    print(f'{"Lib":<34}' + "  Count")
    for k, v in myDict.items():
        print(f'{k:<34}' + "  " + str(v))
    print("Numero de libs = " + str(len(myDict)))
    print('\n')
    print(f'{"Lib":<34}' + "  Count")
    for k, v in myDictPy.items():
        print(f'{k:<34}' + "  " + str(v))
    print("Numero de libs python = " + str(len(myDictPy)))
    return myDictReturn,myDictPyReturn

def count_desired_libs():
    libs = libs_filter("desiredLibs.txt")
    myDict = {}
    myDictPy = {}
    myDictReturn = []
    myDictPyReturn = []
    for lib in arr:
        if not lib:
            continue
        elif lib not in libs:
            continue
        elif lib not in myDict.keys():
            myDict[lib] = 1
        else:
            myDict[lib] += 1
    for lib in myDict.keys():
        myDictReturn.append({
            "name": lib,
            "amount": myDict[lib]
        })

    for lib in arr_py:
        if not lib:
            continue
        elif lib not in libs:
            continue
        elif lib not in myDictPy.keys():
            myDictPy[lib] = 1
        else:
            myDictPy[lib] += 1
    for lib in myDictPy.keys():
        myDictPyReturn.append({
            "name": lib,
            "amount": myDictPy[lib]
        })

    print(f'{"Lib":<34}' + "  Count")
    for k, v in myDict.items():
        print(f'{k:<34}' + "  " + str(v))
    print("Numero de libs = " + str(len(myDict)))
    print('\n')
    print(f'{"Lib":<34}' + "  Count")
    for k, v in myDictPy.items():
        print(f'{k:<34}' + "  " + str(v))
    print("Numero de libs python = " + str(len(myDictPy)))
    return myDictReturn,myDictPyReturn

def libs_filter(path):
    listOfLibs = []
    with open(path, 'r') as arquivo:
            for linha in arquivo:
                listOfLibs.append(linha.strip())
    
    return listOfLibs