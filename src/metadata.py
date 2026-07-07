import exifread
from datetime import datetime

def convert_to_decimal(coord,ref):
    d = float(coord.values[0].num) / float(coord.values[0].den)
    m = float(coord.values[1].num) / float(coord.values[1].den)
    s = float(coord.values[2].num) / float(coord.values[2].den)

    decimal = d+m / 60 + s/3600

    if ref in ["S" , "W"]:
        decimal *= -1

    return decimal


def get_metadata(image_path):
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f)

    metadata = {}

    metadata["datetime"] = datetime.strptime(
        str(tags["EXIF DateTimeOriginal"]),
        "%Y:%m:%d %H:%M:%S"
    )

    metadata["latitude"] = convert_to_decimal(
        tags["GPS GPSLatitude"],
        str(tags["GPS GPSLatitudeRef"])
    )

    metadata["longitude"] = convert_to_decimal(
        tags["GPS GPSLongitude"],
        str(tags["GPS GPSLongitudeRef"])
    )

    return metadata

