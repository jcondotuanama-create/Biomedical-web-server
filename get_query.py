import requests
import json
from query import QUERY_ONLY_DISEASE,QUERY_ONLY_TARGET,QUERY_STRING_ASSOCIATION,QUERY_STRING_DISEASE,QUERY_STRING_TARGET


def get_query_target(gene_id):            
      # Set variables object of arguments to be passed to endpoint
  variables = {"ensemblId": gene_id}

  # Set base URL of GraphQL API endpoint
  base_url = "https://api.platform.opentargets.org/api/v4/graphql"

  # Perform POST request and check status code of response
  r = requests.post(base_url, json={"query": QUERY_STRING_TARGET, "variables": variables})
  print(r.status_code)

  # Transform API response from JSON into Python dictionary and print in console
  api_response = json.loads(r.text)
  return api_response
  
def get_query_disease(efo_id):            
      # Set variables object of arguments to be passed to endpoint
  variables = {"efoId": efo_id}

  # Set base URL of GraphQL API endpoint
  base_url = "https://api.platform.opentargets.org/api/v4/graphql"

  # Perform POST request and check status code of response
  r = requests.post(base_url, json={"query": QUERY_STRING_DISEASE, "variables": variables})
  print(r.status_code)

  # Transform API response from JSON into Python dictionary and print in console
  api_response = json.loads(r.text)
  return api_response
  
  
def get_query_association(gene_id, efo_id):
  variables = {"ensemblId": gene_id ,"efoId": efo_id}

  # Set base URL of GraphQL API endpoint
  base_url = "https://api.platform.opentargets.org/api/v4/graphql"

  # Perform POST request and check status code of response
  r = requests.post(base_url, json={"query": QUERY_STRING_ASSOCIATION, "variables": variables})
  print(r.status_code)

  # Transform API response from JSON into Python dictionary and print in console
  api_response = json.loads(r.text)
  return api_response

def get_targets_asociated(efo_id):
  variables = {"efoId": efo_id}

  # Set base URL of GraphQL API endpoint
  base_url = "https://api.platform.opentargets.org/api/v4/graphql"

  # Perform POST request and check status code of response
  r = requests.post(base_url, json={"query": QUERY_ONLY_DISEASE, "variables": variables})
  print(r.status_code)

  # Transform API response from JSON into Python dictionary and print in console
  api_response = json.loads(r.text)
  return api_response
    
def get_diseases_asociated(gene_id):
  variables = {"ensemblId": gene_id}

  # Set base URL of GraphQL API endpoint
  base_url = "https://api.platform.opentargets.org/api/v4/graphql"

  # Perform POST request and check status code of response
  r = requests.post(base_url, json={"query": QUERY_ONLY_TARGET, "variables": variables})
  print(r.status_code)

  # Transform API response from JSON into Python dictionary and print in console
  api_response = json.loads(r.text)
  return api_response