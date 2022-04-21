from pymongo import MongoClient
import certifi

class Mongo:

    CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.n0lfs.mongodb.net/Lab03?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    db = client["Lab03"]
    prCollection = db["pull_requests"]
    savedReposCollection = db["saved_repos"]

    def insert_one(self, value):
        self.prCollection.insert_one(value)
        print('foi!\n', value)

    def insert_repository(self, repo_name):
        self.savedReposCollection.insert_one({"repo_name": repo_name})
        print(f'Processamento do repositório {repo_name} concluído.')

    def removePRs(self, repo_name):
        self.prCollection.delete_many(repo_name)
        print(f'PR do {repo_name} removidos')