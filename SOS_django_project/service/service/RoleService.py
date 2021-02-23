from service.models import Role
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import models, connection

'''
It contains Role business logics.   
'''
class RoleService(BaseService):

    def search(self,params):
        params["pageNo"]=(params["pageNo"]-1)*self.pageSize
        sql="select * from sos_role where 1=1 "        
        rowSql="select count(ID) from sos_role where 1=1"
        

        val = params.get("name",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and name = '"+val+"' "
            rowSql+=" and name = '"+val+"' "
        
        val = params.get("description",None)
        if( DataValidator.isNotNull(val)):
            sql+=" and description = '"+val+"' "
            rowSql+=" and description = '"+val+"' "
        
        sql+=" LIMIT %s,%s"
        rowSql+=" LIMIT %s,%s"
        cursor = connection.cursor()
       
        cursor.execute(sql,[params["pageNo"],self.pageSize])
        result=cursor.fetchall()
        test_tup1=("id","name","description")
        res={
            "data":[],
            "count":[]
        }
        count=0
        for x in result:
            res["data"].append({test_tup1[i] :  x[i] for i, _ in enumerate(x)})            
        return res 
       

    def get_model(self):
        return Role
