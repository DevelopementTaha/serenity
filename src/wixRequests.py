from pprint import pprint
import requests
import json
from CollectionObject import CollectionObject
from SimpleNameSpace import SimpleNameSpace

from ImageObject import ImageObject
from SessionObject import SessionObject
from keywordObject import keywordObject
from PositipsObject import PositipsObject
from ArticlesObject import ArticlesObject
from UserObject import UserObject

url = "https://www.ma-pause-serenity.fr/_functions-dev"

def getSessions():
    global url
    myUrl = url + "/sessions"

    myResponse = requests.get(myUrl, verify=True)

    if(myResponse.ok):
        jData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d)) #List of rows
        myList = []
        for obj in jData.sessions:  # for loop for the list of rows (1 single row is called obj)
            so = SessionObject(obj._id,obj.title,obj.keyword,obj.ambiance, obj.duree, obj.image, obj.video, obj.categorie,obj.imageCategorie,obj.description,obj.audio)
            myList.append(so)
        
        return myList
        
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None

def getSession(id):
    global url
    myUrl = url + "/session/" + id

    myResponse = requests.get(myUrl, verify=True)

    if(myResponse.ok):
        jData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d)) #List of rows
        so = SessionObject(jData.sessions[0]._id,jData.sessions[0].title,jData.sessions[0].keyword, jData.sessions[0].ambiance, jData.sessions[0].duree, jData.sessions[0].image, jData.sessions[0].video, jData.sessions[0].categorie,jData.sessions[0].imageCategorie,jData.sessions[0].description,jData.sessions[0].audio)
        return so
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None

def getPositip(id):
    global url
    myUrl = url + "/positip/" + id

    myResponse = requests.get(myUrl, verify=True)

    if(myResponse.ok):
        jData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d)) #List of rows
        po = PositipsObject(jData.positips[0]._id,jData.positips[0].title,jData.positips[0].homePageImage,jData.positips[0].category, jData.positips[0].textImage, jData.positips[0].description, jData.positips[0].text, jData.positips[0].hiddenText)
        return po
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None


def getArticle(id):
    global url
    myUrl = url + "/article/" + id

    myResponse = requests.get(myUrl, verify=True)

    if(myResponse.ok):
        jData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d)) #List of rows
        ao = ArticlesObject(jData.articles[0]._id,jData.articles[0].title,jData.articles[0].homePageImage,jData.articles[0].articleImage, jData.articles[0].description)
        return ao
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None


def getsessionsMainLink():	
    global url	
    myUrl = url + "/sessionsMainLink"	
    myResponse = requests.get(myUrl, verify=True)	
    if(myResponse.ok):	
        #jData = json.loads(myResponse.content)	
        objectData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d))	
        listOfImages = []	
        for image in objectData.imageData:	
            io = ImageObject(image.imageId,image.imageName,image.imageLink, image.video)	
            listOfImages.append(io)	
       #print(jData)	
        return listOfImages	
    else:	
        myResponse.raise_for_status()	
        print("Request Failed! on URL: " + myUrl)	
        return None	


def getCollection(id):
    global url
    myUrl = url + "/collection/" + id 


    myResponse = requests.get(myUrl, verify=True) 

    if(myResponse.ok):

        objectData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d))
        for i in range(len(objectData.collections)):
            colObject = objectData.collections[i]
            co = CollectionObject(colObject._id,colObject.name, colObject.image, colObject.description, colObject.collectionsOrder, colObject.showSession, colObject.sessionsOrder, colObject.showCollection, colObject.showPositip, colObject.showArticle)
            
            for session in objectData.sessions[i].sessionRef:
                so = SessionObject(session._id,session.title,session.keyword,session.ambiance, session.duree, session.image, session.video, session.categorie,session.imageCategorie,session.description,session.audio)
                co.addSessionObject(so)
            for positip in objectData.positips[i].positipsDataBase:
                po = PositipsObject(positip._id,positip.title,positip.homePageImage,positip.category, positip.textImage, positip.description, positip.text, positip.hiddenText)
                co.addPositipsObject(po)
            for article in objectData.articles[i].articlesDataBase:
                ao = ArticlesObject(article._id,article.title,article.homePageImage,article.articleImage, article.description)
                co.addArticlesObject(ao)

        return co
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None

