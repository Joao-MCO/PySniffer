import json
import os
import sys

import click
import scripts.get_all_paths as paths
from scripts.plot_data import plot_info_data
import scripts.plot_top10 as plot
from logs import log
from scripts import list_libs
from scripts.analyzing_my_repo import analyzing_libraries


@click.group()
@click.version_option()
def pysniffer():
    """
    ###########      PySniffer      ###########
    """

@pysniffer.command("download_repos")
def download_git_repos():
    """Download GitHub projects"""
    download = "sh download_repos.sh"
    os.system(download)


@pysniffer.command("analyzing_repos")
def analyzing_git_repos(dir = './downloaded_repos/all_repos'):
    """Generate projects statistics"""    

    print("##################################################################")
    print("              PySniffer - Generate Projects Statistics            ")
    print("##################################################################")

    #Counting files and getting projects list
    projects_dict = paths.get_projects(dir)
    projects = projects_dict.keys()
    #verificar se a pasta nao está vazia e se estiver fazer os downloads
    #Using pipreqs
    for p in projects:
        path = dir + '/' + p
        os.system(f'python pipreqs/pipreqs.py {path} --force')

    #Reading requirements file, generating list and save in a Json
    list_libs.list_save_projects_libs(dir, projects, projects_dict)

    print('Returns were generated in returns/all_projects')


@pysniffer.command("analyzing_my_project")
@click.option('--link',
              type=click.STRING,
              help="What is your project's github link?")
def analyzing_my_project(link:str):
    """Generate statistics for my project"""
    dir = './downloaded_repos/my_repo'
    print("##################################################################")
    print("              PySniffer - Generate My Project Statistics          ")
    print("##################################################################")

    print("\n1) COLLECTING DATA AND GENERATE RESULTS:")
    #download repo
    download = f"git -C {dir} clone {link} "
    os.system(download)
    #Counting files and getting projects list
    projects_dict = paths.get_projects(dir)
    projects = projects_dict.keys()

    #Using pipreqs
    for p in projects:
        path = dir + '/' + p
        os.system(f'python pipreqs/pipreqs.py {path} --force')

    #Reading requirements file, generating list and save in a Json
    list_libs.list_save_projects_libs(dir, projects)

    print('\nReturns were generated in returns/my_project')

    #Analyze if the project libraries are among the most used
    print("\n2) ANALYZING MY PROJECT")
    analyzing_libraries()

@pysniffer.command("plot_results")
def plot_results():
    """Plot projects statistics"""    

    print("##################################################################")
    print("              PySniffer - Generate Projects Statistics            ")
    print("##################################################################")

    # Ploting the data from info_data.json
    plot_info_data()


if __name__ == "__main__":
    pysniffer()
