import json

import requests
import pandas as pd

url = 'https://api.github.com/graphql'
token = "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"

name = ""
owner = ""
endCursor = ""
hasNextPage = False

def getPRNextQuery(endcursor):
    prNextQuery = """
    {
      repository(owner: "donnemartin", name: "system-design-primer") {
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
    """ % (endcursor)

    return prNextQuery

def getPullRequests():
    headers = {"Authorization": "Bearer " + token}

    prFirstQuery = """
    {
      repository(owner: "donnemartin", name: "system-design-primer") {
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
    """ # % (owner, name)

    request = requests.post(url, json={'query': prFirstQuery}, headers=headers)
    checkPullRequest(request)
    print(request.json())

    while hasNextPage:
            request = requests.post(url, json={'query': getPRNextQuery(endCursor)}, headers=headers)
            checkPullRequest(request)
            print(request.json())

def checkPullRequest(request):
    jsonResponse = request.json()

    global endCursor
    endCursor = jsonResponse['data']['repository']['pullRequests']['pageInfo']['endCursor']

    global hasNextPage
    hasNextPage = jsonResponse['data']['repository']['pullRequests']['pageInfo']['hasNextPage']

def getRepositoryDataFromFile():
