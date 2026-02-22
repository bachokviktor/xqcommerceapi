from io import BytesIO
from PIL import Image

def create_testing_image():
    """
    This function creates in-memory image
    and returns it.
    """
    testing_file = BytesIO()
    testing_image = Image.new("RGBA", size=(50, 50), color=(255, 0, 0))
    testing_image.save(testing_file, "png")
    testing_file.name = "testing_image.png"
    testing_file.seek(0)

    return testing_file
