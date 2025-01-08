import os
import pathlib
import random
import string


def generate_random_string(length: int = 16):
    """
    Generate a random string of fixed length using alphanumeric characters.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_filename(instance, filename: str, subdir: str = "other") -> str:
    """
    Generate a short random string for the uploaded file name while keeping the extension.
    Allows specifying a custom subdirectory.

    Use like this:

    image = models.ImageField(
        upload_to=partial(generate_random_filename, subdir="services/images/")
    )
    """
    ext: str = pathlib.Path(filename).suffix
    random_name = f"{generate_random_string()}{ext}"
    return os.path.join(subdir, random_name)
