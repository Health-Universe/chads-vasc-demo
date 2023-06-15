from model import chads_vasc_score

# Import FastAPI
from fastapi import FastAPI

# App Instance
app = FastAPI()

# Decorate Function
@app.get("/")
def run(age: int = 65, female: bool = True, chf: bool = False, hypertension: bool = False, stroke_tia: bool = False, vascular_disease: bool = False, diabetes: bool = False) -> int:
    score =  chads_vasc_score(age=age, 
                    female=female, 
                    chf=chf, 
                    hypertension=hypertension,
                    stroke_tia=stroke_tia, 
                    vascular_disease=vascular_disease, 
                    diabetes=diabetes)
    return f"CHA₂DS₂-VASc Score: {score}"