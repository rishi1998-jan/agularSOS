


from service.models import Course
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains Course business logics.   
'''
class CourseService(BaseService):
   
    def search(self,params):
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_course where 1=1 "        
        rowSql="select count(ID) from sos_course where 1=1"
        

        val = params.get("courseName",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and courseName = '"+val+"' "
            rowSql+=" and courseName = '"+val+"' "
        
        val = params.get("coursDescription",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and coursDescription = '"+val+"' "
            rowSql+=" and coursDescription = '"+val+"' "
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
        
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","courseName","coursDescription","coursDuration")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

        

    def get_model(self):
        return Course
