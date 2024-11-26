from collections import Counter
import matplotlib.pyplot as plt
import json

def plot_info_data():
    # Defining the colors that going to be used 
    colors = [
        'darkred', 'firebrick', 'indianred', 'tomato', 'coral',
        'salmon', 'darksalmon', 'lightsalmon', 'sandybrown', 'peachpuff'
    ]

    # Reading the data source
    with open('returns/all_projects/info_data.json', 'r') as file:
        info_data = json.load(file)

    with open('returns/all_projects/libs.json', 'r') as file:
        ext_libs = json.load(file)
    
    with open('returns/all_projects/libs_Py.json', 'r') as file:
        std_libs = json.load(file)

    with open('returns/all_projects/interest_libs.json', 'r') as file:
        interest_ext_libs = json.load(file)
    
    with open('returns/all_projects/interest_repos.json', 'r') as file:
        repos = json.load(file)

    total = info_data["total"]

    global_repos = total["global"]
    interest_repos = total["interest"]
    global_files = total["global_number_of_files"]
    interest_files = total["interest_number_of_files"]

    total_ext = len(ext_libs)
    total_std = len(std_libs)
    
    # Pizza - Total de Libs
    fig, ax = plt.subplots(layout='constrained')
    ax.pie([total_std, total_ext], explode= [0, 0.25], labels=["Padrão", "Externas"], autopct='%1.1f%%', colors=['indianred', 'firebrick'], shadow=True, startangle=90)
    ax.set_label("Total: " + str(total_ext + total_std))
    ax.set_title("Relação de Bibliotecas Externas x Padrões")
    fig.savefig(f'./returns/images/std_x_ext.png', bbox_inches='tight')

    # Pizza - Total de Repositórios
    fig, ax = plt.subplots(layout='constrained')
    ax.pie([global_repos, interest_repos], explode= [0, 0.25], labels=["Analisados", "Interesse"], autopct='%1.1f%%', colors=['indianred', 'firebrick'], shadow=True, startangle=90)
    ax.set_label("Total: " + str(total_ext + total_std))
    ax.set_title("Relação de Repositórios Analisados x Interesse")
    fig.savefig(f'./returns/images/repos_global_x_interest.png', bbox_inches='tight')

    # Pizza - Total de Arquivos
    fig, ax = plt.subplots(layout='constrained')
    ax.pie([global_files, interest_files], explode= [0, 0.25], labels=["Analisados", "Interesse"], autopct='%1.1f%%', colors=['indianred', 'firebrick'], shadow=True, startangle=90)
    ax.set_label("Total: " + str(total_ext + total_std))
    ax.set_title("Relação de Arquivos Analisados x Interesse")
    fig.savefig(f'./returns/images/files_global_x_interest.png', bbox_inches='tight')
    
    # Barras - Bibliotecas Padrão Geral
    fig, ax = plt.subplots(layout='constrained')
    topTen_names = []
    topTen_amounts = []
    for x in std_libs[0:10]:
        topTen_names.append(x["name"])
        topTen_amounts.append(x["amount"])

    ax.bar(topTen_names, topTen_amounts, color=colors)
    ax.set_title("Bibliotecas Padrão")
    ax.set_ylabel("Quantidade de Repositórios")
    ax.set_xlabel("Bibliotecas")
    
    for i in range(len(topTen_amounts)):
        plt.text(i, topTen_amounts[i]+1, str(topTen_amounts[i]), ha='center')

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    fig.savefig(f'./returns/images/standart_libs.png', bbox_inches='tight')

    # Barras - Bibliotecas Externas Geral
    fig, ax = plt.subplots(layout='constrained')
    topTen_names = []
    topTen_amounts = []
    for x in ext_libs[0:10]:
        topTen_names.append(x["name"])
        topTen_amounts.append(x["amount"])

    ax.bar(topTen_names, topTen_amounts, color=colors)
    ax.set_title("Bibliotecas Externas")
    ax.set_ylabel("Quantidade de Repositórios")
    ax.set_xlabel("Bibliotecas")

    for i in range(len(topTen_amounts)):
        plt.text(i, topTen_amounts[i] + 1, str(topTen_amounts[i]), ha='center')

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    fig.savefig(f'./returns/images/external_libs.png', bbox_inches='tight')

    # Barras - Bibliotecas Externas de Interesse
    fig, ax = plt.subplots(layout='constrained')
    topTen_names = []
    topTen_amounts = []
    for x in interest_ext_libs[0:10]:
        topTen_names.append(x["name"])
        topTen_amounts.append(x["amount"])

    ax.bar(topTen_names, topTen_amounts, color=colors)
    # ax.set_title("Bibliotecas Externas de Interesse")
    ax.set_ylabel("Quantidade de Repositórios")
    ax.set_xlabel("Bibliotecas")

    for i in range(len(topTen_amounts)):
        plt.text(i, topTen_amounts[i] + 1 , str(topTen_amounts[i]), ha='center')

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    fig.savefig(f'./returns/images/interest_libs.png', bbox_inches='tight')


    # Pizza - Categorias
    
    # Extrair categorias e contar
    categories = [repo['category'] for repo in repos]
    category_count = Counter(categories)

    # Converter o resultado para o formato solicitado
    category_list = [{"name": category, "amount": count} for category, count in category_count.items()]
    category_list = sorted(category_list, key=lambda x: x["amount"], reverse=True)

    fig, ax = plt.subplots(layout='constrained')
    ax.pie([category["amount"] for category in category_list],  labels=[category["name"] for category in category_list], autopct='%1.1f%%')
    ax.set_label("Total: " + str(total_ext + total_std))
    ax.set_title("Relação de Categorias")
    fig.savefig(f'./returns/images/categories.png', bbox_inches='tight')


