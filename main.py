from fastapi import FastAPI

app = FastAPI(
    title="ProcessDebt API",
    description="Sistema de análise de ineficiência operacional.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Bem-vindo ao ProcessDebt API!"
    }