#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os
import git

api_url = 'https://bitbucket.org/api/2.0'
headers = {'Content-Type': 'application/json'}
repo_clone_urls = []
# Variables to be set
team_name = '<TEAMNAME>'
os_path = '<DIRECTORY_FOR_REPOSITORIES'
username = '<USERNAME>'
password = '<PASSWORD>'


def request_url_generator(arguments, url):
    for argument in arguments:
        url = url + '/' + argument

    return url


# Function to make calls to bitbucket
def bitbucket_requester(url, auth, headers):
    r = requests.get(url, auth=auth, headers=headers).json()
    return r


# function to make post calls to bitbucket
def bitbucket_poster(url, auth, headers, data):
    r = requests.post(url, data=data)
    return r


# Function to get the repos and clone them locally
def get_repos():
    path = ['repositories/' + team_name]
    url = request_url_generator(path, api_url)
    repos = bitbucket_requester(url, (username, password), headers)
    index = int(repos['size'])
    remainder = index % repos['pagelen']
    number_of_pages = (index - remainder) / repos['pagelen']
    for i in range(1, int(number_of_pages) + 2):
        path = ['repositories/' + team_name + '?page=' + str(i)]
        url = request_url_generator(path, api_url)
        repos = bitbucket_requester(url, (username, password), headers)

        repositories = repos['values']
        for repo in repositories:
            clone_urls = repo['links']['clone']
            for url in clone_urls:
                if url['name'] == "https":
                    entry = {"name": repo['name'], "href": url['href']}
                    repo_clone_urls.append(entry)

        with open('repos.json', 'w') as outfile:
            json.dump(repo_clone_urls, outfile)

    return repo_clone_urls


# Function to pull from the remote
def pull_from_remote(temp_path):
    # Change to the directory
    os.chdir(temp_path)
    os.system("git pull")
    os.system("git branch -a >> branches.json")  # Cloning all remote branches
    text_file = open("branches.json", "r")
    lines = text_file.readlines()

    index = 1
    for line in lines:
        if index != 1:
            remote = str(line)
            remote_list = remote.split("/")
            branch = remote_list[-1]
            if branch.strip() != "master":
                os.system("git pull")
        index = index + 1


# Function to clone the repos
def clone_repos(repos):
    try:
        # Clone repos and pull remote branches
        for repo in repos:
            temp_path = os_path + "\\" + repo['name']
            isdir = os.path.isdir(temp_path)
            # Check if the directory exists - if it doesnt - clone it
            if not isdir:
                print("Cloning Repo:" + repo['name'])
                git.Git(os_path).clone(repo['href'])
                checkout_branches(temp_path)
            # Check for updates
            pull_from_remote(temp_path)
            break


    except OSError:
        print("Creation of the directory %s failed" % temp_path)
    else:
        print("Successfully created the directory %s " % temp_path)


# Function to checkout branches locally
def checkout_branches(temp_path):
    # Change to the directory
    os.chdir(temp_path)
    os.system("git branch -a >> branches.json")  # Cloning all remote branches
    text_file = open("branches.json", "r")
    lines = text_file.readlines()

    index = 1
    for line in lines:
        if index != 1:
            remote = str(line)
            remote_list = remote.split("/")
            branch = remote_list[-1]
            if branch.strip() != "master":
                os.system("git checkout -b " + str(branch.strip()) + " --track " + line)
        index = index + 1
    os.system("git checkout master")


def main():
    repos = get_repos()
    clone_repos(repos)


if __name__ == '__main__':
    main()