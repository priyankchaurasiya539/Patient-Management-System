from pydantic import BaseModel

class Address(BaseModel):
    city : str 
    state : str 
    pincode : int

class Patient(BaseModel):

    name : str
    gender : str
    age : int 
    address : Address

address_dict = {
    "city" : "Gurgaon",
    "state" : "Haryana",
    "pincode" : 211001
}

address1 = Address(**address_dict)
patient_dict = {
    "name" : "Priyank Chaurasiya",
    "gender" : "Male",
    "age" : 45,
    "address" : address1
}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.address)
print(patient1.address.pincode)


#we can export pydantic models to json format and dictionery format

temp = patient1.model_dump_json(include=['name' , 'address'])
print(temp)
print(type(temp))