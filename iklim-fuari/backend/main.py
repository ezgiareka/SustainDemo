from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal

app = FastAPI()

# Allow frontend requests from any origin during demo/development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculationRequest(BaseModel):
    transport: Literal["araba", "metro", "yuruyerek_bisiklet"]
    food: Literal["etli", "vegan"]
    drink: Literal["evet","hayir"]
    coffee:Literal["Termos","Tek Kullanimlik"]
    media: Literal["evet", "eglence_icin", "hayir"]
    cop: Literal["dikkatsiz", "sinirli", "sifir", "kompost"]
    trivia: Literal["areka", "sarmasik", "kaktus"]
    bm: Literal["5", "10", "17"]
    internetHours: int
    seyahat: Literal["hic", "az", "orta", "cok"]


TRANSPORT_EMISSIONS = {
    "araba": 1.71,
    "metro": 0.41,
    "yuruyerek_bisiklet": 0.00,
}

FOOD_EMISSIONS = {
    "etli": 13.30,
    "vegan": 2.00,
}

DRINK_EMISSIONS = {
    "evet": 0.50,
    "hayir": 0.00,
}

MEDIA_EMISSIONS = {
    "evet": 0.20,
    "eglence_icin": 0.50,
    "hayir": 0.00,
}

COFFEE_EMISSIONS = {
    "Termos": 0.10,
    "Tek Kullanimlik": 0.50,
}

COP_EMISSIONS = {
    "dikkatsiz": 2.5,
    "sinirli": 1.0,
    "sifir": 0.2,
    "kompost": 0.0,
}

TRIVIA_EMISSIONS = {
    "areka": 0.0,
    "sarmasik": 0.0,
    "kaktus": 0.0,
}

BM_ANSWERS = {
    "5": False,
    "10": False,
    "17": True,
}

def get_internet_emission(hours: int) -> float:
    if hours <= 2:
        return 0.1
    elif hours <= 6:
        return 0.3
    elif hours <= 10:
        return 0.7
    else:
        return 1.2

TRAVEL_EMISSIONS = {
    "hic": 0.0,
    "az": 1.5,
    "orta": 4.0,
    "cok": 9.0,
}


@app.post("/calculate")
def calculate_emission(payload: CalculationRequest):
    transport_emission = TRANSPORT_EMISSIONS[payload.transport]
    food_emission = FOOD_EMISSIONS[payload.food]
    drink_emission = DRINK_EMISSIONS[payload.drink]
    coffee_emission = COFFEE_EMISSIONS[payload.coffee]
    media_emission = MEDIA_EMISSIONS[payload.media]
    cop_emission = COP_EMISSIONS[payload.cop]
    trivia_emission = TRIVIA_EMISSIONS[payload.trivia]
    is_un_correct = BM_ANSWERS[payload.bm]
    internet_emission = get_internet_emission(payload.internetHours)
    travel_emission = TRAVEL_EMISSIONS[payload.seyahat]

    total_emission = transport_emission + food_emission + drink_emission + coffee_emission + media_emission + cop_emission + trivia_emission + internet_emission + travel_emission
    is_eco_friendly = total_emission < 5.0

    return {
        "emission": total_emission,
        "is_eco_friendly": is_eco_friendly,
    }
