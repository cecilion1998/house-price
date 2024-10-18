import csv


def generate_search_parameters(output_file):
    # Define the step for min_size_area, max_size_area, and building_age
    size_step = 10
    age_step = 5

    # Define the range for min_size_area and min_building_age
    min_size_areas = range(0, 201, size_step)  # Generate min_size_area from 0 to 200 with step 10
    min_building_ages = range(0, 31, age_step)  # Generate building ages from 0 to 30 with step 5

    # Define the room options (in Persian)
    rooms = ['یک', 'دو', 'سه', 'چهار', 'پنج']  # One to five rooms

    # Open the CSV file to write the parameters
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(['min_size_area', 'max_size_area', 'min_building_age', 'max_building_age', 'rooms'])

        # Generate all combinations of the parameters
        for min_size_area in min_size_areas:
            max_size_area = min_size_area + size_step - 1  # Ensure no overlap, e.g., 0-9, 10-19
            for min_building_age in min_building_ages:
                max_building_age = min_building_age + age_step - 1  # Ensure no overlap, e.g., 0-5, 6-10
                for room in rooms:
                    # Write the combination to the file
                    writer.writerow([min_size_area, max_size_area, min_building_age, max_building_age, room])

    print(f"Search parameters saved to {output_file}")


# Call the function to generate the CSV file
output_file = 'search_parameters.csv'
generate_search_parameters(output_file)
