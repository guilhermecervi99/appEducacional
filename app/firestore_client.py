# app/firestore_client.py
from google.cloud import firestore

def get_firestore_client():
    """
    Inicializa e retorna um cliente do Firestore.
    As credenciais são obtidas a partir da variável de ambiente GOOGLE_APPLICATION_CREDENTIALS.
    """
    return firestore.Client()
