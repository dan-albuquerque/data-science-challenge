"""Endpoint para cálculo de Performance."""
from fastapi import APIRouter, HTTPException, Request
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import roc_auc_score

router = APIRouter(prefix="/performance")

with open("monitoring/model.pkl", "rb") as f:
    model = pickle.load(f)

@router.post("/")
async def evaluate_performance(request: Request):
    try:
        body = await request.json()
        # se o body for lista direta
        if isinstance(body, list):
            records = body
        else:
            records = body.get("records")

        if not records:
            raise HTTPException(status_code=400, detail="Body deve conter lista de registros ou chave 'records'.")

        df = pd.DataFrame(records)
        df = df.replace({None: np.nan})

        if "REF_DATE" not in df.columns or "TARGET" not in df.columns:
            raise HTTPException(status_code=400, detail="Registros devem conter 'REF_DATE' e 'TARGET'")

        # volumetria
        df["REF_DATE"] = pd.to_datetime(df["REF_DATE"])
        volumetria = df.groupby(df["REF_DATE"].dt.to_period("M")).size().to_dict()

        # performance
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
