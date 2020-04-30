from random import randint
from flask import Flask
from flask import request
from flask import jsonify
from model_mongodb import User
from flask_cors import CORS # Cross-Origin Resource Sharing
app = Flask(__name__)
CORS(app) # allow our backend to respond to calls coming from a different origin

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
         'job': 'Aspiring actress',
      },
      {
         'id' : 'zap555',
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
	return 'Hello, World!'

# randomly generate a 6-digit string id from tex/viewable ascii chars (33-126)
def randID():
    id = ""
    for i in range(0, 6):
        id += chr(randint(ord('!'), ord('~')))
    return id

def find_user_by_name_and_job(name, job):
    subdict = {'users_list' : []} #empty subdict to add to if name match found
    for user in users['users_list']:
       if user['name'] == name and user['job'] == job:
          subdict['users_list'].append(user)
    return subdict

def find_user_by_name(name):
    subdict = {'users_list' : []} #empty subdict to add to if name match found
    for user in users['users_list']:
       if user['name'] == name:
          subdict['users_list'].append(user)
    return subdict

@app.route('/users', methods=['GET','POST'])
def get_users():
   global users
   if request.method == 'GET':
       search_username = request.args.get('name') #accessing val of param 'name'
       search_job = request.args.get('job')
       # if there is a name AND a job to search for, only return subdict of users w/ name, job
       if search_username and search_job:
          users = User().find_by_name_and_job(search_username, search_job);
       elif search_username:
          # users = find_user_by_name(search_username)
          users = User().find_by_name(search_username)
       else:
          users = User().find_all()
       return {"users_list": users}
   elif request.method == 'POST':
       userToAdd = request.get_json() #get the data/body of the http request
       # userToAdd['id'] = randID()
       # users['users_list'].append(userToAdd)
       newUser = User(userToAdd)
       newUser.save()
       resp = jsonify(newUser), 201
       return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    user = User({"_id":id})
    if request.method == 'GET':
        user.reload()
        return user
    elif request.method == 'DELETE':
        # if id:
        #     for user in users['users_list']:
        #         if user['id'] == id:
        #             # TODO: delete user
        #             users['users_list'].remove(user)
        #             resp = jsonify(success=True) #set the http response to show success
        #             resp.status_code = 200 #optionally, you can always set a response code.
        #             return resp
        #if id not asked for or no user id matches, error
        resp = jsonify(success=user.remove()), 204 #set the http response to show No Content
        return resp
