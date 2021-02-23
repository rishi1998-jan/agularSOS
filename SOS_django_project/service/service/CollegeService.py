


from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains Role business logics.   
'''
class CollegeService(BaseService):

    def search(self, params):       
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_college where 1=1 "        
        rowSql="select count(ID) from sos_college where 1=1"
        
        val = params.get("collegeName",None)
        if( DataValidator.isNotNull(val)):
            sql+="and collegeName = '"+val+"' "
            rowSql+="and collegeName = '"+val+"' "
        
        val = params.get("collegeAddress",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and collegeAddress = '"+val+"' "
            rowSql+=" and collegeAddress = '"+val+"'"
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","collegeName","collegeAddress","collegeState","collegeCity","collegePhoneNumber")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 

      
    def get_model(self):
        return College
