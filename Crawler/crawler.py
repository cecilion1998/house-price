import requests
import json
import re
import csv
from datetime import datetime, timezone
import uuid
import os

# Global counter to ensure unique IDs across all requests
unique_id_counter = 1

def run_search_from_file(input_file, output_file):
    global unique_id_counter  # Access the global counter
    # Open the CSV file that contains the search parameters
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        # Loop through each row in the file
        for row in reader:
            min_size = int(row[0])
            max_size = int(row[1])
            min_building_age = int(row[2])
            max_building_age = int(row[3])
            rooms = row[4]

            # Call the search_apartment_rent function with the parameters from the file
            search_apartment_rent(min_size, max_size, rooms, min_building_age, max_building_age, output_file)


def convert_to_number(text):
    """Convert Persian numerals and formatted string to an integer, return 0 if not a number."""
    persian_to_english = text.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
    cleaned_text = re.sub(r'[^\d]', '', persian_to_english)

    # Return 0 if the cleaned text is empty (e.g., for 'رهن کامل')
    if not cleaned_text:
        return 0

    return int(cleaned_text)


def search_apartment_rent(min_size, max_size, rooms, min_building_age, max_building_age, output_file):
    global unique_id_counter  # Access the global counter

    # URL for the POST request
    url = "https://api.divar.ir/v8/postlist/w/search"

    # Get the current time in ISO 8601 format with milliseconds and Z (UTC time)
    current_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds')

    # Generate a random UUID
    search_uid = str(uuid.uuid4())  # Generate a random UUID for search_uid

    # Payload with minimum and maximum values passed as input
    payload = {
        "city_ids": ["1"],
        "pagination_data": {
            "@type": "type.googleapis.com/post_list.PaginationData",
            "last_post_date": current_time,
            "page": 1,
            "layer_page": 1,
            "search_uid": search_uid  # Use the random UUID here
        },
        "search_data": {
            "form_data": {
                "data": {
                    "category": {"str": {"value": "apartment-rent"}},
                    "districts": {"repeated_string": {"value": ["302"]}},
                    "rooms": {"repeated_string": {"value": [rooms]}},  # Dynamic rooms input
                    "size": {"number_range": {"minimum": str(min_size), "maximum": str(max_size)}},
                    "building-age": {"number_range": {"minimum": str(min_building_age), "maximum": str(max_building_age)}}  # Dynamic building age input
                }
            },
            "server_payload": {
                "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                "additional_form_data": {
                    "data": {
                        "sort": {"str": {"value": "sort_date"}}
                    }
                }
            }
        }
    }

    # Headers (if necessary)
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_json = response.json()

        # Extract list_widgets from the response
        list_widgets = response_json.get('list_widgets', [])

        # Check if the output file already exists
        file_exists = os.path.exists(output_file)

        # Open the file in append mode
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the headers if the file is new
            if not file_exists:
                writer.writerow(
                    ['id', 'title', 'rent', 'deposit', 'total', 'min_size', 'max_size', 'rooms', 'min_building_age', 'max_building_age'])

            # Extract specific fields from each item in list_widgets
            for item in list_widgets:
                data = item.get('data', {})
                title = data.get('title', 'N/A')
                middle_description_text = data.get('middle_description_text', 'N/A')
                top_description_text = data.get('top_description_text', 'N/A')

                # Convert rent and deposit to numbers
                rent = convert_to_number(middle_description_text.split(': ')[-1])
                deposit = convert_to_number(top_description_text.split(': ')[-1])

                # Calculate the total
                total = (rent / 3000000) * 100000000 + deposit

                # Write to CSV with min_size, max_size, rooms, min_building_age, and max_building_age
                writer.writerow([unique_id_counter, title, rent, deposit, int(total), min_size, max_size, rooms, min_building_age, max_building_age])

                # Optionally, print the extracted fields and total to console
                print(f"Id: {unique_id_counter}")
                print(f"Title: {title}")
                print(f"Rent: {rent} تومان")
                print(f"Deposit: {deposit} تومان")
                print(f"Total: {int(total)} تومان")
                print(f"Min Size: {min_size}, Max Size: {max_size}")
                print(f"Rooms: {rooms}, Min Building Age: {min_building_age}, Max Building Age: {max_building_age}")
                print("-" * 50)

                # Increment the unique ID counter after each entry
                unique_id_counter += 1

    else:
        print("Failed to retrieve data. Status code:", response.status_code)


# Call the function to read from the generated file and perform searches
input_file = 'search_parameters.csv'  # The file created in Step 1
output_file = 'apartment_rent_data.csv'  # Output file for search results
run_search_from_file(input_file, output_file)
