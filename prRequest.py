import json
from datetime import datetime
from pymongo import MongoClient

import requests
import pandas as pd
from csv2json import convert, load_csv, save_json

tokenAlt = "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"
tokenLe = "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"
tokenLucas = "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"

endCursor = ""
hasNextPage = False

tokens = [tokenAlt, tokenLe, tokenLucas]
cursorCount = 0
token = tokens[cursorCount % 3]

client = MongoClient()

def getPRNextQuery(endcursor, name, owner):
    prNextQuery = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 10, after: "%s") {
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
    url = 'https://api.github.com/graphql'
    headers = {"Authorization": "Bearer " + token}

    prFirstQuery = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 10) {
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

    prList = []

    request = requests.post(url, json={'query': prFirstQuery}, headers=headers)

    if request.status_code == 200:
        doOperations(request.json(), prList)
        while hasNextPage:

            request = requests.post(url, json={'query': getPRNextQuery(endCursor, name, owner)}, headers=headers)
            doOperations(request.json(), prList)
    elif request.status_code == 502:
        global cursorCount
        cursorCount += 1

        global token
        token = tokens[cursorCount % 3]

        request = requests.post(url, json={'query': getPRNextQuery(endCursor, name, owner)}, headers=headers)
        doOperations(request.json(), prList)

    df = pd.DataFrame(prList)
    df.to_csv('pullrequestTeste.csv', encoding='utf-8')


def doOperations(response, list):
    checkIfHasNext(response)
    filterPullRequest(response, list)


def checkIfHasNext(request):
    global hasNextPage
    hasNextPage = request['data']['repository']['pullRequests']['pageInfo']['hasNextPage']

    # if hasNextPage != True:
        # salvar aqui processado

    global endCursor
    endCursor = request['data']['repository']['pullRequests']['pageInfo']['endCursor']


def filterPullRequest(request, list):
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

            if (closed or merged) and reviews >= 1:
                if (closed and merged) or (closed and not merged):
                    timeSpent = calculateCloseMergeTime(createdAt, closedAt)
                else:
                    timeSpent = calculateCloseMergeTime(createdAt, mergedAt)

                if timeSpent is not None:
                    list.append(pullRequest)
                    print(pullRequest)


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
    convertCsvToJson("repositories", "repositories")

    with open('repositories.json') as f:
        repositoriesList = json.load(f)

    # for i in range(len(repositoriesList)):
    #     getPullRequests(repositoriesList[i]['name'], repositoriesList[i]['owner'])

    getPullRequests("system-design-primer", "donnemartin")