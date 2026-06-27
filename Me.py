from fastapi import FastAPI , Path , HTTPException , Query 
import json 
from pydantic import BaseModel , Field , computed_field , model_validator , field_validator
from typing import Annotated , List , Dict , Literal
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str , Field(... , description= "Put the patient id" , examples=["P001"])]
    name : Annotated[str , Field(... , description="Patient Name" , examples= ["Mohit , Nitish"])]
    city : Annotated[str , Field(... , description="Patient City" )]
    age : Annotated[int , Field(... , description="Patient's Age" , gt=0 , lt= 100 , strict=True)]
    gender : Annotated[Literal["male" , "female" , "others"] , Field(... , description="Patient gender")]
    height : Annotated[float , Field(... , description="Height of the Patient (in meters)" , gt=0 , lt=200)]
    weight : Annotated[float , Field(... , description="Weight of the Patient (in meters)")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(((self.weight)/(self.height * self.height)) , 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str :
        if self.bmi < 18.2:
            return "UnderWeight"
        elif self.bmi < 25 :
            return "Normal"
        
        elif self.bmi < 30 :
            return "OverWeight"
        
        else :
            return "Obese"

#load the data
def load_data():
    with open ("patients.json" , "r") as f :
        data = json.load(f)
    return data

#save the data 
def save_data(data):
    with open("patients.json" , "w") as f :
        json.dump(data , f)


@app.get("/")
def root():
    return {
        "message" : "Hello , Welcome to the world of api"
    }

@app.get("/about")
def about():
    return {
        "message" : "This is the patient management app."
    }


@app.get("/view")
def patient_data():
    data = load_data()
    return data

#get the patient info by putting the patient id 
@app.get("/patient/{patient_id}")
def patient_id_data(patient_id : str = Path(... , description="ID of the patient" , example="P001")):
    data = load_data()

    if patient_id in data :
        return data[patient_id] 
    raise HTTPException(status_code=404 , detail="Patien Not found")

#now its time to add new patient id

#create the end point --> post
#load the patient data
#check the patient data present in data 
#if not add them in the data

@app.post("/create")
def new_patient(patient : Patient):
    data = load_data()

    if patient.id in data :
        raise HTTPException(status_code=409 , detail="Patient already exist in the database")
    
    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=200 ,content={"message" : "Patient data created successfully"})


