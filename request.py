import json

import requests

def getRepositories():
    url = 'https://api.github.com/graphql'
    token = "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"
    headers = {"Authorization": "Bearer " + token}

    query = """
    {
        search(query:"stars:>100", type:REPOSITORY, first:5){
            pageInfo {
                startCursor
                endCursor
                hasNextPage
            }
            nodes {
            ... on Repository {
                    name
                    url
                    createdAt
                    updatedAt
              
                    pullRequestMerged: pullRequests(states: MERGED){
                        totalCount
                    }
              
                    pullRequestClosed: pullRequests(states: CLOSED){
                        totalCount
                    }
              
                    owner {
                        login
                    }
                } 
            } 
        }
    }
    """

    request = requests.post(url, json={'query': query}, headers=headers)
    filterRepository(request)

def filterRepository(request):
    jsonResponse = request.json()

    jsonTotalCount = len(jsonResponse['data']['search']['nodes'])

    for i in range(jsonTotalCount):

        repository = jsonResponse['data']['search']['nodes'][i]

        pullRequestMergedCount = repository["pullRequestMerged"]['totalCount']
        pullRequestClosedCount = repository["pullRequestClosed"]['totalCount']

        if (pullRequestMergedCount >= 50 & pullRequestClosedCount >= 0) |\
            (pullRequestMergedCount + pullRequestClosedCount >= 100):
            print(f' name: {repository["name"]}')