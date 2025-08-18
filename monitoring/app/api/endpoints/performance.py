"""Endpoint para cálculo de Performance."""
from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import roc_auc_score
from datetime import datetime

router = APIRouter(prefix="/performance")

# Carrega modelo já na inicialização
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@router.post("/")
def evaluate_performance(records):
    try:
        # Converte para DataFrame
        df = pd.DataFrame(records)
        
        # Trata nulos
        df = df.replace({None: np.nan})
        
        # Garante que tem a coluna de data e alvo
        if "REF_DATE" not in df.columns or "TARGET" not in df.columns:
            raise HTTPException(status_code=400, detail="Registros devem conter 'REF_DATE' e 'TARGET'")
        
        # Volumetria por mês
        df["REF_DATE"] = pd.to_datetime(df["REF_DATE"])
        volumetria = df.groupby(df["REF_DATE"].dt.to_period("M")).size().to_dict()
        
        # Performance (AUC-ROC)
        X = df.drop(columns=["TARGET", "REF_DATE"])
        y = df["TARGET"]
        y_pred = model.predict_proba(X)[:, 1]
        auc = roc_auc_score(y, y_pred)
        
        return {
            "VOLUMETRIA_MENSAL": {str(k): int(v) for k, v in volumetria.items()},
            "AUC_ROC": auc
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
