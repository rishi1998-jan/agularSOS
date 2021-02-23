



from service.models import Faculty
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Student business logics.
'''
class FacultyService(BaseService):
    def search(self,params):
        q = self.get_model().objects.filter()

        val = params.get("firstName",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( firstName = val)

        val = params.get("lastName",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( lastName = val)

        val = params.get("email",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( email = val)

        val = params.get("password",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( password = val)

        val = params.get("mobileNumber",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( mobileNumber = val)

        val = params.get("address",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( address = val)

        val = params.get("gender",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( gender = val)

        val = params.get("dob",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( dob = val)



        val = params.get("college_ID",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( college_ID = val)

        val = params.get("collegeName",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( collegeName = val)   

        val = params.get("subject_ID",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( subject_ID = val)

        val = params.get("subjectName",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( subjectName = val)

        val = params.get("course_ID",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( course_ID = val)

        val = params.get("courseName",None)
        if( DataValidator.isNotNull(val)):
           q= q.filter( courseName = val)
        return q

    def get_model(self):
        return Faculty