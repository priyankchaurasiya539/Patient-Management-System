from pydantic import BaseModel , EmailStr  , AnyUrl , Field , field_validator ,model_validator , computed_field #It is used for the data validation
from typing import List , Dict , Optional , Annotated

#Why we use pydantic -- > It solved two big problem 1. Clear error messages 2. Data validation problem 3.Nested data validation 4 . ML config management

#Pydantic model and schema is defined
class Patient(BaseModel):
    name : Annotated[str , Field(max_length=50 , title="Name of the patient" , description="Put the patient name less than in 50 characters" , examples = ["Nitish" , "Amrit"])]                    #here Field -- > Any user cannot put the name who has length greater than 50
    email : EmailStr                                        #it will handle the email input like standard way of putting email @gmail.com-----
    linkedin_url : AnyUrl                                   #it will handle the URL input like standard way of putting URL http//anrene//38-----
    age : Annotated[int , Field( gt=0 , lt=100 , strict=True)]
    weight : Annotated[float , Field(gt = 0 , strict=True)]        # here Field help that any user cannot put the weight less than zero(gt = greater than and lt = lessthan) , strict --> means it only accepts float values not "75.2" and not 75.2
    height : Annotated[float , Field(gt = 0 , lt=200)]

    married : Annotated[bool , Field(default=None , description="Is the patient married or not")]
    allergies : Optional[List[str]] = None  #we use this syntax because we are telling that list contains the elements as string  #if a user does not have any allergies then he/she cannot put any data in allegeries and in final result none is printed

    contact_details : Dict[str , str]   #we use this syntax because we are telling that dict contains the elements as string , string

    @computed_field
    @property
    def bmi(self) -> float :       #means we want answer in float
        bmi = round((self.weight)/(self.height ** 2 ) , 2 ) 
        return bmi


    @model_validator(mode="after")  #we do not have to give input of names , because we are apply model_validator to the whole model
    def validate_emergency_contact(cls , model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("Patients older than 60 must have emergency contact details")
        return model

    @field_validator("email")  #We have to apply field validator at email string
    @classmethod
    def email_validator (cls , value):
        valid_domains = ["hdfc.ac.in" , "icici.ac.in"]
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains :
            raise ValueError ("Not a valid domain.")
        return value
    
    #We use field validator for the name as well that we always say the user to put the patient name in capital letter

    @field_validator("name")
    @classmethod
    def name_validator(cls , value):
        upper_name = value.upper()
        return upper_name



def insert_patient_data (patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("BMI : " , patient.bmi)
    
    print("Data is inserted into the database.")

    

patient_info = {
    "name" : "Priyank Chaurasiya" ,
    "email" : "priyank.20257031@hdfc.ac.in" , 
    "linkedin_url" : "http://linkedin.com//123",
    "age" : 75 ,
    "weight" : 90.8 , 
    "height" : 150.2 ,
    "married" : True , 
    "allergies" : ["pollen" , "dust" , "smoke"] , 
    "contact_details" : { "phone_number" : "8726352463" , "emergency" : "787445515"} 
    }
patient1 = Patient(**patient_info)

insert_patient_data(patient1)


"""Field Validator(it is class method) -- > It is used to validate that we are providing our services to selected clients . Ex. If our hospital is tie up with a bank name HDFC bank , then we have to ensure that only hdfc bank employees should use our services. And we can validate this by modify email string , we must provide services those employees whose email ends with @hdfc.ac.in"""

"""Model Validator -- > It is used when we want to conditions to satisfy that if we want the people have age >= 60 then there must be a emergency contact details to fill. It can combines multiple field validator"""


