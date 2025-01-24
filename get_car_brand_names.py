import re


def extract_car_brands_from_file(filepath="example.txt"):
    """
    Parses a text file to extract car brand names
    from 'data-brand-name' attributes within <a> tags.

    Args:
        filepath (str, optional): The path to the text file.
                                   Defaults to "example.txt".

    Returns:
        list: A list of unique car brand names found in the text.
              Returns an empty list if the file cannot be read.
    """
    brand_names = set()
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            text_content = file.read()
            # Regular expression to find 'data-brand-name' attribute values in <a> tags
            pattern = r'<a data-brand-name="([^"]*)"'
            matches = re.findall(pattern, text_content)
            for match in matches:
                brand_names.add(match)
    except FileNotFoundError:
        print(f"Error: File not found at path: {filepath}")
        return []  # Return empty list if file not found
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []  # Return empty list if there's any other error reading the file
    return list(brand_names)


# Example usage with your example.txt file:
car_brands = extract_car_brands_from_file("example.txt")
print(car_brands)
print(f"\nNumber of unique car brands found: {len(car_brands)}")
