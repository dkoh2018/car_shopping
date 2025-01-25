import requests
from bs4 import BeautifulSoup
import json
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def scrape_car_models(make, username, password, base_url, data_dir):
    """
    Scrapes car models and prices for a given make from cars.com research page
    using Oxylabs proxy and saves the data to a JSON file.

    Args:
        make (str): The car make to scrape (e.g., "tesla").
        username (str): Oxylabs username.
        password (str): Oxylabs password.
        base_url (str): Base URL for cars.com research.
        data_dir (str): Directory to save the JSON output.

    Returns:
        list: A list of dictionaries containing model and price data, or None if scraping fails.
    """
    url_make = make.replace(" ", "_").lower()  # Convert make to URL-friendly format
    url_to_scrape = base_url + url_make + "/"
    payload = {"source": "universal", "url": url_to_scrape}

    try:  # Add try-except block for request
        response = requests.request(
            "POST",
            "https://realtime.oxylabs.io/v1/queries",
            auth=(
                username,
                password,
            ),  # Using the username and password passed as arguments
            json=payload,
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        html_content = response.json()["results"][0]["content"]
        soup = BeautifulSoup(html_content, "html.parser")

        models_data = []
        model_list_items = soup.find_all(
            "spark-card", class_="new-car-lineup-model-card"
        )

        for item in model_list_items:
            model_name_element = item.find(
                "div",
                {
                    "data-qa": lambda x: x
                    and x.startswith(f"{make.lower().replace(' ', '_')}-")
                },
            )  # URL-safe make for data-qa prefix
            if model_name_element:
                link_element = model_name_element.find("a", {"data-card-link": ""})
                if link_element:
                    model_name_div = link_element.find(
                        "div", class_="new-car-model-card-name"
                    )
                    if model_name_div:
                        model_year_model_name = model_name_div.text.strip()
                        parts = model_year_model_name.split(" ", 1)
                        model_year = parts[0] if parts else "Year N/A"
                        model_name = (
                            parts[1] if len(parts) > 1 else model_year_model_name
                        )

                        price_element = item.find(
                            "div", class_="new-car-model-card-price"
                        )
                        price = (
                            price_element.text.strip()
                            if price_element
                            else "Price not found"
                        )

                        models_data.append(
                            {"year": model_year, "model": model_name, "price": price}
                        )
                    else:
                        print(
                            f"Warning: 'div' tag with class 'new-car-model-card-name' not found inside 'a' tag for {make}."
                        )  # More specific warning
                else:
                    print(
                        f"Warning: 'a' tag with data-card-link not found in model_name_element for {make}."
                    )  # More specific warning

        filename = f"{make.lower().replace(' ', '_')}.json"  # URL-safe filename
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "w") as outfile:
            json.dump(
                {"results": [{"content": html_content}]}, outfile, indent=4
            )  # Save full content for debugging if needed
        print(f"Data for {make.capitalize()} saved to: {filepath}")

        return models_data  # Return the scraped data

    except requests.exceptions.RequestException as e:  # Catch request exceptions
        print(f"Request error scraping {make.capitalize()}: {e}")
        return None  # Return None to indicate scraping failure
    except json.JSONDecodeError as e:  # Catch JSON decode errors
        print(f"JSON decode error for {make.capitalize()}: {e}")
        return None
    except Exception as e:  # Catch any other unexpected errors
        print(f"Unexpected error scraping {make.capitalize()}: {e}")
        return None


if __name__ == "__main__":
    # Example usage if you want to run the scraper module directly for testing
    USERNAME = os.environ.get("USERNAME")  # Get Oxylabs username from .env
    PASSWORD = os.environ.get("PASSWORD")  # Get Oxylabs password from .env
    BASE_URL = "https://www.cars.com/research/"
    MAKES = [
        "Acura",
        "Alfa_Romeo",
        "Aston_Martin",
        "Audi",
        "Bentley",
        "BMW",
        "Bugatti",
        "Buick",
        "Cadillac",
        "Chevrolet",
        "Chrysler",
        "Dodge",
        "Ferrari",
        "FIAT",
        "Fisker",
        "Ford",
        "Genesis",
        "GMC",
        "Honda",
        "Hyundai",
        "INEOS",
        "INFINITI",
        "Jaguar",
        "Jeep",
        "Kia",
        "Lamborghini",
        "Land_Rover",
        "Lexus",
        "Lincoln",
        "Lotus",
        "Lucid",
        "Maserati",
        "Mazda",
        "McLaren",
        "Mercedes_Benz",
        "MINI",
        "Mitsubishi",
        "Nissan",
        "Polestar",
        "Porsche",
        "RAM",
        "Rivian",
        "Rolls_Royce",
        "Subaru",
        "Suzuki",
        "Tesla",
        "Toyota",
        "VinFast",
        "Volkswagen",
        "Volvo",
    ]
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    if USERNAME and PASSWORD:  # Check if USERNAME and PASSWORD are loaded
        for make in MAKES:
            scrape_car_models(make, USERNAME, PASSWORD, BASE_URL, data_dir)
    else:
        print(
            "Error: USERNAME and PASSWORD environment variables not set. "
            "Make sure you have a .env file with USERNAME and PASSWORD defined."
        )
