import requests
import pandas as pd
from datetime import datetime, timedelta

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

# Function to query the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    return response.json()

# Function to clean up text
def clean_text(text):
    # Remove unwanted characters (like hyphens) and extra spaces
    cleaned_text = text.replace('---', '').replace('--', '').strip()
    # Ensure no newline characters at the beginning or end
    cleaned_text = cleaned_text.strip("\n").strip()
    return cleaned_text

# Simplified extraction function
def extract_parts(generated_text):
    summary_start = "Résumé de l'incident"
    products_start = "Produits et technologies impactés"
    impact_start = "Impacts"
    recommendations_start = "Recommandations pour prévenir l'incident"

    # Find positions of each part
    summary_index = generated_text.find(summary_start)
    products_index = generated_text.find(products_start)
    impact_index = generated_text.find(impact_start)
    recommendations_index = generated_text.find(recommendations_start)

    # Debugging: Print the generated text and found indices
    print("Generated Text:", generated_text)
    print("Indices - Summary:", summary_index, "Products:", products_index, "Impact:", impact_index, "Recommendations:", recommendations_index)

    summary = clean_text(generated_text[summary_index + len(summary_start):products_index]) if summary_index != -1 and products_index != -1 else "Non spécifié"
    products = clean_text(generated_text[products_index + len(products_start):impact_index]) if products_index != -1 and impact_index != -1 else "Non spécifié"
    impact = clean_text(generated_text[impact_index + len(impact_start):recommendations_index]) if impact_index != -1 and recommendations_index != -1 else "Non spécifié"
    recommendations = clean_text(generated_text[recommendations_index + len(recommendations_start):]) if recommendations_index != -1 else "Non spécifié"

    return summary, products, impact, recommendations

# Read the summaries from the CSV file
yesterday = datetime.now() - timedelta(1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
file_name = f"{yesterday_str}_articles.csv"
data = pd.read_csv(file_name, encoding="utf-8")

# Lists to store extracted data
extracted_summaries = []
extracted_products = []
extracted_impacts = []
extracted_recommendations = []

for summary_text in data['summary']:
    payload = {
        "inputs": f"""En tant qu'expert en cybersécurité au sein du SOC, votre responsabilité est de préparer des bulletins de sécurité concernant les dernières nouvelles de cybersécurité. Veuillez fournir un résumé bien structuré en phrases simples. Commencez par un "Résumé de l'incident" qui décrit brièvement l'incident en question. Ensuite, précisez les "Produits et technologies impactés" en mentionnant les produits et technologies spécifiques affectés par cet incident, y compris leurs versions si possible (par exemple, systèmes d'exploitation comme Windows ou macOS V10.X, bases de données comme SQL V16.X, Debian bookworm versions antérieures à 6.1.99-1, MaaS360 VPN versions antérieures à 3.000.850, ONTAP Select Deploy administration utility versions antérieures à 9.15.1, etc.). Poursuivez avec une section intitulée "Impacts" où vous énumérerez les conséquences possibles de cet incident (comme l'exécution de code arbitraire à distance, l'atteinte à la confidentialité des données, le déni de service à distance, l'élévation de privilèges, etc...). Enfin, fournissez des "Recommandations pour prévenir l'incident", incluant des recommandations préventives pour éviter ou atténuer l'impact de cet incident. Veuillez générer le texte en français, même si le résumé est en anglais.""",
        "parameters": {
            "temperature": 0.8,
            "top_p": 0.9,
            "top_k": 50,
            "max_new_tokens": 500,
            "repetition_penalty": 1.0,
            "return_full_text": False
        }
    }
    response = query(payload)
    generated_text = response[0]['generated_text'] if isinstance(response, list) and response else ""
    summary, products, impact, recommendations = extract_parts(generated_text)
    extracted_summaries.append(summary)
    extracted_products.append(products)
    extracted_impacts.append(impact)
    extracted_recommendations.append(recommendations)

data['resume'] = extracted_summaries
data['impacted_products'] = extracted_products
data['impacts'] = extracted_impacts
data['recommendations'] = extracted_recommendations

# Save updated DataFrame back to CSV
data.to_csv(file_name, index=False, encoding="utf-8")
