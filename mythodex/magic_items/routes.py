from app import app, connect_db

@app.route('/test')
def testroute():
    return 'not a 404'