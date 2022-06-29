import pymongo
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps
from flask import Flask, render_template, jsonify , Response, request
from dotenv import load_dotenv
import os
from .connection import *
from math import radians, cos, sin, asin, sqrt

@app.route('/signup', methods =['POST' , 'GET'])
def signup () :
   #data = db.storeOwner
   
   req_Json= request.json
   email=req_Json['email']
   password=req_Json['password']
   storeName=req_Json['storeName']

   Filter = {"email":email}
   if db.storeOwner.count_documents(Filter):
     return("Thsi email already has an store. Try another one.")
   else:
     db.storeOwner.insert_one({"email": email, "password": password, "storeName": storeName})
     result = db.storeOwner.find_one({'email': email},{'_id':1})
     print(result)
     return json.dumps(result, indent=4, default = json_util.default)
  
###########################################################################################
@app.route('/login', methods = ['GET','POST'])
def login():
    data = db.storeOwner
    req_Json= request.json
    email=req_Json['email']
    password=req_Json['password']
    result = data.find_one({'email':email , 'password':password},{})
    print(result)
    
    return json.dumps(result, indent=4, default = json_util.default)

###########################################################################################
@app.route('/edit_profile', methods =['GET','POST'])
def editProfile () :

  req_Json= request.json
  ID=req_Json['ID']
  storeName=req_Json['storeName']
  phone_number=req_Json['phone_number']
  facebook_link=req_Json['facebook_link']
  another_link=req_Json['another_link']
  image=req_Json['image']
  longtiude=req_Json['longtiude']
  latitude=req_Json['latitude']

  data = db.storeOwner.update_one({"_id":ObjectId(ID)}, 
   {   "$set": {"storeName":storeName, "contacts":{"phone_number":phone_number, "facebook_link":facebook_link, "another_link":another_link}, "location":{'longtiude':longtiude, 'latitude':latitude} }  } )

  return 'Product updated successfully.'

###########################################################################################
@app.route('/delete_account', methods = ['GET'])
def deleteAccount():
    req_Json= request.json
    ID=req_Json['ID']
    data = db.storeOwner.delete_one({'_id':ObjectId(ID)})

    return 'Account deleted successfully'
###########################################################################################

@app.route('/searchStore', methods = ['GET'])
def search_store():
  list=[]
  req_Json= request.json
  store_name=req_Json['store_name']

  regex = ".*" + store_name + ".*"

  for result in db.storeOwner.find( {"storeName" : {'$regex' : regex, "$options":"i"}},{"storeName":1, "image":1} ):
      list.append(result)
  print(list)
  return json.dumps(list, indent=4, default = json_util.default)
###########################################################################################

@app.route('/storeDetail', methods = ['GET'])
def view_store():
    list=[]
    data = db.storeOwner
    req_Json= request.json
    ID=req_Json['ID']
    result = data.find_one({'_id':ObjectId(ID)},{'_id':0,"email":0, "password":0})
    print(result)

    for result1 in db.product.find({"store_id":ObjectId(ID)},{"store_id":0}):
      list.append(result1)
    print(list)
    return json.dumps( (result,list) , indent=4, default=json_util.default)
###########################################################################################

@app.route('/getAllStores', methods = ['GET'])
def view_all_stores():
    list=[]
    data = db.storeOwner

    
    for result in data.find({},{ 'email':0 , 'contacts':0, 'location':0, 'password':0, 'products':0}):
      list.append(result)
    print(list)
    return json.dumps(list, indent=4, default=json_util.default)
###########################################################################################
list0=[]
def dist(  long1, lat1 , long2, lat2):
      dlon= long2 - long1
      dlat= lat2 - lat1
      a= sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
      c= 2 * asin(sqrt(a))
      km= 6371 * c
      return(km) 

      
@app.route('/', methods = ['GET'])
def loc():
    data = db.storeOwner
    req_Json= request.json
    long1=req_Json['long1']
    lat1=req_Json['lat1']
    
    #result = []
    for result in data.find({ },{'_id':0, 'long':1, 'lat':1}):
      myList=result.values()
      long2 = list(myList)[0]
      lat2  = list(myList)[1]
      result= dist (long1, lat1, long2, lat2 ) 
      list0.append(result)
      list0.sort()

    print (list0[0:6])
    return json.dumps(list0[0:6], indent=4, default=json_util.default)