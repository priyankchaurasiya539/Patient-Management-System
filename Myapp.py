from pydantic import BaseModel , Field , field_validator , EmailStr , model_validator
from typing import List , Dict , Annotated , Optional

class Patient(BaseModel):
    name : Annotated[str , Field (max_length=50 , title="Put the name here" , description="Name should be less than 50 characters" , examples=["Nitish" , "Aman"] )]
    email : EmailStr
    age : Annotated[int , Field(gt = 0 , lt=100 , description="Put the age here" , examples=42 , strict=True)]
    married : Annotated[bool , Field(default=None)]
    allergies : List[str]
    contact_details : Dict[str , str]

    @model_validator(mode="after")
    def validate_emergency_contact(cls , model):
        if model.age > 75 and "emergency" not in model.contact_details:
            raise ValueError("Patients older than 60 must have emergency contact details")
        return model

    @field_validator("name")
    @classmethod
    def name_validator(cls , value):
        capital_name = value.upper()
        return capital_name
    
    @field_validator("email")
    @classmethod
    def email_validator(cls , value):
        valid_domains = ["hdfc.ac.in" , "icici.ac.in" , "sbi.ac.in"]
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains :
            raise ValueError("Not a valid user")
        return value


def insert_patient_data(patient : Patient):
    print(patient.name)
    print(patient.email)
    print(patient.contact_details)
    print("Data is updated successfully.")

patient_info = {
    "name" : "Priyank Chaurasiya",
    "email" : "priyank.20257031@sbi.ac.in" , 
    "age" : 88 , 
    "married" : True , 
    "allergies" : ["dermatitis" , "smoke" , "dust"],
    "contact_details" : {"phone_number" : "8726352463" , "emergency" : "46551658"}
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)
