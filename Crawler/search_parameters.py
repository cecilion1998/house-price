import csv

def generate_search_parameters(output_file):
    # Define the step for min_size, max_size, and building_age
    size_step = 10
    age_step = 5

    # Define the range for min_size, max_size, and building_age
    min_sizes = range(0, 201, size_step)  # Generate min_sizes from 0 to 200 with step 10
    building_ages = range(0, 31, age_step)  # Generate building ages from 0 to 30 with step 5

    # Define the room options (in Persian)
    rooms = ['یک', 'دو', 'سه', 'چهار', 'پنج']  # One to five rooms

    # Open the CSV file to write the parameters
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(['min_size', 'max_size', 'building_age', 'rooms'])

        # Generate all combinations of the parameters
        for min_size in min_sizes:
            max_size = min_size + size_step  # Ensure max_size is exactly one step above min_size
            for building_age in building_ages:
                max_building_age = building_age + age_step  # Same for building_age
                for room in rooms:
                    # Write the combination to the file
                    writer.writerow([min_size, max_size, building_age, room])

    print(f"Search parameters saved to {output_file}")


# Call the function to generate the CSV file
output_file = 'search_parameters.csv'
generate_search_parameters(output_file)
