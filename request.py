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
    # print(request.z)
    jsonResponse = request.json()
    repository = jsonResponse['data']['search']['nodes'][0]
    print(f'Repository name: {repository["name"]}')

    pullRequestMergedCount = repository["pullRequestMerged"]['totalCount']
    pullRequestClosedCount = repository["pullRequestClosed"]['totalCount']
    print(pullRequestMergedCount)
    print(pullRequestClosedCount)

