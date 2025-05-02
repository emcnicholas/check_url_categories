import os
import requests


def get_domain_categorization(domain):
    """
    Fetch the domain categorization from Cisco Umbrella Investigate API.

    Args:
        domain (str): The domain to categorize (e.g., "example.com").

    Returns:
        dict: The API response in JSON format.
    """
    # Fetch the access token from environment variables
    access_token = os.getenv("INVESTIGATE_ACCESS_TOKEN")

    if not access_token:
        raise ValueError("Access token not found. Please set the 'INVESTIGATE_ACCESS_TOKEN' environment variable.")

    # Base URL for the Umbrella Investigate API
    url = f"https://investigate.api.umbrella.com/domains/categorization/{domain}?showlabels"

    # Headers required for the request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check the response status and return the JSON response if successful
    if response.status_code == 200:
        return response.json()
    else:
        # Raise an exception for unsuccessful status codes with the reason
        response.raise_for_status()


def prepare_and_categorize_domain(domain):
    """
    Inspects and transforms the domain parameter before passing it to the
    get_domain_categorization function. If the domain starts with '*.',
    it strips the '*.' and processes the remaining domain.

    Args:
        domain (str): The domain to categorize (e.g., "*.example.com" or "example.com").

    Returns:
        dict: The response from the get_domain_categorization function.
    """
    # Check if the domain starts with '*.' and strip it if necessary
    if domain.startswith("*."):
        domain = domain[2:]  # Remove the '*.' from the beginning

    # Pass the transformed domain to the get_domain_categorization function
    category = get_domain_categorization(domain)
    domain_category = category[domain]['content_categories']
    #return get_domain_categorization(domain)
    return domain_category

# Example usage:
# Ensure the environment variable 'INVESTIGATE_ACCESS_TOKEN' is set before running this script.
# Example: export INVESTIGATE_ACCESS_TOKEN="YourAccessToken"
result = prepare_and_categorize_domain("cnn.com")
print(result)