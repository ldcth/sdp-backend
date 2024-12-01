from pymongo import MongoClient

uri = "mongodb+srv://ductho263:Ductho263@historycluster.mrqug.mongodb.net/history-quiz?retryWrites=true&w=majority&appName=HistoryCluster"
# uri = "mongodb+srv://NgVSang:Sang100302@demoproject.mbabi.mongodb.net/?retryWrites=true&w=majority&appName=demoProject"

client = MongoClient(uri)

database = client.get_database('history-quiz')
# database = client.get_database('PBL_7')