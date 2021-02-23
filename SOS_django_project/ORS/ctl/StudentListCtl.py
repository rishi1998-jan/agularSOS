from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import StudentForm
from service.models import Student
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService

class StudentListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        print("ors studentlist request to form is run") 
        self.form["firstName"]=requestForm.get("firstName",None)
        self.form["lastName"]=requestForm.get("lastName",None)
        self.form["dob"]=requestForm.get("dob",None)
        self.form["mobileNumber"]=requestForm.get("mobileNumber",None)
        self.form["email"]=requestForm.get("email",None)
        self.form["college_ID"]=requestForm.get("college_ID",None)
        self.form["collegeName"]=requestForm.get("collegeName",None)
        self.form["ids"]= requestForm.getlist( "ids", None)

    def display(self,request,params={}):
        print("ors studentlist display is run")
        self.page_list = self.get_service().search(self.form)
        collegeList=CollegeService().search(self.form)
        
        for x in self.page_list: 
            for y in collegeList:
                if x.college_ID==y.id:
                    print("ddddd----------->",x.college_ID==y.id)
                    x.collegeName=y.collegeName
        res = render(request,self.get_template(),{"pageList":self.page_list})
        return res

    def submit(self,request,params={}):
        print("ors studentlist submit is run")
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list, "form":self.form})
        return res
        
    def get_template(self):
        return "ors/StudentList.html"          

    # Service of Marksheet     
    def get_service(self):
        return StudentService()        

    def deleteRecord(self,request,params={}):
        print("ors studentlist delete record is run") 
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
                        res = render(request,self.get_template(),{"pageList":self.page_list ,"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not delete"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res