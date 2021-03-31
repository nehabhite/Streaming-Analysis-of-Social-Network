import pymongo

# TWITTER API KEYS
# used to connect with twitter public API to fetch tweets
CONSUMER_API_KEY = "MsR0xzen9YvoA8XDA1eJVdufy"
CONSUMER_API_SECRET = "kMpRIH51FyvFgFu0ofR8rmLbqMnCSfLAFchYFnglDkYWDg5t5r"
ACCESS_TOKEN = "137438589-H3540VwUJB4Ia8MSjoOinISV9oVeOjq2VDyEoGUQ"
ACCESS_TOKEN_SECRET = "MFK6NDBHDis1GFDAXc6cDmfmV0pqq8eYa5muyAPkdEN2O"

#SET UP LOCAL MONGODB CONNECTIONS
LOCAL_CLIENT = pymongo.MongoClient()

print("Connection established with MongoDB successfully!")
