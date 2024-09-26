import requests
import json
import re
import csv
from datetime import datetime, timezone


def convert_to_number(text):
    """Convert Persian numerals and formatted string to an integer, return 0 if not a number."""
    persian_to_english = text.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))
    cleaned_text = re.sub(r'[^\d]', '', persian_to_english)

    # Return 0 if the cleaned text is empty (e.g., for 'رهن کامل')
    if not cleaned_text:
        return 0

    return int(cleaned_text)


def search_apartment_rent(min_size, max_size, output_file):
    # URL for the POST request
    url = "https://api.divar.ir/v8/postlist/w/search"

    # Get the current time in ISO 8601 format with milliseconds and Z (UTC time)
    current_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds')

    # Payload with minimum and maximum values passed as input
    payload = {
        "city_ids": ["1"],
        "pagination_data": {
            "@type": "type.googleapis.com/post_list.PaginationData",
            "last_post_date": current_time,  # Use dynamic current time here
            "page": 1,
            "layer_page": 1,
            "search_uid": "02a284cd-a3bc-4934-978c-ff750052bb27"
        },
        "search_data": {
            "form_data": {
                "data": {
                    "category": {"str": {"value": "apartment-rent"}},
                    "districts": {"repeated_string": {"value": ["302"]}},
                    "rooms": {"repeated_string": {"value": ["یک"]}},
                    "size": {"number_range": {"minimum": str(min_size), "maximum": str(max_size)}},
                    "building-age": {"number_range": {"maximum": "15"}}
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

        # Prepare CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'title', 'rent', 'deposit', 'total'])  # CSV headers

            # Extract specific fields from each item in list_widgets
            for idx, item in enumerate(list_widgets):
                data = item.get('data', {})
                title = data.get('title', 'N/A')
                middle_description_text = data.get('middle_description_text', 'N/A')
                top_description_text = data.get('top_description_text', 'N/A')

                # Convert rent and deposit to numbers
                rent = convert_to_number(middle_description_text.split(': ')[-1])
                deposit = convert_to_number(top_description_text.split(': ')[-1])

                # Calculate the total
                total = (rent / 3000000) * 100000000 + deposit

                # Write to CSV
                writer.writerow([idx + 1, title, rent, deposit, int(total)])

                # Optionally, print the extracted fields and total to console
                print(f"Id: {idx + 1}")
                print(f"Title: {title}")
                print(f"Rent: {rent} تومان")
                print(f"Deposit: {deposit} تومان")
                print(f"Total: {int(total)} تومان")
                print("-" * 50)

    else:
        print("Failed to retrieve data. Status code:", response.status_code)


# Example usage with minimum and maximum inputs and output file name
min_size = 60
max_size = 80
output_file = 'apartment_rent_data.csv'
search_apartment_rent(min_size, max_size, output_file)
