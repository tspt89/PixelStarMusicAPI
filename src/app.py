from flask import Flask, request, render_template, jsonify
import spotipy
import redis
import json
import re
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)


r = redis.StrictRedis(
	host='104.198.244.0',
	port=6379,
	charset="utf-8",
	decode_responses=True
	)




@app.route('/')
def inicio():
	app.logger.info(f"Entramos al path {request.path}")
	return "Hola Mundo desde flask."

@app.route('/saludar/<nombre>')
def saludar(nombre):
	return f'Saludos {nombre}'

@app.route('/edad/<int:edad>')
def mostrar_edad(edad):
	return f'Tu edad es: {edad}'

@app.route('/mostrar/<nombre>', methods=['GET','POST'])
def mostrar_nombre(nombre):
	return render_template('mostrar.html',nombre=nombre)

@app.route('/api/mostrarPlaylist')
def getPlaylist():
	
	sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="22af8a2d155b479ba6971680d903d894",
															   client_secret="e75127b7d9244deeb95385fc825715cf"))
	results = sp.playlist('spotify:playlist:3WxTnGherpf7t4F0VzchD4')
	array = []
	#print(results)
	#results = sp.playlist('spotify:playlist:37i9dQZEVXbMDoHDwVN2tF')
	for idx, track in enumerate(results['tracks']['items']):
		res = {	'name':track['track']['name'],
				'artist':track['track']['artists'][0]['name'],
				'album':track['track']['album']['name'],
				'release': track['track']['album']['release_date'],
				'duration': track['track']['duration_ms']
				}
		#unidict = {k.decode('utf8'): v.decode('utf8') for k, v in strdict.items()}
		r.rpush('top',track['track']['name'])
		r.hmset(track['track']['name'],res);
		array.append(res)
		print(res)
    #print(json.dumps(results, sort_keys=True, indent=4))
	#return jsonify(res)
	print("array completo:",array)
	return jsonify(array)

@app.route('/login', methods=['POST'])
def login():
	print("JSON")
	#
	content = request.get_json()
	tmp = r.hgetall(content['email'])
	print("LOGIN",tmp)
	if content['email'].encode("utf-8") == tmp['email'] and content['password'] == tmp['password']:
		return jsonify(True)
	else:
		return jsonify(False)
	
@app.route('/register', methods=['POST'])
def registration():
	print("JSON")
	content = request.get_json()
	print(content)
	if check(content['email']) and len(content['password']) >= 5:
		print("PASA")
		if content['name']:
			if content['lastname']:
				regis = {'name': content['name'],
						'lastname':content['lastname'],
						'email':content['email'],
						'password': content['password']}
				r.hmset(content['email'],regis);
				tmp = r.hgetall(content['email'])
				print("HGETALL",tmp)
				
				return json.dumps(True)
	

	return jsonify(False)

def check(email):  
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

	# pass the regular expression 
	# and the string in search() method 
	if(re.search(regex,email)):  
		print("Valid Email")
		return True
	
	else:  
		print("Invalid Email")
		return False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=4000)