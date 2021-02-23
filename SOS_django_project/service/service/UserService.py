

from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains User business logics.   
'''
class UserService(BaseService):

    def authenticate(self,params):
        userList = self.search(params) 
        if (userList.count() == 1):
            return userList[0]
        else:
            return None
     
    def search(self,params):
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_user where 1=1 "        
        rowSql="select count(ID) from sos_user where 1=1"
        

        val = params.get("firstName",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and firstName = '"+val+"' "
            rowSql+=" and firstName = '"+val+"' "
        
        val = params.get("login_id",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and login_id = '"+val+"' "
            rowSql+=" and login_id = '"+val+"' "
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
       
      
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","firstName","lastName","login_id","password","confirmpassword","dob","address","gender","mobilenumber","role_Id","role_Name")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

      

    def get_login_id(self,login):
        q = self.get_model().objects.filter()
        if( DataValidator.isNotNull(login)):
            q= q.filter( login_id = login)           
        return q
        


    def get_model(self):
        return User
