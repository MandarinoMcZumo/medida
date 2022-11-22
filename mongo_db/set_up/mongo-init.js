data_db = db.getSiblingDB('data');
data_db.createCollection('ranking');
data_db.createCollection('events');
backup_db = db.getSiblingDB('back_up');
backup_db.createCollection('airflow_requests');