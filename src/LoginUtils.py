from wixRequests import postUserSession, getUserSession
from datetime import datetime, timedelta

def addUserSessionToDB(userName, userId, sessionId):
    return postUserSession(userName, userId, sessionId)

def loginUserWithSessionId(userName, userId, sessionId):
    if(userName is not None and userId is not None):

        #decode Hash MD5
        #https://stackoverflow.com/questions/11567290/cryptojs-and-pycrypto-working-together
        #  Better ->  https://medium.com/@sachadehe/encrypt-decrypt-data-between-python-3-and-javascript-true-aes-algorithm-7c4e2fa3a9ff
        return addUserSessionToDB(userName, userId, sessionId)
    return False

def isUserValidInSession(userId):
    if(userId is not None):
        user = getUserSession(userId)
        if(user is not None):
            timeNow = datetime.utcnow()
            updatedDate = datetime.strptime(user.updatedDate, '%Y-%m-%dT%H:%M:%S.%fZ')
            expiryDate = updatedDate + timedelta(hours=user.validity)
            if(timeNow < expiryDate):
                return True
    return False
