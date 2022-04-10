import requests

def getPullRequests():
    url = 'https://api.github.com/graphql'
    token = "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"
    headers = {"Authorization": "Bearer " + token}

    owner = None
    name = None

    prFirstQuery = """
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 15) {
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
    """ % (owner, name)

    request = requests.post(url, json={'query': prFirstQuery}, headers=headers)
    print(request)

    def getPRNextQuery(endcursor):
        prNextQuery = """
          repository(owner: "freeCodeCamp", name: "freeCodeCamp") {
            pullRequests(first: 15, after: "endCursor") {
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
        """ % endcursor

        return prNextQuery