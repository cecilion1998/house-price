import requests
import json


def search_apartment_rent(min_size, max_size):
    # URL for the POST request
    url = "https://api.divar.ir/v8/postlist/w/search"

    # Payload with minimum and maximum values passed as input
    payload = {
        "city_ids": ["1"],
        "pagination_data": {
            "@type": "type.googleapis.com/post_list.PaginationData",
            "last_post_date": "2024-08-24T13:51:04.973912Z",
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

        # Extract specific fields from each item in list_widgets
        for item in list_widgets:
            data = item.get('data', {})
            title = data.get('title', 'N/A')
            middle_description_text = data.get('middle_description_text', 'N/A')
            top_description_text = data.get('top_description_text', 'N/A')

            # Print the extracted fields
            print(f"Title: {title}")
            print(f"Middle Description: {middle_description_text}")
            print(f"Top Description: {top_description_text}")
            print("-" * 50)

    else:
        print("Failed to retrieve data. Status code:", response.status_code)


# Example usage with minimum and maximum inputs
min_size = 60
max_size = 80
search_apartment_rent(min_size, max_size)
