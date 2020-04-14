from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/users', methods=['GET','POST','DELETE'])
def get_users():
   if request.method == 'GET':
       search_username = request.args.get('name') #accessing val of param 'name'
       search_job = request.args.get('job')
       # if there is a name to search for, only return subdict of users w/ name
       if search_username and search_job:
          subdict = {'users_list' : []} #empty subdict to add to if name match found
          for user in users['users_list']:
             if user['name'] == search_username and user['job'] == search_job:
                subdict['users_list'].append(user)
          return subdict
       return users
   elif request.method == 'POST':
       userToAdd = request.get_json() #get the data/body of the http request
       users['users_list'].append(userToAdd)
       resp = jsonify(success=True) #set the http response to show success
       #resp.status_code = 200 #optionally, you can always set a response code.
       # 200 is the default code for a normal response
       return resp
   elif request.method == 'DELETE':
       userToDelete = request.get_json() #get the data/body of the http request
       users['users_list'].remove(userToDelete)
       resp = jsonify(success=True) #set the http response to show success
       #resp.status_code = 200 #optionally, you can always set a response code.
       # 200 is the default code for a normal response
       return resp

@app.route('/users/<id>')
def get_user(id):
   if id:
      for user in users['users_list']:
         if user['id'] == id:
            return user #return user if found
      return ({}) #if no user matches id, return empty dict
   return users #if id not asked for, return all users

# in the form of a JSON object (or python dictionary)
users = {
   'users_list' :
   [
      {
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123',
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222',
         'name': 'Mac',
         'job': 'Professor',
      },
      {
         'id' : 'yat999',
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555',
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}