def getAllCollections():
    global url
    myUrl = url + "/allCollections"

    myResponse = requests.get(myUrl, verify=True) 

    if(myResponse.ok):

        objectData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d))
        listOfCollections = []
        for i in range(len(objectData.collections)):
            colObject = objectData.collections[i]
            co = CollectionObject(colObject._id,colObject.name, colObject.image, colObject.description, colObject.collectionsOrder, colObject.showSession, colObject.sessionsOrder,colObject.showCollection, colObject.showPositip, colObject.showArticle)
            
            for session in objectData.sessions[i].sessionRef:
                so = SessionObject(session._id,session.title,session.keyword,session.ambiance, session.duree, session.image, session.video, session.categorie,session.imageCategorie,session.description,session.audio)
                co.addSessionObject(so)
            for positip in objectData.positips[i].positipsDataBase:
                po = PositipsObject(positip._id,positip.title,positip.homePageImage,positip.category, positip.textImage, positip.description, positip.text, positip.hiddenText)
                co.addPositipsObject(po)
            for article in objectData.articles[i].articlesDataBase:
                ao = ArticlesObject(article._id,article.title,article.homePageImage,article.articleImage, article.description)
                co.addArticlesObject(ao)

            listOfCollections.append(co)
        sortedCollectionList = sorted(listOfCollections, key=lambda x: x.order)
        sortedSessionList = sorted(listOfCollections, key=lambda x: x.sessionsOrder)
        return listOfCollections, sortedCollectionList, sortedSessionList
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None

def getkeyword():
    global url
    myUrl = url + "/keyword"

    myResponse = requests.get(myUrl, verify=True)

    if(myResponse.ok):

        #jData = json.loads(myResponse.content)
        keywordData = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d))
        listOfkeywords = []
        for keyword in keywordData.datas:
            ko = keywordObject(keyword.title,keyword.equivalent, keyword.image)
            listOfkeywords.append(ko)

       #print(jData)
        return listOfkeywords
    else:
        myResponse.raise_for_status()
        print("Request Failed! on URL: " + myUrl)
        return None

def postUserSession(userName, userId, sessionId):

    user = getUserSession(userId)

    if(user is not None):
        return updateUserSession(user.id, userName, userId, sessionId)
    else:
        return insertUserSession(userName, userId, sessionId)


def insertUserSession(userName, userId, sessionId):

    myUrl = url + "/insertUserSession"
    validity = getUserSessionValidity(userId)
    if(validity is None):
        validity = 6 #default

    jsons = {"userName": userName, "userId": userId, "sessionId": sessionId, "validity": validity}
    
    myResponse = requests.post(myUrl, data=json.dumps(jsons))

    if(myResponse.ok):
        print("User " + userName + " Inserted in with sessionId: " + sessionId)
        return True
    else:
        print("User " + userName + " Insertion not successful with sessionId: " + sessionId)
        return False

def updateUserSession(id, userName, userId, sessionId):

    myUrl = url + "/updateUserSession"

    validity = getUserSessionValidity(userId)
    if(validity is None):
        validity = 6 #default

    myResponse = requests.post(
    myUrl,
    json = {"_id": id, "userName": userName, "sessionId": sessionId, "validity": validity})
    if(myResponse.ok):
        print("User " + userName + " updated in with sessionId: " + sessionId)
        return True
    else:
        print("User " + userName + " update not successful with sessionId: " + sessionId)
        return False

def getUserSession(userId):
    myUrl = url + "/findUserSession/"+ userId

    myResponse = requests.get(myUrl,verify=True)

    if(myResponse.ok):
        userSession = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d)) #List of rows
        user = UserObject(userSession.userSessions[0]._id,userSession.userSessions[0].userName,userSession.userSessions[0].userId,userSession.userSessions[0].sessionId,userSession.userSessions[0]._updatedDate,userSession.userSessions[0].validity)
        print("User " + user.userName + " exists with SessionId: " + user.sessionId)
        return user
    else:
        print("User with Id" + userId + " does not exist")
        return None

def getUserSessionValidity(userId):
    myUrl = url + "/sessionValidity/"

    myResponse = requests.get(myUrl,verify=True)

    if(myResponse.ok):
        validityRow = json.loads(myResponse.content, object_hook=lambda d: SimpleNameSpace(**d)) #List of rows
        validity = (validityRow.validity[0].validity)
        return validity
    else:
        return None
