import requests

def getRepositories():
    global repositoriesCount
    repositoriesCount = 0

    global endCursor
    endCursor = ""

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
        search(type: REPOSITORY, query:"stars:>100", first: 10, after: %s ) {
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
    filterRepository(request, repositoriesCount, endCursor)



def filterRepository(request, repositoriesCount, endCursor):
    jsonResponse = request.json()

    jsonTotalCount = len(jsonResponse['data']['search']['nodes'])

    if jsonTotalCount > 0:
        for i in range(jsonTotalCount):
            repository = jsonResponse['data']['search']['nodes'][i]

            pullRequestMergedCount = repository["pullRequestMerged"]['totalCount']
            pullRequestClosedCount = repository["pullRequestClosed"]['totalCount']

            if (pullRequestMergedCount >= 50 & pullRequestClosedCount >= 50) |\
                (pullRequestMergedCount + pullRequestClosedCount >= 100):
                print(f' name: {repository["name"]}')

                repositoriesCount += 1
                print(repositoriesCount)

            endCursor = jsonResponse['data']['search']['pageInfo']['endCursor']
            print(endCursor)
