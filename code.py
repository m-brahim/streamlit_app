import streamlit as st
import snowflake.connector
import pandas as pd

# Remplacez ces valeurs par vos propres informations de connexion
username = "BMEGDOUD@SYNERGY.FR"
password = "Azert2609*"
account = "synergy.eu-west-1.snowflakecomputing.com"
database = "DEMODB"
warehouse = "SYNERGY"

# Établir la connexion à Snowflake
conn = snowflake.connector.connect(
    user=username,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database
)
