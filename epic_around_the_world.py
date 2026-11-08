import requests

API_KEY = "DEMO_KEY"


def get_epic_photos(api_key, date):
    url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def get_region(longitude):
    if -150 <= longitude < -30:
        return "Americas"
    elif -30 <= longitude < 60:
        return "Africa and Europe"
    elif 60 <= longitude < 150:
        return "Asia"
    else:
        return "Pacific"


def count_photos_by_region(photos):
    counts = {}
    for photo in photos:
        longitude = photo["centroid_coordinates"]["lon"]
        region = get_region(longitude)
        counts[region] = counts.get(region, 0) + 1
    return counts


def build_image_url(photo):
    date = photo["date"][:10].replace("-", "/")
    return f"https://epic.gsfc.nasa.gov/archive/natural/{date}/png/{photo['image']}.png"


def print_timeline(photos):
    for photo in photos:
        time = photo["date"][11:]
        region = get_region(photo["centroid_coordinates"]["lon"])
        print(f"{time} | {region} | {build_image_url(photo)}")
    print("\nPhotos per region:")
    for region, count in count_photos_by_region(photos).items():
        print(f"{region}: {count}")


def main():
    date = input("Enter a date (YYYY-MM-DD): ")
    photos = get_epic_photos(API_KEY, date)
    if photos is None:
        print("Sorry, the request failed. Check the date format and your API key.")
    elif len(photos) == 0:
        print("No photos were taken on that date. Try another one.")
    else:
        print(f"EPIC took {len(photos)} photos on {date}.\n")
        print_timeline(photos)


main()
