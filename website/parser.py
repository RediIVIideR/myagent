import requests
from bs4 import BeautifulSoup
from models import Property
from collections import Counter


def remove_non_unique(lst):
    counter = Counter(lst)
    unique_elements = [elem for elem in lst if counter[elem] == 1]
    return unique_elements


def parse_all():
    start_page_url = "https://www.offplan-dubai.com/offplan-projects-in-dubai/#gridview"
    resp = requests.get(start_page_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    property_links = soup.find_all("a", class_="color_blue")
    for propertty in property_links:
        link = propertty["href"]
        # response = requests.get(link)
        response = requests.get("https://www.offplan-dubai.com/binghatti-lavender/")

        soupp = BeautifulSoup(response.text, "html.parser")

        project_name = soupp.find("h1", class_="w-blogpost-title").text
        project_developer = soupp.find("div", class_="dev_name").text
        info = remove_non_unique(soupp.find("div", class_="bg-colors").text.split("\n"))
        project_price = info[1]
        project_location = info[3]
        project_type = info[5]
        project_bedrooms = info[7]

        # Highlights
        highlights = remove_non_unique(
            soupp.find("div", class_="nolist").text.split("\n")
        )

        # Descriptions
        elem = soupp.find_all("div", class_="default-font")

        for el in elem:
            preceding_div = el.find_previous_sibling("div")
            block = preceding_div.parent.text
            if "Project Details" in block:
                project_details = remove_non_unique(block.split("\n"))
            if "Location" in block:
                property_location_description = remove_non_unique(block.split("\n"))
            if "Amenities" in block:
                amenities = remove_non_unique(block.split("\n"))
            if "Interiors and Units" in block:
                unit_description = remove_non_unique(block.split("\n"))

        # Payment Plan Extraction
        property_payment_plan = soupp.find(
            "h6", class_="w-separator-text", string="Payment Plan"
        ).parent.parent.parent.text.split("\n")
        property_payment_plan = remove_non_unique(property_payment_plan)

        property_object = Property.objects.create(
            property_name=project_name,
            property_accommodation_type=project_type,
            property_location=project_location,
            property_location_description=property_location_description,
            property_units=unit_description,
            property_payment_plan=unit_description,
            property_bed_number=project_bedrooms,
            property_description=project_details,
            property_starting_price_aed=project_price,
            property_developer=project_developer,
            # Add other field values similarly
            date=timezone.now(),  # Set the current timestamp for the 'date' field
        )
        # For FileFields, you will need to provide actual file paths
        # property_object.property_image1.name = "path/to/image1.jpg"
        # property_object.property_image2.name = "path/to/image2.jpg"
        # Add paths to other images similarly

        # Save the instance after updating FileField paths
        property_object.save()

        # photos = soupp.find_all("div", class_="w-gallery-item-img")
        # print(photos)
        break


parse_all()
