

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Faculty
from service.forms import FacultyForm
from service.service.FacultyService import FacultyService
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from datetime import datetime
from django.utils.dateparse import parse_date

class FacultyCtl(BaseCtl):
    def preload(self,request):
        self.course_List = CourseService().search(self.form)
        self.college_List = CollegeService().search(self.form)
        self.subject_List = SubjectService().search(self.form)
        

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        newdate=""
        if(requestForm["dob"]):
            formDate=requestForm["dob"].replace("/", "-")
            newdate=datetime.strptime(formDate,'%m-%d-%Y').strftime('%Y-%m-%d')
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["email"] = requestForm["email"]
        self.form["password"] = requestForm["password"]
        
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["dob"] =newdate
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["subject_ID"] = requestForm["subject_ID"]
       
        self.form["course_ID"] = requestForm["course_ID"]
       

    # Populate Form from Model
    def model_to_form(self, obj):
       
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["email"] = obj.email
        self.form["password"] = obj.password
      
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["dob"] = obj.dob
        self.form["college_ID"] = obj.college_ID
        self.form["subject_ID"] = obj.subject_ID
        # self.form["subjectName"] = obj.subjectName
        self.form["course_ID"] = obj.course_ID
       

    # Convert form into module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        e = CollegeService().get(self.form["college_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id= pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.email = self.form["email"]
        obj.password = self.form["password"]
       
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.dob = self.form["dob"]
        obj.college_ID = self.form["college_ID"]
        obj.subject_ID= self.form["subject_ID"]
       
        obj.course_ID = self.form["course_ID"]
       
        obj.courseName=c.courseName
        obj.collegeName=e.collegeName 
        obj.subjectName=s.subjectName 
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "lastName can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["email"])):
            inputError["email"] = "email can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "password can not be null"
            self.form["error"] = True

        

        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "gender can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "college_ID can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "subject_ID can not be null"
            self.form["error"] = True

       

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "course_ID can not be null"
            self.form["error"] = True

        
        return self.form["error"]

    
    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form":self.form,"courseList":self.course_List,"collegeList":self.college_List,"subjectList":self.subject_List })
        return res

   
    def submit(self, request, params={}):
        r = self.form_to_model(Faculty())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is successfully saved"
        res = render(request,self.get_template(),{"form":self.form})
        return res

    # Template html of Role page
    def get_template(self):
        return "ors/AddFaculty.html"

    # Service of Role

    def get_service(self):
        return FacultyService()