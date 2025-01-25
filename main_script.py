import os
from pprint import pprint
from bs4 import BeautifulSoup
import json  # Import json to load existing data
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Your Oxylabs username and password - DIRECTLY SET HERE (now from .env)
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

# Base URL for cars.com research - you can change the make here
BASE_URL = "https://www.cars.com/research/"

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# Dynamically determine MAKES from files in the data directory
MAKES = []
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        make = filename[:-5]  # Remove ".json" extension
        MAKES.append(make)

company_cars_data = {}  # Initialize a dictionary to store data, keyed by company

if USERNAME and PASSWORD:  # Check if USERNAME and PASSWORD are loaded
    for make in MAKES:
        filename = f"{make}.json"
        filepath = os.path.join(data_dir, filename)

        if os.path.exists(filepath):
            print(
                f"Data file for {make.capitalize()} exists: {filepath}"
            )  # Adjusted print statement
            # Load existing data from JSON file
            with open(filepath, "r") as infile:
                make_data = json.load(infile)  # More generic variable name
                # Assuming your make.json has the structure from your example,
                # extract the HTML content from the 'results' -> 'content'
                if (
                    "results" and make_data["results"]
                ):  # Check if 'results' key exists and is not empty
                    html_content = make_data["results"][0]["content"]

                    soup = BeautifulSoup(html_content, "html.parser")
                    models_data = (
                        []
                    )  # Not really needed anymore, but keeping for now, we will directly add to company_cars_data
                    model_list_items = soup.find_all(
                        "spark-card", class_="new-car-lineup-model-card"
                    )

                    for item in model_list_items:
                        model_name_element = item.find(
                            "div", {"data-qa": lambda x: x and x.startswith(f"{make}-")}
                        )
                        if model_name_element:
                            # Debugging: Print the model_name_element to inspect its content
                            print("\n--- model_name_element content ---")
                            print(model_name_element)

                            link_element = model_name_element.find(
                                "a", {"data-card-link": ""}
                            )  # refined selector

                            if (
                                link_element
                            ):  # Check if link_element is found before proceeding
                                model_name_div = link_element.find(
                                    "div", class_="new-car-model-card-name"
                                )  # find the div inside 'a'
                                if model_name_div:  # Check if model_name_div is found
                                    model_year_model_name = (
                                        model_name_div.text.strip()
                                    )  # extract text from the div

                                    # Splitting to get Year and Model Name (assuming format "YYYY Make Model")
                                    parts = model_year_model_name.split(
                                        " ", 1
                                    )  # Split at the first space
                                    model_year_str = (  # Renamed to model_year_str
                                        parts[0] if parts else "Year N/A"
                                    )  # Year is the first part
                                    model_name = (
                                        parts[1]
                                        if len(parts) > 1
                                        else model_year_model_name
                                    )  # Model is the rest, or full name if no space

                                    price_element = item.find(
                                        "div", class_="new-car-model-card-price"
                                    )
                                    price_str = (  # Renamed to price_str
                                        price_element.text.strip()
                                        if price_element
                                        else "Price not found"
                                    )

                                    car_data = {
                                        "year": model_year_str,  # Initially string
                                        "model": model_name,
                                        "price": price_str,  # Initially string
                                    }  # Car data dict

                                    # Convert year to integer
                                    try:
                                        car_data["year"] = int(car_data["year"])
                                    except ValueError:
                                        print(
                                            f"Warning: Could not convert year '{car_data['year']}' to integer for model '{model_name}'. Keeping as string."
                                        )
                                        # If conversion fails, it remains as string

                                    # Convert price to integer, removing '$' and ','
                                    if car_data["price"] != "Price not found":
                                        price_value = (
                                            car_data["price"]
                                            .replace("$", "")
                                            .replace(",", "")
                                        )
                                        try:
                                            car_data["price"] = int(price_value)
                                        except ValueError:
                                            print(
                                                f"Warning: Could not convert price '{car_data['price']}' to integer for model '{model_name}'. Keeping as string."
                                            )
                                            # If conversion fails, it remains as string
                                    else:
                                        car_data["price"] = (
                                            None  # Or keep "Price not found" as string, or 0, depending on desired behavior
                                        )

                                    company_name = (
                                        make.capitalize()
                                    )  # Company name for key
                                    if (
                                        company_name not in company_cars_data
                                    ):  # Initialize list if company key doesn't exist
                                        company_cars_data[company_name] = []
                                    company_cars_data[company_name].append(
                                        car_data
                                    )  # Append car data to company's list

                                else:
                                    print(
                                        "Warning: 'div' tag with class 'new-car-model-card-name' not found inside 'a' tag."
                                    )
                                    continue  # Skip to the next model if inner div is missing

                            else:
                                print(
                                    "Warning: 'a' tag with data-card-link not found in model_name_element."
                                )
                                continue  # Skip to the next model if <a> tag is missing

                    # Output the extracted data to console for each make (still printing models_data, but it's not used for final output)
                    print(f"\nExtracted data for {make.capitalize()} from JSON:")
                    pprint(
                        company_cars_data.get(make.capitalize(), [])
                    )  # Print from company_cars_data directly

                else:
                    print(
                        f"Warning: 'results' key not found or empty in {filename}. Skipping file content extraction."
                    )

        else:
            print(
                f"Data file for {make.capitalize()} does not exist.  Make sure {filename} is in the data directory."  # Adjusted print statement
            )

    # After processing all makes, save company_cars_data to complete.json in the root directory
    complete_filepath = "complete.json"  # Changed to save in root directory
    with open(complete_filepath, "w") as outfile:
        json.dump(
            company_cars_data, outfile, indent=4
        )  # Save company_cars_data to JSON

    print(
        f"\nAll car data from all makes saved to: {complete_filepath}"
    )  # Adjusted print statement
    print("\nProcess complete.")

else:
    print(
        "Error: USERNAME and PASSWORD environment variables not set. "
        "Make sure you have a .env file with USERNAME and PASSWORD defined."
    )
