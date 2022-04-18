from datetime import datetime

import requests
import pandas as pd

token = "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"
endCursor = ""
hasNextPage = False


def getPRNextQuery(endcursor, name, owner):
    prNextQuery = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 50, after: "%s") {
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
        pullRequests(first: 50) {
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
    doOperations(request.json(), prList)

    while hasNextPage:
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
                if (closed & merged) or (closed and (merged is False)):
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


def readFile():
    fileLines = []

    with open("repositories.csv") as file:
        for line in file:
            fileLines.append(line)

    return fileLines


def main():
    # getPullRequests("system-design-primer", "donnemartin")

    list = readFile()
    print(list[0])
