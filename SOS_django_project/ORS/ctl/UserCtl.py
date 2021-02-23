


from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage
from datetime import datetime
from django.utils.dateparse import parse_date

class UserCtl(BaseCtl):
    def preload(self,request):
        self.page_list = RoleService().search(self.form)
        self.preloadData=self.page_list

    #Populate Form from HTTP Request 
    def request_to_form(self,requestForm):
        newdate=""
        if(requestForm["dob"]):
            formDate=requestForm["dob"].replace("/", "-")
            newdate=datetime.strptime(formDate,'%m-%d-%Y').strftime('%Y-%m-%d')
        self.form["id"]  = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] =newdate
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] =requestForm["role_Id"]

    #Populate Form from Model 
    def model_to_form(self,obj):

        if (obj == None):
            return
        self.form["id"]  = obj.id 
        self.form["firstName"] = obj.firstName 
        self.form["lastName"] = obj.lastName 
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password 
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = obj.role_Id
        self.form["role_Name"] = obj.role_Name


    #Convert form into module
    def form_to_model(self,obj):
        c = RoleService().get(self.form["role_Id"])
        pk = int(self.form["id"])
        newdate=""
       
        if(pk>0): 
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id = self.form["role_Id"]
        
        obj.role_Name=c.name
        return obj

    #Validate form 
    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
            
        if(DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "confirmpassword can not be null"
            self.form["error"] = True   

        if(DataValidator.isNotNull(self.form["confirmpassword"])):
            if(self.form["password"] != self.form["confirmpassword"]):
                inputError["confirmpassword"] = "Password and confirm Password are not Same"
                self.form["error"] = True    
             
        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["address"])):
            inputError["address"] = "address can not be null"
            self.form["error"] = True    
        if(DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "mobileNumber can not be null"
            self.form["error"] = True
      
      
        return self.form["error"]        

    #Display Role page 
    def display(self,request,params={}):
        if( params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(), {"form":self.form,"roleList":self.preloadData})
        return res

   
    def submit(self,request,params={}):
        duplicat=self.get_service().get_login_id(self.form["login_id"])

        if(duplicat.count()>0):
            self.form["error"] = True
            self.form["message"] = "User is already exist, Please register with another mail id"
            res = render(request,self.get_template(),{"form":self.form})            
        else:
            user = request.session.get("user",None)
            emsg=EmailMessage()
            emsg.to= [self.form["login_id"]]
            e={}
            e["login"]= self.form["login_id"]
            e["password"]=self.form["password"]
            emsg.subject= "ORS Registration Successful"    
            mailResponse=EmailService.send(emsg,"signUp",e)           
            if(mailResponse==1):
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "You have registered successfully"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Please Check Your Internet Connection"
                res = render(request,self.get_template(),{"form":self.form})
        return res 

    def get_template(self):
        return "ors/User.html"  

    # Service of Role     
    def get_service(self):
        return UserService()        
