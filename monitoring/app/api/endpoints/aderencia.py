"""Endpoint para cálculo de aderência."""
from fastapi import APIRouter, HTTPException, Request
import pandas as pd
import numpy as np
import pickle
from scipy.stats import ks_2samp

router = APIRouter(prefix="/aderencia")

with open("monitoring/model.pkl", "rb") as f:
    model = pickle.load(f)

# with open("monitoring/my_model.pkl", "rb") as f:
#     my_model = pickle.load(f)

@router.post("/")
async def evaluate_aderencia(request: Request):
    try:
        body = await request.json()
        dataset_path = body.get("dataset_path")
        if not dataset_path:
            raise HTTPException(status_code=400, detail="É necessário fornecer 'dataset_path' no body da requisição")
        
        # carrega dataset de teste
        df_test = pd.read_csv("datasets/credit_01/test.gz", compression="gzip")
        
        # carrega dataset fornecido
        df_new = pd.read_csv(dataset_path, compression="gzip")
        df_new = df_new.replace({None: np.nan})

        # identifica colunas categóricas
        cat_cols = df_test.select_dtypes(include=["object", "category"]).columns
        # para cada coluna categórica, substitui valores desconhecidos por np.nan
        for col in cat_cols:
            valores_treino = set(df_test[col].dropna().unique())
            df_new[col] = df_new[col].apply(lambda x: x if x in valores_treino or pd.isna(x) else np.nan)

        # alinha colunas do novo dataset com as do teste
        cols_model = df_test.drop(columns=["TARGET"], errors="ignore").columns
        df_new = df_new.reindex(columns=cols_model, fill_value=np.nan)

        # gera scores

        scores_new = model.predict_proba(df_new)[:, 1] # retornando a chance de ser a classe 1
        scores_test = model.predict_proba(df_test.drop(columns=["TARGET"], errors="ignore"))[:, 1]

        # scores com o novo modelo
        # my_model_scores_new = my_model.predict_proba(df_new)[:, 1]
        # my_model_scores_test = my_model.predict_proba(df_test.drop(columns=["TARGET"], errors="ignore"))[:, 1]

        ks_stat, p_value = ks_2samp(scores_new, scores_test)
        # my_model_ks_stat, my_model_p_value = ks_2samp(my_model_scores_new, my_model_scores_test)

        return {
            "ks_statistic": float(ks_stat),
            "p_value": float(p_value),
            # "my_model_ks_statistic": float(my_model_ks_stat),
            # "my_model_p_value": float(my_model_p_value)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
