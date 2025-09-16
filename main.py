from fastapi import FastAPI,Path,HTTPException,Query
import json 
from pydantic import BaseModel , Field, computed_field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse
app = FastAPI()

# @app.get("/")
# def Hello():
#     return {'message' : 'Hello World'}

# @app.get('/about')
# def About():
#     return {'message': 'this is about page'}

def loadData():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get('/')
def Patient():
    return {'message': 'patient management system api'}

@app.get('/about')
def About():
    return {'message': 'fully functional api to manage your patient records '}

@app.get('/view')
def View():
    data = loadData()
    return data

# path params:
# path parameters are dynamic segments of a url used to identify a specific resource
# we use path from fastapi framework to enhance the readabilty , we can add data validation 
# used to provide metadata , validation ,rules and documentation hints for path parameters in ur api end points

@app.get('/patient/{patientId}')
def getPatient(patientId: str = Path(..., description="ID of the patient in the db" , examples="P001")):
    # load all the patients 
    data = loadData()
    if patientId in data:
        return data[patientId]  
    # return {'message': 'patient not found'}
    raise HTTPException(status_code=404 , detail="patient not found")

# http status code 
# http status codes are 3 digit numbers returned by a web sever (like fastAPI) to indicate the result of a 
# clients request (like from a browser or api consumer)

# they help the client (browser, frontend , mobile app , etc..) understand: 
# whether the req was succesfull 
# anything went wrong 
# what kind of issue occrued 

# 2XX success (the req was successfully received and procceseed)
# 3XX redirection (further action needs to be taken )
# 4XX cluent error (some thing went wrong with the req from the client)
# 5XX sevrr error (some thing went wrong on the server side )

# HTTPException is a spcl built in exception in fast api to return custom http error responses when comething goes wrong  in ur api 
# instead of returing normal json or crashthe servr , u can gracefully raise an error with 
# a proper http status code 
# a custom error message 


# query parameter 
# quesry parameter are optional key value pair appended to the end of a url used to pass additional data to server 
# in an http req, they are tyically emploted fr operations like filtering , sorting, searcing ,without altering the end point itself
# /patients?city=delhi&sort_by=age

# the ? marks the start of  query parameter 
# each parameter is a key value pair key=value 
# multiple paramters are separted by & 

# in this case:
# city=Delhi is a query parameter for filtering 
# sort_age =age is a query parameter for sorting 



# Qrery is a utilituy fn provided by FastAPi to declare and docuent query parameters in ur api end point 

@app.get('/sort')
def sortPatients(sort_by: str = Query(..., description="sort on the basis of height , weight and bmi"), order:str = Query(...,description='sort in asc or dec order')):
    valid_field  = ['height', 'weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"invalid field select from {valid_field}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = loadData()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property 
    def bmi(self) ->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property 
    def verdict(self)->str:
        if (self.bmi < 18.5):
            return 'Under Weight'
        elif (self.bmi<25):
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data,f)

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = loadData()


    # check if patient already exists 
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # if already exists , then add 
    data[patient.id]= patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={"message": "pateint created succesfully"})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str , patient_update: PatientUpdate):
    data = loadData()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient id not found")
    
    existing_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_info[key] = value 

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_info['id'] =patient_id
    patient_pydantic_obj = Patient(**existing_info)
    #-> pydantic object -> dict
    existing_info = patient_pydantic_obj.model_dump(exclude='id')


    data[patient_id] = existing_info

    save_data(data) 

    return JSONResponse(status_code=200, content={'message':'patient updated'})



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = loadData()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})