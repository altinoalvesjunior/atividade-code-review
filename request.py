import requests

def getRepositories():
    url = 'https://api.github.com/graphql'
    token = "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"
    headers = {"Authorization": "Bearer " + token}

    query = """
    query getRepoInfo {
        search(query: "stars:>100", type: REPOSITORY, first: 25) {
            nodes {
              ... on Repository {
                nameWithOwner
                url
                createdAt
                primaryLanguage {
                  name
                  id
                }
              }
            }
        }
    }
    """

    request = requests.post(url, json={'query': query}, headers=headers)
    print(request.content)