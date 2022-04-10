import requests

repositoriesCount = 0
endCursor = ""


def getRepositories():
    url = 'https://api.github.com/graphql'
    token = "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"
    headers = {"Authorization": "Bearer " + token}

    firstQuery = """
        {
        search(type: REPOSITORY, query:"stars:>100", first: 10) {
            pageInfo {
                hasNextPage
                endCursor    
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
                } 
            } 
        }
    }
    """

    nextQuery = """
        {
        search(type: REPOSITORY, query:"stars:>100", first: 10, after:"%s") {
            pageInfo {
                hasNextPage
                endCursor    
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
                } 
            } 
        }
    }
    """ % endCursor

    request = requests.post(url, json={'query': firstQuery}, headers=headers)
    filterRepository(request)
    print(endCursor)

    request = requests.post(url, json={'query': nextQuery}, headers=headers)
    filterRepository(request)

    # while True:
    #     request = requests.post(url, json={'query': firstQuery}, headers=headers)
    #     filterRepository(request, repositoriesCount)
    #
    #     if not repositoriesCount < 100:
    #         break


def filterRepository(request):
    jsonResponse = request.json()

    jsonTotalCount = len(jsonResponse['data']['search']['nodes'])

    global endCursor
    endCursor = jsonResponse['data']['search']['pageInfo']["endCursor"]

    if jsonTotalCount > 0:
        for i in range(jsonTotalCount):
            repository = jsonResponse['data']['search']['nodes'][i]

            pullRequestMergedCount = repository["pullRequestMerged"]['totalCount']
            pullRequestClosedCount = repository["pullRequestClosed"]['totalCount']

            if (pullRequestMergedCount >= 50 & pullRequestClosedCount >= 50) | \
                    (pullRequestMergedCount + pullRequestClosedCount >= 100):
                print(f' name: {repository["name"]}')

                global repositoriesCount
                repositoriesCount += 1