# DesafioDNC

Pipeline de Extração e Armazenamento de Dados Meteorológicos e de Trânsito

### • Descrição
Este projeto consiste em uma pipeline para a extração de dados **meteorológicos** e de **trânsito** de fontes externas, processamento desses dados e armazenamento em um banco de dados **PostgreSQL** hospedado no [***ElephantSQL***](https://www.elephantsql.com/). As informações meteorológicas são obtidas da [***Open-Meteo API***](https://open-meteo.com/en/docs), enquanto as informações de trânsito são adquiridas através da [***TomTom API***](https://developer.tomtom.com/routing-api/documentation/routing/routing-service). A execução da pipeline é orquestrada usando o ***Apache Airflow*** no [***Google Cloud Platform (GCP)***](https://cloud.google.com/?hl=pt_br). As funções responsáveis pela extração de dados estão hospedadas no ***Google Cloud Functions***.

### • Componentes
**FORECAST**: Módulo Python para a extração, processamento e armazenamento de dados meteorológicos;<br>
**TRAFFIC**: Módulo Python para a extração, processamento e armazenamento de dados de trânsito;<br>
**CONSTANTS**: Arquivo para armazenar constantes e configurações do projeto.<br>

### • DAGs (Directed Acyclic Graphs):
**cleanup.py:** DAG para limpeza de dados históricos no banco de dados;<br>
**forecast.py:** DAG para obtenção e armazenamento de dados meteorológicos;<br>
**traffic.py:** DAG para obtenção e armazenamento de dados de trânsito.


## • Configuração

### • Dependências:

Python 3.x<br>
Pacotes Python: requests, psycopg2;<br>
Apache Airflow instalado localmente ou no GCP.

### • Configuração do Banco de Dados:

Configure as informações de conexão no arquivo **constants.py**;<br>
Certifique-se de que o **PostgreSQL** esteja configurado e acessível.<br>

### • Configuração da API:

Obtenha as **chaves de API** necessárias para ***Open-Meteo*** e ***TomTom API***;<br>
Adicione as chaves no arquivo **constants.py***.

### • Configuração do Google Cloud Functions:

As funções Python **(forecast e traffic)** estão hospedadas no ***Google Cloud Functions***. Certifique-se de configurar corretamente no **GCP** e ajustar as chamadas dessas funções nas **DAGs**.

### • Configuração do Apache Airflow:

Certifique-se de que o **Apache Airflow** esteja configurado e as **DAGs** estejam no diretório apropriado.<br>

**Uso:**<br>
Execute as **DAGs** no **Apache Airflow** conforme a necessidade:

**cleanup.py** para limpar dados históricos antigos;<br>
**forecast.py** para obter e armazenar dados meteorológicos;<br>
**traffic.py** para obter e armazenar dados de trânsito;<br><br>
Certifique-se de configurar os agendamentos das **DAGs** de acordo com as necessidades do projeto.
