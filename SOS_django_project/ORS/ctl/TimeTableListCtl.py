
 
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import TimeTableForm
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService

class TimeTableListCtl(BaseCtl):

    def request_to_form(self,requestForm):
        self.form["examTime"]=requestForm.get("examTime",None)
        self.form["examDate"]=requestForm.get("examDate",None)
        self.form["subject_ID"]=requestForm.get("subject_ID",None)
       
        self.form["course_ID"]=requestForm.get("course_ID",None)
       
        self.form["semester"]=requestForm.get("semester",None)
        self.form["ids"]= requestForm.getlist( "ids", None)

    def display(self,request,params={}):
        self.page_list = self.get_service().search(self.form)
        courseList=CourseService().search(self.form)
        subject_List = SubjectService().search(self.form)
        for x in self.page_list: 
            for y in courseList: 
                if x.course_ID==y.id:
                    x.courseName=y.courseName 
            for z in subject_List:               
               if x.subject_ID==z.id:
                   x.subjectName=z.subjectName
        res = render(request,self.get_template(), {"form":self.form,"courseList":courseList,"subjectList":subject_List ,"page_list":self.page_list})
        return res
    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        self.page_list = self.get_service().search(self.form)
        res = render(request,self.get_template(),{"pageList":self.page_list, "form":self.form})
        return res
        
    def get_template(self):
        return "ors/TimeTableList.html"          

    # Service of Marksheet     
    def get_service(self):
        return TimeTableService()        

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
                        self.form["error"] = True
                        self.form["message"] = "Data is not delete"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res



