from wixRequests import postUserSession

def addUserSessionToDB(userName, sessionId):
    postUserSession(userName, sessionId)

def loginUserWithSessionId(userName, sessionId):
    if(userName is not None):

        #decode Hash MD5
        #https://stackoverflow.com/questions/11567290/cryptojs-and-pycrypto-working-together
        #  Better ->  https://medium.com/@sachadehe/encrypt-decrypt-data-between-python-3-and-javascript-true-aes-algorithm-7c4e2fa3a9ff
        addUserSessionToDB(userName, sessionId)
        return True
    return False

def validateUserSessionTime(userName):

    return False
