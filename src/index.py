import json
import uuid
from flask import Flask, render_template, request, session, redirect
from urllib.parse import unquote_plus
from LoginUtils import isUserValidInSession, loginUserWithSessionId

app = Flask(__name__)
app.secret_key = 'serenity'
from wixRequests import getSessions, getSession, getPositip, getArticle, getCollection, getkeyword, getAllCollections

@app.route('/')
def index():
    sortedCollectionList, sortedSessionList = getAllCollections()
    anyCollections = any(col.showCollection == True for col in sortedCollectionList) #boolean variable
    keyword = getkeyword()
    try:
        if(isUserValidInSession(session['userId'])):
            return render_template('index.html', collections = sortedCollectionList, sortedSessionListFromCollection = sortedSessionList, keys = keyword, anyCollections = anyCollections)
        else:
            return redirect('/sessionExpired')
    except KeyError as ke:
        return redirect('/sessionExpired')

@app.route('/login')
def loginHome():
    user = request.args.get('user', None)
    data = json.loads(user)
    userName = data['fullName']
    userId = data['id']
    sessionId = str(uuid.uuid4())
    session['uid'] = sessionId
    loggedSuccessfully = loginUserWithSessionId(userName, userId, sessionId)
    if loggedSuccessfully:
        session['userId'] = userId
        return redirect('/')
    else:
        return redirect('/sessionExpired')

@app.route('/card')
def card():
    clickedKey = request.args.get('keyword', '')
    sessions = getSessions()
    keys = getkeyword()
    if(isUserValidInSession(session['userId'])):
        return render_template('card.html', sessions = sessions, keys = keys, clickedKey = clickedKey)
    else:
        return redirect('/sessionExpired')

@app.route('/showSession')
def showSession():
    sessionId = request.args.get('sessionId', None)
    selectedSession = getSession(sessionId)
    
    if(isUserValidInSession(session['userId'])):
        return render_template('SessionPage.html', session = selectedSession)
    else:
        return redirect('/sessionExpired')

@app.route('/showPositips')
def showPositip():
    positipId = request.args.get('positipId', None)
    selectedSession = getPositip(positipId)
    
    if(isUserValidInSession(session['userId'])):
        return render_template('Positips.html', session = selectedSession)
    else:
        return redirect('/sessionExpired')

@app.route('/showArticles')
def showArticle():
    articleId = request.args.get('articleId', None)
    selectedSession = getArticle(articleId)
    
    if(isUserValidInSession(session['userId'])):
        return render_template('Articles.html', session = selectedSession)
    else:
        return redirect('/sessionExpired')

@app.route('/showSessionAudio')
def showSessionAudio():
    sessionId = request.args.get('sessionId', None)
    selectedSession = getSession(sessionId)
    
    if(isUserValidInSession(session['userId'])):
        return render_template('SessionAudio.html', session = selectedSession)
    else:
        return redirect('/sessionExpired')

@app.route('/showCollections')
def showCollections():
    collectionId = request.args.get('collectionId', None)
    collection = getCollection(collectionId)
    
    if(isUserValidInSession(session['userId'])):
        return render_template('collection.html', collection = collection)
    else:
        return redirect('/sessionExpired')

@app.route('/openLink')
def openLink():
    videoLink = unquote_plus(request.args.get('videoLink'))
    
    if(isUserValidInSession(session['userId'])):
        return render_template('/try.html', videoLink = videoLink)
    else:
        return redirect('/sessionExpired')

@app.route('/sessionExpired')
def expired():
    return render_template('SessionExpired.html')

@app.route('/None')
def none():
    return render_template('/notFound.html')

@app.route('/loginPage.html')
def login():
    return render_template('Loginpage.html')

@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
