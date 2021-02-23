


from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import MarksheetForm
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService

class MarksheetListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["rollNumber"]=requestForm.get("rollNumber",None)
        self.form["name"]=requestForm.get("name",None)
        self.form["physics"]=requestForm.get("physics",None)
        self.form["chemistry"]=requestForm.get("chemistry",None)
        self.form["maths"]=requestForm.get("maths",None)
        self.form["student_ID"]=requestForm.get("student_ID",None)
        self.form["ids"]= requestForm.getlist( "ids", None)

    def display(self,request,params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list})
        return res

    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list, "form":self.form})
        return res
        
    def get_template(self):
        return "ors/MarksheetList.html"          

    # Service of Marksheet     
    def get_service(self):
        return MarksheetService()        

    def deleteRecord(self,request,params={}):
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list})
        if(bool(self.form["ids"])==False):
           
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
           
            for ids in self.form["ids"]:
                self.page_list = self.get_service().search(self.form)
                id=int(ids)
                if( id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form["error"] = False
                        self.form["message"] = "Data is successfully deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
                    else:
                        self.form["error"] = False
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res



