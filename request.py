import pandas as pd
import requests

repositoriesCount = 0
endCursor = ""

def getNextQuery(endcursor):
    nextQuery = """
        {
        search(type: REPOSITORY, query:"stars:>100", first: 5, after:"%s") {
            pageInfo {
                hasNextPage
                endCursor    
            }
            nodes {
            ... on Repository {
                    name
                    owner {
                        login
                    }
                    url
                    createdAt
                    updatedAt

                    pullRequestMerged: pullRequests(states: MERGED){
                        totalCount
                    }

                    pullRequestClosed: pullRequests(states: CLOSED){
                        totalCount
                    }
                } 
            } 
        }
    }
    """ % endcursor

    print('endcursor é ' + endcursor)
    return nextQuery


def getRepositories():
    url = 'https://api.github.com/graphql'
    token = "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"
    headers = {"Authorization": "Bearer " + token}

    print('endcursor é ' + endCursor)

    firstQuery = """
        {
        search(type: REPOSITORY, query:"stars:>100", first: 5) {
            pageInfo {
                hasNextPage
                endCursor    
            }
            nodes {
            ... on Repository {
                    name
                    owner {
                        login
                    }
                    url
                    createdAt
                    updatedAt

                    pullRequestMerged: pullRequests(states: MERGED){
                        totalCount
                    }

                    pullRequestClosed: pullRequests(states: CLOSED){
                        totalCount
                    }
                } 
            } 
        }
    }
    """

    listR = []

    request = requests.post(url, json={'query': firstQuery}, headers=headers)
    while repositoriesCount < 100:
        filterRepository(request, listR)
        request = requests.post(url, json={'query': getNextQuery(endCursor)}, headers=headers)

    df = pd.DataFrame(listR)
    df.to_csv('repositories.csv', encoding='utf-8')

def filterRepository(request, repoList):
    jsonResponse = request.json()
    jsonTotalCount = len(jsonResponse['data']['search']['nodes'])

    global endCursor
    endCursor = jsonResponse['data']['search']['pageInfo']['endCursor']

    if jsonTotalCount > 0:
        for i in range(jsonTotalCount):
            repository = jsonResponse['data']['search']['nodes'][i]

            pullRequestMergedCount = repository["pullRequestMerged"]['totalCount']
            pullRequestClosedCount = repository["pullRequestClosed"]['totalCount']

            if (pullRequestMergedCount >= 50 & pullRequestClosedCount >= 50) | \
                    (pullRequestMergedCount + pullRequestClosedCount >= 100):
                print(f' name: {repository["name"]}')
                repoList.append(repository)

                global repositoriesCount
                repositoriesCount += 1