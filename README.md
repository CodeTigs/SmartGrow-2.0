# 🌱 SmartGrow - Backend de Estufa Inteligente

Este repositório contém o código do backend para o projeto "SmartGrow", um sistema de automação de estufa que utiliza **Lógica Fuzzy** para o controle inteligente de ambiente.

O sistema é construído em Python usando o framework **FastAPI** e é responsável por:
* Receber dados de sensores (temperatura, umidade do solo).
* Processar esses dados através de um motor de inferência Fuzzy para controlar irrigação e ventilação.
* Controlar a iluminação através de um temporizador fixo (ligado das 18h às 23h).
* Retornar os níveis de controle (0-100%) para os atuadores (irrigação, ventilação).
* Armazenar o histórico de leituras em um banco de dados SQLite.
* Fornecer endpoints para controle manual do sistema.

## 🚀 Tecnologias Utilizadas
* **Python 3**
* **FastAPI:** Para a criação da API RESTful.
* **Scikit-Fuzzy (`skfuzzy`):** Para a implementação da Lógica de Controle Fuzzy.
* **SQLite3:** Para armazenamento leve e local do histórico de dados.
* **Uvicorn:** Como servidor ASGI para rodar a API.

## ⚙️ Como Rodar o Projeto Localmente

Siga estes passos para configurar e executar o backend no seu computador.

### 1. Pré-requisitos
* [Git](https://git-scm.com/)
* [Python 3.10+](https://www.python.org/)

### 2. Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/EnzoCouto1/SmartGrow
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o venv
    python -m venv venv
    
    # Ativar no Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    ```
    *(Se a ativação falhar no PowerShell, rode `Set-ExecutionPolicy Bypass -Scope Process` e tente novamente)*

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o Banco de Dados:**
    O `main.py` criará e configurará o banco de dados automaticamente na primeira vez que for executado. O script `database.py` pode ser usado como referência, mas não precisa ser executado manualmente.

### 3. Execução

1.  **Inicie o Servidor da API:**
    ```bash
    # O --host 0.0.0.0 permite que o ESP32 na sua rede local acesse a API
    uvicorn main:app --reload --host 0.0.0.0
    ```

2.  **Acesse a API:**
    * **Servidor Rodando em:** `http://localhost:8000`
    * **Documentação Interativa (Swagger):** `http://localhost:8000/docs`

## 🧪 Como Testar o Backend

Enquanto o hardware (ESP32) não está conectado, você pode usar o script `teste_sensor.py` para simular o envio de dados.

1.  Mantenha o servidor rodando no primeiro terminal.
2.  Abra um **segundo terminal**, ative o `venv` nele também.
3.  Execute o script de teste:
    ```bash
    python teste_sensor.py
    ```
4.  Siga as instruções no menu do console para enviar cenários de teste.

## 🤖 API Endpoints

### `POST /leituras`
Recebe as leituras dos sensores, aciona a lógica Fuzzy e retorna o estado dos atuadores. **Este é o único endpoint que o ESP32 utiliza.**
* **Corpo da Requisição (JSON):**
    ```json
    {
      "temperatura_celsius": 25.5,
      "umidade_solo": 45.2
    }
    ```
* **Resposta (JSON):**
    A resposta contém o estado calculado para os atuadores, que o ESP32 deve aplicar.
    ```json
    {
      "status": "sucesso",
      "mensagem": "Leitura processada com lógica fuzzy.",
      "estado_atual": {
        "nivel_irrigacao": 15.0,
        "velocidade_ventilacao": 35.5,
        "nivel_iluminacao": 0.0 
      }
    }
    ```
    *(O `nivel_iluminacao` é controlado pelo temporizador no backend, não pela lógica fuzzy)*

### `GET /status_sistema`
Consulta o estado atual dos atuadores. Pode ser usado por um frontend, mas não é utilizado pelo ESP32.
* **Resposta (JSON):**
    ```json
    {
      "nivel_irrigacao": 15.0,
      "velocidade_ventilacao": 35.5,
      "nivel_iluminacao": 0.0
    }
    ```

### `POST /manual/irrigacao/{nivel}`
Define manualmente o nível de irrigação (0-100).
* **Exemplo:** `POST /manual/irrigacao/50`

### `POST /manual/ventilacao/{velocidade}`
Define manualmente a velocidade da ventilação (0-100).
* **Exemplo:** `POST /manual/ventilacao/75`

### `GET /leituras`
Consulta o histórico de leituras salvas no banco de dados.
* **Resposta (JSON):**
    ```json
    [
      {
        "id": 1,
        "temperatura": 25.5,
        "umidade": 45.2,
        "horario": "2025-11-05T20:30:00.123456"
      }
    ]
    ```
