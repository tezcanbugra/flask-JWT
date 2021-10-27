from flask import Flask, jsonify, request, make_response
import jwt, datetime
import functools import wraps


app = Flask(__name__)

#You shouldn't store the secret key in a public place or in product environment. This is only for an example. 
app.config['SECRET_KEY'] = 'changethiss3cr3tkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        
        if not token:
            return jsonify({'message' : 'Token is missing.'}) , 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        else: 
            return jsonify({'message' : 'Token is invalid.'}) , 403

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can see this.'})

@app.route('protected')
@token_required
def protected():
    return jsonify({'message' : 'This is a protected page.'})

@app.route('login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password'
        token = jwt.encode({'user': auth.username, 'expire': datetime.datetime.utcnow() + datetime.timedelta(minutes=30), app.config['SECRET_KEY']})
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Couldn\'t verify!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})



if __name__ == '__main__':
    app.run(debug=True)