import json

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

    request = requests.post(url, json={'query': prFirstQuery}, headers=headers)
    checkIfHasNext(request)
    print(request.json())

    while hasNextPage:
         request = requests.post(url, json={'query': getPRNextQuery(endCursor, name, owner)}, headers=headers)
         checkIfHasNext(request)
         print(request.json())

def checkIfHasNext(request):
    jsonResponse = request.json()

    global hasNextPage
    hasNextPage = jsonResponse['data']['repository']['pullRequests']['pageInfo']['hasNextPage']

    global endCursor
    endCursor = jsonResponse['data']['repository']['pullRequests']['pageInfo']['endCursor']

def tester():
    f = open("repositories.csv", 'r')
    texto = f.readlines()

    x = 0

    while x < len(texto):
        if texto[x] == "\n":
            local = texto.index(texto[x])
            texto.pop(local)
        else:
            texto[x] = texto[x].split(',')
            x += 1

    # name = texto[10][1]
    # owner = texto[10][2]

    return texto

def main():
    text = tester()

    print(text)