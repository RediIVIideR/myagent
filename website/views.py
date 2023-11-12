from django.shortcuts import render
from .models import *
from django.template import loader
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from collections import Counter
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from io import BytesIO
import math
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def remove_non_unique(lst):
    counter = Counter(lst)
    unique_elements = [elem for elem in lst if counter[elem] == 1]
    return unique_elements


def convert_price_to_number(price):
    price_str = price.replace("AED ", "", 2)
    if "EUR" in price_str:
        return None
    if "YEAR" in price_str:
        return None
    if "K" in price_str:
        return float(price_str.replace("K", "")) * 1000
    elif "M" in price_str:
        return float(price_str.replace("M", "")) * 1000000
    else:
        return None


def filter_objects_within_range(min_price, max_price, objects):
    filtered_objects = []
    for obj in objects:
        price_in_number = convert_price_to_number(obj.property_starting_price_aed)
        if price_in_number == None:
            continue
        if min_price <= price_in_number <= max_price:
            filtered_objects.append(obj)
    return filtered_objects


def price_conversion(price):
    price = price.upper()
    aed_price = price
    price = price[4:]

    if "REQ" in price:
        return "Request", "Request"

    if "€" in price:
        price = price.replace("€", "", 10)

    if "," in price:
        price = float(price.replace(",", "", 10))
        aed_price = "AED " + str(price / 1000) + "K"

        usd_price = price * 0.27
        usd_price = int(math.ceil(usd_price / 5000.0)) * 5000
        usd_price = "USD " + str(int(usd_price / 1000)) + "K"
        return aed_price, usd_price

    if "K" in price:
        price = price[: price.find("K")]
        price = float(price) * 1000
        usd_price = price * 0.27
        usd_price = int(math.ceil(usd_price / 5000.0)) * 5000
        usd_price = "USD " + str(int(usd_price / 1000)) + "K"
        return aed_price, usd_price
    if "M" in price:
        price = price[: price.find("M")]
        price = float(price) * 1000000
        usd_price = price * 0.27
        usd_price = int(math.ceil(usd_price / 5000.0)) * 5000
        usd_price = "USD " + str(int(usd_price / 1000)) + "K"
        return aed_price, usd_price


def parse_all(request):
    # start_page_url = "https://www.offplan-dubai.com/offplan-projects-in-dubai/#gridview"
    for i in range(5, 11):
        start_page_url = (
            f"https://www.offplan-dubai.com/offplan-projects-in-dubai/page/{i}/"
        )
        print(i)
        resp = requests.get(start_page_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        property_links = soup.find_all("a", class_="color_blue")
        for propertty in property_links:
            link = propertty["href"]
            response = requests.get(link)
            # response = requests.get(
            #     "https://www.offplan-dubai.com/symphony-at-town-square/"
            # )

            soupp = BeautifulSoup(response.text, "html.parser")
            try:
                project_name = soupp.find("h1", class_="w-blogpost-title").text
            except:
                continue
            print(i, project_name)
            existing_object = Property.objects.filter(
                property_name=project_name
            ).first()
            if existing_object:
                continue
            else:
                preview_img_link = soup.find(
                    "a", attrs={"aria-label": project_name}
                ).find("img")["src"]
                print(preview_img_link)
                project_developer = soupp.find("div", class_="dev_name").text
                info = remove_non_unique(
                    soupp.find("div", class_="bg-colors").text.split("\n")
                )
                project_price = info[1]
                project_location = info[3]
                project_type = info[5]
                project_bedrooms = info[7]

                # Highlights
                highlights = remove_non_unique(
                    soupp.find("div", class_="nolist").text.split("\n")
                )
                highlights = "^".join(highlights)

                # Descriptions
                elem = soupp.find_all("div", class_="default-font")

                for el in elem:
                    try:
                        preceding_div = el.find_previous_sibling("div")
                        block = preceding_div.parent.text
                    except:
                        block = el.text
                    print(block)
                    if "Project Details" in block:
                        project_details = remove_non_unique(block.split("\n"))
                        print(block)
                        try:
                            project_details = "^".join(
                                project_details[
                                    project_details.index("Project Details") + 1 :
                                ]
                            )
                        except:
                            project_details = "^".join(
                                project_details[
                                    project_details.index("Project Details:") + 1 :
                                ]
                            )
                    if "Minutes" in block and not "Location" in block:
                        property_location_description = remove_non_unique(
                            block.split("\n")
                        )
                        property_location_description = "^".join(
                            property_location_description[0:]
                        )
                    if "Location" in block:
                        property_location_description = remove_non_unique(
                            block.split("\n")
                        )
                        property_location_description = "^".join(
                            property_location_description[1:]
                        )
                    if "Amenities" in block:
                        amenities = remove_non_unique(block.split("\n"))
                        amenities = "^".join(amenities[1:])
                    if "Interiors and Units" in block or "Interiors & Units" in block:
                        unit_description = remove_non_unique(block.split("\n"))
                        unit_description = "^".join(unit_description[1:])
                    else:
                        unit_description = ""

                # Payment Plan Extraction
                try:
                    property_payment_plan = soupp.find(
                        "h6", class_="w-separator-text", string="Payment Plan"
                    ).parent.parent.parent.text.split("\n")
                except:
                    property_payment_plan = soupp.find_all(
                        "div",
                        class_="table-responsive",
                    )[2].text.split("\n")
                property_payment_plan = remove_non_unique(property_payment_plan)
                property_payment_plan = "^".join(property_payment_plan[1:])
                print(property_payment_plan)

                price = price_conversion(project_price)

                property_object = Property.objects.create(
                    property_name=project_name,
                    property_accommodation_type=project_type,
                    property_location=project_location,
                    property_location_description=property_location_description,
                    property_units=unit_description,
                    property_payment_plan=property_payment_plan,
                    property_bed_number=project_bedrooms,
                    property_description=project_details,
                    property_starting_price_aed=price[0],
                    property_developer=project_developer,
                    property_amenities=amenities,
                    property_highlights=highlights,
                    property_starting_price_usd=price[1],
                    date=timezone.now(),
                )

                response = requests.get(preview_img_link).content
                image_field = getattr(property_object, f"property_image1", None)
                image_field.save(f"1.png", BytesIO(response), save=True)

                photos = soupp.find_all("a", class_="w-gallery-item")
                i = 2
                for photo in photos:
                    response = requests.get(photo["href"])
                    if response.status_code == 200:
                        img_data = response.content

                        image_field = getattr(
                            property_object, f"property_image{i}", None
                        )

                        print("saved")
                        image_field.save(f"{i}.png", BytesIO(img_data), save=True)
                        i += 1

                property_object.save()


def main(request):
    slider = Slider.objects.filter()[0]
    objects = Property.objects.all()[:6]
    context = {"slider_photo": slider, "properties": objects}
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))


