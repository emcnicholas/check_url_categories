import os
import openpyxl
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

def update_categories_in_excel(file_path):
    """
    Opens the given xlsx file, loops through the 'URL' column, and updates the 'Category'
    column with the 'content_categories' field retrieved from the Cisco Umbrella API.

    Args:
        file_path (str): The path to the Excel file (e.g., 'url.xlsx').

    Returns:
        None
    """
    # Load the workbook and select the active sheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Find column indexes for 'URL' and 'Category'
    url_column_index = None
    category_column_index = None

    # Read the header row to find the 'URL' and 'Category' columns
    for col in range(1, sheet.max_column + 1):
        header = sheet.cell(row=1, column=col).value
        if header == "URL":
            url_column_index = col
        elif header == "Category":
            category_column_index = col

    # Ensure both columns exist
    if url_column_index is None or category_column_index is None:
        raise ValueError("The Excel file must have 'URL' and 'Category' columns.")

    # Iterate through each row (starting from the second row) and update the Category column
    for row in range(2, sheet.max_row + 1):
        # Get the URL from the URL column
        url = sheet.cell(row=row, column=url_column_index).value

        if url:
            # Remove any leading '*.' from the URL
            if url.startswith("*."):
                url = url[2:]

            # Call the Cisco Umbrella API to get content categories
            try:
                response = get_domain_categorization(url)
                content_categories_list = response[url]['content_categories'] #extract_content_categories(response)
                content_categories = ", ".join(content_categories_list)
            except Exception as e:
                content_categories = f"Error: {e}"

            # Update the Category column with the content categories
            sheet.cell(row=row, column=category_column_index, value=content_categories)

    # Save the updated workbook
    workbook.save(file_path)


# Example usage:
# Ensure the environment variable 'UMBRELLA_ACCESS_TOKEN' is set before running this script.
# Example: export UMBRELLA_ACCESS_TOKEN="YourAccessToken"
update_categories_in_excel("url.xlsx")