


from service.models import Subject
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains Student business logics.   
'''
class SubjectService(BaseService):
    
    def search(self,params):
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_subject where 1=1 "        
        rowSql="select count(ID) from sos_subject where 1=1"
        

        val = params.get("subjectName",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and subjectName = '"+val+"' "
            rowSql+=" and subjectName = '"+val+"' "
        
        val = params.get("courseName",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and courseName = '"+val+"' "
            rowSql+=" and courseName = '"+val+"' "
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
       
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","subjectName","subjectDescription","course_ID")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

       
        

    def get_model(self):
        return Subject
