from django.utils.text import slugify

locations = ["ACTON", "AJAX-PICKERING", "Hamilton", "hamilton"]

for location in locations:
    slug = slugify(location)
    print(f"{location} -> {slug}")
