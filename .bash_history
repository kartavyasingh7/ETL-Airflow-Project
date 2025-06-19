cd ~/C:/Users/Acer/Desktop/ETL Airflow Project
cd ~/ETL Airflow Project
source venv/bin/activate
ls
which python
cd ~/ETL Airflow Project
which airflow
ls venv/bin/airflow
ls
which airflow
.venv/bin/airflow db init
ls
source venv/bin/activate
cd ~/ETL Airflow Project
ls
python3.10 -m venv venv
source venv/bin/activate
export AIRFLOW_VERSION=2.9.1
export PYTHON_VERSION=3.10export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
export PYTHON_VERSION=3.10
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
airflow db init
mkdir dags scripts data
touch README.md requirements.txt .gitignore
nano .gitignore
