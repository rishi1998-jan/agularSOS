from service.models import Marksheet
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains Role business logics.   
'''
class MarksheetService(BaseService):

    def search(self,params):
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_marksheet where 1=1 "        
        rowSql="select count(ID) from sos_marksheet where 1=1"
        

        val = params.get("rollNumber",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and rollNumber = '"+val+"' "
            rowSql+=" and rollNumber = '"+val+"' "
        
        val = params.get("name",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and name = '"+val+"' "
            rowSql+=" and name = '"+val+"' "
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
       
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","rollNumber","name","physics","chemistry","maths")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

       

    def get_model(self):
        return Marksheet
