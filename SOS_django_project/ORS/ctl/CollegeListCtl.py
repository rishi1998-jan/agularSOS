

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CollegeForm
from service.models import College
from service.service.CollegeService import CollegeService


class CollegeListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        print("ors colllegelist request to form is run")
        self.form["collegeName"] = requestForm.get("collegeName", None)
        self.form["collegeAddress"] = requestForm.get("collegeAddress", None)
        self.form["collegeState"] = requestForm.get("collegeState", None)
        self.form["collegeCity"] = requestForm.get("collegeCity", None)
        self.form["collegePhoneNumber"] = requestForm.get("collegePhoneNumber", None)
        self.form["ids"]= requestForm.getlist( "ids", None)
       
    def display(self, request, params={}):
        print("ors colllegelist display is run")
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {"pageList": self.page_list,"no":0})
        return res

    def submit(self, request, params={}):
        print("ors colllegelist submit is run")
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def get_template(self):
        return "ors/CollegeList.html"

        # Service of College
 
    def get_service(self):
        return CollegeService()

    def deleteRecord(self,request,params={}):
        print("ors colllegelist delete is run")
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
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

