from app import app

@app.route('/test')
def testroute():
    return 'not a 404'