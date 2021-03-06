import json
import time
from datetime import datetime
from pymongo import MongoClient
from mongo import Mongo

import requests
from csv2json import convert, load_csv, save_json

endCursor = ""
hasNextPage = False

cursorCount = 0

client = MongoClient()


def getPRNextQuery(endcursor, name, owner):
    prNextQuery = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 5, after: "%s") {
          totalCount
          nodes {
            id
            createdAt
            closed
            closedAt
            merged
            mergedAt
            bodyText
            changedFiles
            files {
              totalCount
            }
            participants {
              totalCount
            }
            comments {
              totalCount
            }
            reviews {
              totalCount
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    """ % (owner, name, endcursor)

    return prNextQuery


def getPullRequests(name, owner):
    tokens = ["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",
              "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",
              "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"]

    global token
    global cursorCount
    token = tokens[cursorCount % 3]
    print('Token é ', token)

    url = 'https://api.github.com/graphql'
    headers = {"Authorization": "Bearer " + token}

    prFirstQuery = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 5) {
          totalCount
          nodes {
            id
            createdAt
            closed
            closedAt
            merged
            mergedAt
            bodyText
            changedFiles
            files {
              totalCount
            }
            participants {
              totalCount
            }
            comments {
              totalCount
            }
            reviews {
              totalCount
            }
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    """ % (owner, name)

    request = requests.post(url, json={'query': prFirstQuery}, headers=headers)

    if request.status_code == 200:
        doOperations(request.json(), name)
        while hasNextPage:
            request = requests.post(url, json={'query': getPRNextQuery(endCursor, name, owner)}, headers=headers)
            doOperations(request.json(), name)
    elif request.status_code == 502:
        cursorCount += 1
        token = tokens[cursorCount % 3]
        time.sleep(3)
        print('Trocando token: ', token)
        getPullRequests(name, owner)
    elif request.content is None or request.status_code == 204:
        print('Request vazia\nTentando novamente...')
        getPullRequests(name, owner)


def doOperations(response, name):
    checkIfHasNext(response, name)
    filterPullRequest(response, name)


def checkIfHasNext(request, name):
    global hasNextPage
    hasNextPage = request['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
    print('hasNextPage = ', hasNextPage)

    if hasNextPage != True:
        Mongo().insert_repository(name)

    global endCursor
    endCursor = request['data']['repository']['pullRequests']['pageInfo']['endCursor']
    print('O endcursor é: ', endCursor)

def filterPullRequest(request, name):
    print('Filtrando Pull Requests...')
    jsonTotalCount = len(request['data']['repository']['pullRequests']['nodes'])

    if jsonTotalCount > 0:
        for i in range(jsonTotalCount):
            pullRequest = request['data']['repository']['pullRequests']['nodes'][i]

            closed = pullRequest["reviews"]['totalCount']
            merged = pullRequest["reviews"]['totalCount']
            reviews = pullRequest["reviews"]['totalCount']
            mergedAt = pullRequest["mergedAt"]
            closedAt = pullRequest["closedAt"]
            createdAt = pullRequest["createdAt"]

            def format(pr):
                return {
                    "name": name,
                    "createdAt": pr["createdAt"],
                    "closed": pr["closed"],
                    "closedAt": pr["closedAt"],
                    "merged": pr["merged"],
                    "mergedAt": pr["mergedAt"],
                    "bodyText": pr["bodyText"],
                    "changedFiles": pr["changedFiles"],
                    "files": pr["files"]["totalCount"],
                    "participants": pr["participants"]["totalCount"],
                    "comments": pr["comments"]["totalCount"],
                    "reviews": pr["reviews"]["totalCount"],
                }

            if (closed or merged) and reviews >= 1:
                if (closed and merged) or (closed and not merged):
                    timeSpent = calculateCloseMergeTime(createdAt, closedAt)
                else:
                    timeSpent = calculateCloseMergeTime(createdAt, mergedAt)

                if timeSpent is not None:
                    prFormatted = format(pullRequest)
                    Mongo().insert_one(prFormatted)
                    print(prFormatted)


def calculateCloseMergeTime(createdAt, closedMergedAt):
    if (closedMergedAt is not None) and (createdAt is not None):
        createdTime = datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ")
        finishedTime = datetime.strptime(closedMergedAt, "%Y-%m-%dT%H:%M:%SZ")

        timeInSeconds = (finishedTime - createdTime).total_seconds()

        if timeInSeconds >= 3600:
            return divmod(timeInSeconds, 3600)[0]


def convertCsvToJson(csvFileName, jsonFileName):
    with open(csvFileName + '.csv') as r, open(jsonFileName + '.json', 'w') as w:
        convert(r, w)


def main():
    # convertCsvToJson("repositories", "repositories")

    with open('files/repositories.json') as f:
        repositoriesList = json.load(f)
    for i in range(len(repositoriesList)):
        getPullRequests(repositoriesList[i]['name'], repositoriesList[i]['owner'])