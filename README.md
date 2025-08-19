# Monitoramento de Modelos de Crédito

API em FastAPI para monitorar um modelo em produção.


A API possui dois endpoints principais:
- performance e volumetria mensal do lote recebido

- aderência via teste Kolmogorov–Smirnov entre os scores do lote e a base de teste

## Estrutura do repositório
```
monitoring/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── performance.py
│   │       └── aderencia.py
│   ├── routers.py
│   └── main.py
|
├── model.pkl
├── batch_records.json
└── requirements.txt

datasets/
├── credit_01
│ ├── oot.gz
│ ├── test.gz
| └── train.gz
health/
credit/
README.md
.gitignore
testes.ipynb # notebook testando endpoints da API e respondendo perguntas do desafio
```

Observação: se seu clone veio com caminhos ligeiramente diferentes, ajuste os paths indicados.

## Pré-requisitos:
- Python 3.10
- Conda ou venv 
- Portas 8001 livres no host

## Criação do ambiente
- Conda recomendado.

```conda terminal
conda create -n monitoring python=3.10 -y
conda activate monitoring
```

## Instalação das dependências

Na raiz do repositório:


pip install -r monitoring/requirements.txt

Se necessário, garanta estes pacotes mínimos instalados:
- scikit-learn == 1.0.2

- fastapi==0.70.0

- uvicorn==0.15.0

- pandas~=1.3.5

- scipy==1.15.3

- pydantic==1.8.2

- requests==2.25.1

Exemplo de instalação direta(lembre de colocar as versões, o modelo precisa da versão do sklearn 1.0.2):

```
pip install fastapi uvicorn pandas numpy scipy scikit-learn pydantic requests
```

## Executando a API
```
python monitoring/app/main.py
```

A API ficará disponível em:

http://localhost:8001

## executando o notebook de testes
- no arquivo testes.ipynb clique no botaõ de "run all" e verá minhas respostas as perguntas e os endpoints funcionando.

## Meu processo e feedback
- Dediquei mais tempo à compreensão dos requisitos, já que fazia algum tempo que não desenvolvia uma API (minha experiência é maior em consumir APIs). O início exigiu mais atenção para estruturar a arquitetura e adaptar o código já disponibilizado.
- Houve certa negligência da minha parte em relação a versões e dependências. Enfrentei dificuldades para rodar o código com a versão 1.0.2 do scikit-learn, o que demandou ajustes e consumiu tempo adicional.
- Após superar essas etapas mais burocráticas, consegui organizar o código, seguindo os requisitos e o passo a passo do desafio. Essa foi a parte mais tranquila da implementação.
- Gostei desse desafio pois ampliou minha visão sobre como modelos de machine learning são monitorados em produção. Questões como tempo, volumetria e controle de uso me fizeram refletir sobre aspectos que até então não faziam parte do meu foco, já que estive mais voltado ao desenvolvimento dos modelos em si. :)
- Como sugestão de melhoria, acredito que o repositório do desafio poderia estar mais enxuto. Algumas pastas não são destinadas a esta etapa, e embora entenda que possam ser aproveitadas em desafios futuros, a presença delas pode causar certa confusão inicial.
