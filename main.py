from model import chads_vasc_score

# Import FastAPI
from fastapi import FastAPI

# App Instance
app = FastAPI()

# Decorate Function
@app.post("/")
def run(age: int, female: bool, chf: bool, hypertension: bool, stroke_tia: bool, vascular_disease: bool, diabetes: bool) -> int:
    chads_vasc_score(age=age, 
                    female=female, 
                    chf=chf, 
                    hypertension=hypertension,
                    stroke_tia=stroke_tia, 
                    vascular_disease=vascular_disease, 
                    diabetes=diabetes)