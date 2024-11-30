from pymongo import MongoClient

uri = "mongodb+srv://ductho263:Ductho263@historycluster.mrqug.mongodb.net/history-quiz?retryWrites=true&w=majority&appName=HistoryCluster"

client = MongoClient(uri)

database = client.get_database('history-quiz')