def search_property(request):
    keyword = request.GET.get("keyword")
    property_types = request.GET.getlist("type")
    locations = request.GET.getlist("loc")
    min_price = request.GET.get("minprice")
    max_price = request.GET.get("maxprice")
    developers = request.GET.getlist("developer")
    bedrooms = request.GET.getlist("bed")

    developers_list = list(
        set(Property.objects.values_list("property_developer", flat=True))
    )
    locations_list = list(
        set(Property.objects.values_list("property_location", flat=True))
    )
    objects = Property.objects.all()  # Retrieve your data

    if keyword:
        objects = objects.filter(property_name__contains=keyword)
    if min_price:
        objects = objects.filter(property_starting_price_aed__gte=min_price)
    if max_price:
        objects = objects.filter(property_starting_price_aed__lte=max_price)

    q_objects = Q()

    if bedrooms:
        for bedroom in bedrooms:
            q_objects |= Q(property_bed_number__contains=bedroom)

    if developers:
        for developer in developers:
            q_objects |= Q(property_developer__contains=developer)

    if locations:
        for location in locations:
            q_objects |= Q(property_location__contains=location)

    if property_types:
        for prop_type in property_types:
            q_objects |= Q(property_accommodation_type__contains=prop_type)

    if q_objects:
        objects = objects.filter(q_objects)

    # Set the number of items per page
    items_per_page = 6
    paginator = Paginator(objects, items_per_page)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    properties = Property.objects.filter()
    context = {
        "page_obj": page_obj,
        "locations": sorted(locations_list),
        "developers": sorted(developers_list),
    }

    template = loader.get_template("property-list.html")
    return HttpResponse(template.render(context, request))


def search(request):
    keyword = request.GET.get("keyword")
    property_types = request.GET.getlist("type")
    locations = request.GET.getlist("loc")
    min_price = float(request.GET.get("minprice"))
    max_price = float(request.GET.get("maxprice"))
    developers = request.GET.getlist("developer")
    bedrooms = request.GET.getlist("bed")

    developers_list = list(
        set(Property.objects.values_list("property_developer", flat=True))
    )
    locations_list = list(
        set(Property.objects.values_list("property_location", flat=True))
    )
    objects = Property.objects.all()  # Retrieve your data

    if keyword:
        objects = objects.filter(property_name__contains=keyword)

    q_objects = Q()

    if bedrooms:
        for bedroom in bedrooms:
            q_objects |= Q(property_bed_number__contains=bedroom)

    if developers:
        for developer in developers:
            q_objects |= Q(property_developer__contains=developer)

    if locations:
        for location in locations:
            q_objects |= Q(property_location__contains=location)

    if property_types:
        for prop_type in property_types:
            q_objects |= Q(property_accommodation_type__contains=prop_type)

    if q_objects:
        objects = objects.filter(q_objects)

    objects = filter_objects_within_range(min_price, max_price, objects)

    # Set the number of items per page
    items_per_page = 6
    paginator = Paginator(objects, items_per_page)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    properties = Property.objects.filter()
    context = {
        "page_obj": page_obj,
        "locations": locations_list,
        "developers": developers_list,
    }

    template = loader.get_template("search.html")
    return HttpResponse(template.render(context, request))


def show_property(request):
    id = request.GET.get("id")
    project = Property.objects.get(id=id)
    amenities = project.property_amenities.split("^")
    description = project.property_description.split("^")
    location = project.property_location_description.split("^")
    payment_plan = project.property_payment_plan.split("^")
    highlights = project.property_highlights.split("^")
    units = project.property_units.split("^")

    context = {
        "property": project,
        "amenities": amenities,
        "description": description,
        "location": location,
        "payment": payment_plan,
        "highlights": highlights,
        "units": units,
    }
    template = loader.get_template("property.html")
    return HttpResponse(template.render(context, request))


def custom_404(request, exception):
    print(exception)
    context = {}
    template = loader.get_template("404.html")
    return HttpResponse(template.render(context, request))
