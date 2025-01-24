import json


def get_all_tags_from_json(filename="complete.json"):
    """
    Extracts all unique tags (keys) from all levels of a JSON file.

    Args:
        filename (str, optional): The name of the JSON file. Defaults to "complete.json".

    Returns:
        list: A list of unique tags (keys) found in the JSON file.
              Returns an empty list if the file is not found or is not valid JSON.
    """
    tags = set()  # Use a set to store unique tags
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            def extract_tags_recursive(item):
                if isinstance(item, dict):
                    for key in item.keys():
                        tags.add(key)  # Add the key to the set
                        extract_tags_recursive(item[key])  # Recursively check the value
                elif isinstance(item, list):
                    for element in item:
                        extract_tags_recursive(
                            element
                        )  # Recursively check each element in the list

            extract_tags_recursive(
                data
            )  # Start the recursive extraction from the root data
            return sorted(
                list(tags)
            )  # Convert set to list and sort it for consistent output

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from file '{filename}'.")
        return []


if __name__ == "__main__":
    all_tags = get_all_tags_from_json()
    if all_tags:
        print("All unique tags found in the JSON file:")
        for tag in all_tags:
            print(tag)
