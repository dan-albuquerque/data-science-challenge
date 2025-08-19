# 🚀 Monitoramento de Modelos de Crédito

Este projeto implementa uma API em **FastAPI** para monitoramento de modelos de concessão de crédito em produção.  
A API possui endpoints para cálculo de **performance** (AUC-ROC e volumetria mensal) e **aderência** (teste estatístico KS entre distribuições de score).

---

## 📂 Estrutura do Projeto

monitoring/
│── app/
│ ├── api/
│ │ ├── endpoints/
│ │ │ ├── aderencia.py
│ │ │ ├── performance.py
│ │ └── routers.py
│ ├── main.py
│── model.pkl
│── batch_records.json
│── requirements.txt
│── README.md