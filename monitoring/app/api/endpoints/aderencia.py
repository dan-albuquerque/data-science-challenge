"""Endpoint para cálculo de aderência."""
from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import pickle
from scipy.stats import ks_2samp

router = APIRouter(prefix="/aderencia")

# Carrega modelo
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@router.post("/")
def evaluate_aderencia(body):
    try:
        dataset_path = body.get("dataset_path")
        if not dataset_path:
            raise HTTPException(status_code=400, detail="É necessário fornecer 'dataset_path' no body da requisição")
        
        # Carrega dataset fornecido
        df_new = pd.read_csv(dataset_path, compression="gzip")
        df_new = df_new.replace({None: np.nan})
        
        # Carrega dataset de teste
        df_test = pd.read_csv("monitoring/model.pkl", compression="gzip")

        # Gera scores (ignora coluna 'TARGET' se existir)
        scores_new = model.predict_proba(df_new.drop(columns=["TARGET"], errors="ignore"))[:, 1]
        scores_test = model.predict_proba(df_test.drop(columns=["TARGET"], errors="ignore"))[:, 1]

        # Teste KS
        ks_stat, p_value = ks_2samp(scores_new, scores_test)
        
        return {
            "ks_statistic": float(ks_stat),
            "p_value": float(p_value)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))