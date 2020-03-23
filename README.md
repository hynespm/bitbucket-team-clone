## Description: This repo contains code for automatically cloning repositories from a bitbucket cloud team space.


### Author: Patrick Hynes

The repository contains code that does the following via the bitbucket API

* Iterates over the repositories within your bitbucket team space and creates a local directory for each repository within your team space
* Clones repositories from your bitbucket should a local version not exist
* Iterates through the remote branches of the repositories and checkouts the branches locally* 


### Resources
 * [Repositories API](https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories)
 
 
 
### Repository Structure

* [function.py](function.py)
* [README.md](README.md)


### How to use

 * Set the TEAMNAME variable within the [function.py](function.py)
 * Add USERNAME and PASSWORD credentials to the [function.py](function.py)
 * Choose the directory you wish to use where you store all the repositories 