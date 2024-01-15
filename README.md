# DesafioDNC

Pipeline de Extração e Armazenamento de Dados Meteorológicos e de Trânsito

## Descrição
Este projeto consiste em uma pipeline para a extração de dados **meteorológicos** e de **trânsito** de fontes externas, processamento desses dados e armazenamento em um banco de dados hospedado no ***BigQuery***, e também para geração de [***GRÁFICOS***](https://docs.google.com/spreadsheets/d/1Usr2-kDk-96gmttQ7C3WRi62HZ4V9thorYlSZstdIZ0/edit?usp=sharing). As informações meteorológicas são obtidas da [***Open-Meteo API***](https://open-meteo.com/en/docs), enquanto as informações de trânsito são adquiridas através da [***TomTom API***](https://developer.tomtom.com/routing-api/documentation/routing/routing-service). A execução da pipeline é orquestrada usando o ***Apache Airflow*** no [***Google Cloud Platform (GCP)***](https://cloud.google.com/?hl=pt_br). As funções responsáveis pela extração de dados estão hospedadas no ***Google Cloud Functions***.

### • Componentes do Projeto

***- Google Cloud Functions:***<br>
Funções para chamar APIs de previsão do tempo e tráfego, processar dados e enviar para o Cloud Storage.
- API-TO-GCS: Módulo ***Python*** para a extração, processamento e armazenamento de dados meteorológicos e de trânsito;<br>
- CONSTANTS: Arquivo para armazenar constantes e configurações do projeto.<br>

***- Google Cloud Storage:***<br>
Armazenamento de arquivos ***JSON*** gerados pela extração de dados.

***- Google BigQuery:***<br>
Armazém de dados para armazenar informações de previsão do tempo e tráfego.<br>
 - Esquema do Banco de dados:
  <img src="https://github.com/joa0-saldanha/DesafioDNC/assets/80000631/e83f74c3-6f58-40d0-aa09-aa11f3a4e6a8"  width="700" height="500">



***- Apache Airflow:***<br>
Orquestrador de fluxos de trabalho para programar e monitorar a execução das tarefas.

- DAGs (Directed Acyclic Graphs):<br><br>
**forecast.py:** DAG para obtenção e armazenamento de dados meteorológicos;<br>
**traffic.py:** DAG para obtenção e armazenamento de dados de trânsito;<br>
**cleanup.py:** DAG para limpeza das tabelas históricas.

***- Cloud Build***<br>
A configuração do **Cloud Build** é definida nos TRIGGERS, executando os passos especificados nos arquivos *cloudbuild.yaml* na raiz do projeto. Este arquivo contém as etapas do pipeline **CI/CD**.

***- Secret Manager***<br>
No GCP Secret Manager foram configurados segredos com informações sensíveis para serem utilizados com segurança no deploy da solução.

***- Google Sheets***<br>
A configuração do **Google Sheets** é definida no UI da plataforma, consumindo os dados das tabelas no **BigQuery** de hora em hora e consequentemente atualizando os gráficos.

## Configuração

### • Dependências:

Python 3.x<br>
Pacotes Python: requests, google-cloud, pytz;<br>
Apache Airflow instalado localmente ou no GCP.

### • Configuração do Banco de Dados:

Configure as informações de conexão no arquivo **constants.py**;<br>
Certifique-se de que o **BigQuery** ou outro Banco de Dados esteja configurado e acessível.<br>

### • Configuração da API:

Obtenha as **chaves de API** necessárias para ***Open-Meteo*** e ***TomTom API***;<br>
Adicione as chaves no arquivo **constants.py***.

### • Configuração do Google Cloud Functions:

A função Python **API-TO-GCS** esta hospedada no ***Google Cloud Functions***. Certifique-se de configurar corretamente no **GCP** e ajustar as chamadas dessa função nas **DAGs**.

### • Configuração do Apache Airflow:

Certifique-se de que o **Apache Airflow** esteja configurado e as **DAGs** estejam no diretório apropriado.<br>

### • Configuração do Google Sheets:

Certifique-se de conectar apropriadamente os dados do **BigQuery** ao **Google Sheets** para a geração e atualização dos gráficos.<br>


## Uso: ##

Execute as **DAGs** no **Apache Airflow** conforme a necessidade:

Certifique-se de configurar os agendamentos das **DAGs** de acordo com as necessidades do projeto.

## Links: ##

• [**Gráficos**](https://docs.google.com/spreadsheets/d/1Usr2-kDk-96gmttQ7C3WRi62HZ4V9thorYlSZstdIZ0/edit?usp=sharing);<br>
• [**Esquema database**](https://drawsql.app/teams/myself-207/diagrams/dncchallenge);<br>
• [**Open-Meteo API**](https://open-meteo.com/en/docs);<br>
• [**TomTom API**](https://developer.tomtom.com/routing-api/documentation/routing/routing-service)<br>.
