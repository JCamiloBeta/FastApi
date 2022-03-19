#Python
from msilib.schema import Patch
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI, Body, Query, Path

app= FastAPI()

#Models

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}    

# Rquest and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
     # El ... para hacerlo obligatorio, no recomendado en un Query parameter
    age: int = Query(
        ...,
        title= "Person Age",
        description= "This is the person age. It's required"
        )
):
    return {name: age}

    '''
    Funcion para probar la validacion en los query parameter.
    El Age esta obligatorio, no se recomienda hacer esto, si necesitas un
    parametro obligatorio se recomienda hacerlo en un path parameter
    '''

# Validaciones: Path Parametros
    
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title= "Detail Person",
        description= "This is the detail person."
        )
    ):
        return  {person_id: "It exists!"}


# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Personal ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
