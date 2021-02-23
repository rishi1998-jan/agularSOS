from service.models import Student
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains Student business logics.   
'''
class StudentService(BaseService):
    def search(self,params):
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_student where 1=1 "        
        rowSql="select count(ID) from sos_student where 1=1"
        

        val = params.get("firstName",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and firstName = '"+val+"' "
            rowSql+=" and firstName = '"+val+"' "
        
        val = params.get("email",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and email = '"+val+"' "
            rowSql+=" and email = '"+val+"' "
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
       
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","firstName","lastName","dob","mobileNumber","email","college_ID","collegeName")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

       

    def get_model(self):
        return Student
