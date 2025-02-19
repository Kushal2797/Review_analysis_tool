import json
import csv
import openai
import argparse
import logging
from collections import Counter
from sklearn.cluster import AgglomerativeClustering
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("script.log"),  # Log messages to file
        logging.StreamHandler()  # Also print logs to console
    ]
)
# Load OpenAI API Key

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found! Set it in .env or environment variables.")


def get_embeddings(text_list):
    """Fetches embeddings from OpenAI's text-embedding-3-small model for a list of attributes."""
    try:
        response = openai.Embedding.create(
            model="text-embedding-3-small",
            input=text_list
        )
        return [item["embedding"] for item in response["data"]]
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        return [np.zeros(1536) for _ in text_list]  # Return zero vectors if API call fails

def cluster_attributes(attributes):
    """Clusters similar attributes using OpenAI embeddings and Agglomerative Clustering."""
    if not attributes:
        return {}
    try:
        attribute_counts = Counter(attributes)  # Keep track of attribute frequency
        unique_attributes = list(attribute_counts.keys())  # Get unique attributes
        
        embeddings = get_embeddings(unique_attributes)
        clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=1)
        labels = clustering_model.fit_predict(embeddings)
        
        clustered_frequencies = {}
        for idx, label in enumerate(labels):
            cluster_key = f"Cluster {label}"
            if cluster_key not in clustered_frequencies:
                clustered_frequencies[cluster_key] = []
            clustered_frequencies[cluster_key].append(unique_attributes[idx])
        
        # Pick the shortest attribute name as the representative
        final_clusters = {}
        for cluster, attr_list in clustered_frequencies.items():
            representative = min(attr_list, key=len)
            final_clusters[representative] = sum(attribute_counts[attr] for attr in attr_list)
        
        return final_clusters
    except Exception as e:
        logging.error(f"Error in clustering attributes: {e}")
        return {}

# System and User Prompts
SYSTEM_PROMPT = """
You are an AI assistant that extracts delight attributes from customer reviews.
Identify key aspects that customers love about a product and return relevant attributes.
"""

def extract_delight_attributes_batch(reviews):
    """Uses OpenAI to extract delight attributes for a batch of reviews."""
    try:
        formatted_reviews = "\n".join([f"Review {idx+1}: {review}" for idx, review in enumerate(reviews)])
        
        prompt = f"""
        Reviews:{formatted_reviews}
        Identify delight attributes that customers love about the product from the reviews provided Above.
        A review contains one or more than one attributes.
        If no specific delight attribute is mentioned and review is very generic then return "General" otherwise return a list of attribute(s) in your response. 
        Some examples of Generic reviews are those which contains following kind of information:
            1. Client loves the product and satisfied with the quality.
            2. Client only gives star ratinf in the review and no key attributes are mentioned.
        Instructions to follow while extracting delight attributes:
            1. Only include those attributes which customer actully loved and clearly visible in the customer's review.
            2. For a particular review do not repeat same kind of delight attribute. (Fragrance and odor control are same kind of attributes.)
            3. Multiple reviews might talk about the same delight attributes in different words, so please use standard attribute words in your response, which I can combine in the later stages by some means of clustering method. 
            4. If a customer is recommanding a product then it is not any delight attribute.
        Return JSON object in your response with Review number as the key and attributes as the value.
        Sample output format is provided below for your reference.
        {{
        "Review 1":[list of attribute(s)] or 'None'
        "Review 2":[list of attribute(s)] or 'None'
        ...
        }}."""
        
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
            
        )
        
        output = response["choices"][0]["message"]["content"].strip()

        start = output.find("{")
        end = output.rfind("}") +1
        output = output[start:end]
        
        return output
    except Exception as e:
        logging.error(f"Error extracting delight attributes: {e}")
        return ["General"] * len(reviews)
    

def process_reviews(input_file, json_output, csv_output, batch_size=100):
    """Processes reviews to extract delight attributes and save results."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
    except Exception as e:
        logging.error(f"Error reading input file: {e}")
        return
    extracted_data = []
    attributes = []

    total_batches = len(reviews) // batch_size + (1 if len(reviews) % batch_size != 0 else 0)
    
    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i + batch_size]
        logging.info(f"Processing batch {i // batch_size + 1} of {total_batches}")
        batch_texts = [review['body'] for review in batch]
        delight_attributes_dict = eval(extract_delight_attributes_batch(batch_texts))
        
        for j, review in enumerate(batch):
            delight_attributes = delight_attributes_dict.get(f"Review {j+1}", "None")
            if type(delight_attributes) == list:
                delight_attributes_split = [attr.strip() for attr in delight_attributes]
                attributes.extend(delight_attributes_split)
                delight_attributes_split = ", ".join(delight_attributes_split)

            else:
                delight_attributes_split = "General"
                attributes.append(delight_attributes_split)
            extracted_data.append({
                "review_id": review.get("review_id", "N/A"),
                "author": review.get("author", "N/A"),
                "body": review.get("body", "N/A"),
                "delight_attributes": delight_attributes_split
            })
    clustered_attributes = cluster_attributes(attributes)
    
    # Save JSON output
    try:
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump({"reviews": extracted_data}, f, indent=4)
        logging.info(f"JSON output saved to {json_output}")
    except Exception as e:
        logging.error(f"Error saving JSON output: {e}")
    
    # Save CSV output
    try:
        with open(csv_output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Delight Point", "Frequency"])
            for attr, freq in sorted(clustered_attributes.items(), key=lambda x: x[1], reverse=True):
                writer.writerow([attr, freq])
        logging.info(f"CSV output saved to {csv_output}")
    except Exception as e:
        logging.error(f"Error saving CSV output: {e}")

    return extracted_data,clustered_attributes


def main():
    parser = argparse.ArgumentParser(description="Extract delight attributes from customer reviews.")
    parser.add_argument("input_file", type=str, help="Path to the reviews JSON file")
    parser.add_argument("json_output", type=str, help="Path to save the extracted JSON output")
    parser.add_argument("csv_output", type=str, help="Path to save the frequency CSV output")
    args = parser.parse_args()
    process_reviews(args.input_file, args.json_output, args.csv_output)

if __name__ == "__main__":
    main()