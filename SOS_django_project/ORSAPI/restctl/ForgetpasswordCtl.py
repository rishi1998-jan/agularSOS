
  

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.forms import UserForm
from service.service.UserService import UserService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage

from django.http.response import JsonResponse
import json


class ForgetpasswordCtl(BaseCtl): 
    def get(self,request, params = {}):
        pass

    def delete(self,request, params = {}):
        pass

    def search(self,request, params = {}):
        json_request=json.loads(request.body)
        if(json_request):
            params["login_id"]=json_request.get("login_id",None)
        
        service=UserService()
        c=service.search(params)
        res={} 
        data=[]
        for x in c:
            data.append(x.to_json())
        if(c!=None):
            res["data"]=data
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res})

    def form_to_model(self,obj,request):
       pass
    def request_to_form(self,requestForm):
        self.form["login_id"]  = requestFrom["login_id"]
    
    def save(self,request, params = {}):
        json_request=json.loads(request.body)

        self.request_to_form(json_request) 
        emsg=EmailMessage()
        emsg.to= [self.form["login_id"]]
        e={}
        e["login"]= self.form["login_id"]
        e["password"]=self.form["password"]
        emsg.subject= "ORS Registration Successful"    
      
        mailResponse=EmailService.send(emsg,"signUp",e)  
        r=self.form_to_model(User(), json_request)
        service=UserService()
        c=service.save(r)
        res={}
       
        if(mailResponse==1):
            res["data"]=r.to_json()
            res["error"]=False
            res["message"]="Data is Successfully saved"
           
        else:
            res["error"]=True
            res["message"]="Data is not saved"
        return JsonResponse({"data":res})

     #  def submit(self,request,params={}):
    #     if(self.input_validation()):
    #         return render(request,self.get_template(),{"form":self.form})
    #     else:     
    #         q= User.objects.filter( login_id = self.form["login_id"])
    #         userList=""
    #         for userData in q:
    #             userList=userData
    #         if(userList!=""):
    #             emsg=EmailMessage()
    #             emsg.to= [userList.login_id]
    #             emsg.subject= "Forget Password"
    #             mailResponse=EmailService.send(emsg,"forgotPassword",userList)
    #             if(mailResponse==1):
    #                 self.form["error"] = False
    #                 self.form["message"] = "Please check your mail, Your password is send successfully"
    #                 res = render(request,self.get_template(),{"form":self.form})
    #                 request.session["user"] = userList
    #                 res = render(request,self.get_template(),{"form":self.form})
    #             else:
    #                 self.form["error"] = True
    #                 self.form["message"] = "Please Check Your Internet Connection"
    #                 res = render(request,self.get_template(),{"form":self.form})
    #         else:
    #             self.form["error"] = True
    #             self.form["message"] = "login id is not correct"
    #             res = render(request,self.get_template(),{"form":self.form})

        
    #     return res        
    

      
    def get_template(self):
        return "orsapi/User.html"          

        
    def get_service(self):
        return UserService()    


   


       



