from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, List, Dict, Literal , Optional
import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the Patient", examples=["Mohan", "Rohit"])]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(gt=0, le=100, strict=True, description="Age of the Patient", examples=[45])]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(gt=0, description="Height of the patient (in meters)")]
    weight: Annotated[float, Field(gt=0, description="Weight of the patient (in kg)")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight) / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"      # BUG FIXED: was returning "Normal"
        else:
            return "Obese"
        

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str] , Field(default=None)]
    city : Annotated[Optional[str] , Field(default=None)]
    age : Annotated[Optional[int] , Field(default=None , gt = 0 , lt=100 , strict=True)]
    gender : Annotated[Optional[Literal["male" , "female" , "others"]] , Field(default=None)]
    height : Annotated[Optional[float] , Field(default=None , gt = 0)]
    weight : Annotated[Optional[float] , Field(default=None , gt = 0)]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def root():
    return {
        "message": "Patients Condition Management"
    }

@app.get("/about")
def about():
    return {
        "message": "This app is made by FASTAPI in json format"
    }

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient_id(patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient Not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight and BMI"),
    order: str = Query('asc', description="Sort in ascending/descending order")
):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select between asc and desc")

    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=409, detail="Patient Already existed")  # BUG FIXED: 400 -> 409

    # BUG FIXED: patient_id -> patient.id, "Id" -> "id"
    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


#Update --> edit --> patient id , weight , city , name 
#here put is used
#here we bulid a new pydantic model -- ham yahan pr purana wala pydantic model use nhi kr skte hai because hamko patient ki saari details daalni hogi jo mandatory hai , to ham naya pydantic model banayenge jo optional agar user sirf patient ki city change krna chahta hai to sirf vahin change ho aur kuch bhi na change ho


@app.put("/edit/{patient_id}")
def update_patient(patient_id : str , patient_update : PatientUpdate):

    #load the data 
    data = load_data()

    #check patient id in data or not 
    if patient_id not in data :
        raise HTTPException(status_code= 404 , detail="Patient Id not found")
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True) #ye sirf vo data store kregi jo data change hua

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi -> verdict -> pydantic object -> dict 
    existing_patient_info['id'] = patient_id #here patient id will be added
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_object.model_dump(exclude={'id'})

    #add this dictionary to data
    data[patient_id] = existing_patient_info

    #save data
    save_data(data)

    return JSONResponse(status_code=200 , content={"message" : "patient updated"})



#delete route/end point (to delete a particular patient data) --> we only give patient_id to delete the patient from the data 
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):

    #First load the data 
    data = load_data()

    if patient_id not in data :
        raise HTTPException(status_code=404 , detail="Patient Id not found.")
    
    del data[patient_id] #delete the patient id 

    save_data(data)
    return JSONResponse(status_code=200 , content={"message" : "Patient deleted successfully."})





