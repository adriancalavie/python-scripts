import os
from PIL import Image
from typing import TypeVar
import inquirer
import configparser

# Defining the keys and values for the dictionary that will be returned by the get_prompts_from_user()
# function.
# Keys:
IMAGE_PATH = "image"
SELECTED_FORMATS = "selected formats"

# Supported extensions:
KNOWN_FORMATS = ['png', 'jpeg', 'gif', 'webp']
# A list of formats that support transparency.
TRANSPARENCY_CAPABLE_FORMATS = ['webp', 'png']

# Settings:
is_checking_formats = bool(False)
check_current_format_in_selection = bool(False)


def get_prompts_from_user():
    """
    It asks the user for an image path and a list of formats to export to
    :return: A dictionary with the user's answers.
    """
    prompts = [
        inquirer.Path(
            IMAGE_PATH,
            message='Insert the image path',
            path_type=inquirer.Path.FILE,
            exists=True,
        ),
        inquirer.Checkbox(
            SELECTED_FORMATS,
            message='Select the formats you want to export to',
            choices=KNOWN_FORMATS,
            carousel=True
        )
    ]
    return inquirer.prompt(prompts)


def get_image(image_path: str):
    """
    It takes a path to an image, checks if the extension is in a list of known formats, and if it is, it
    returns an Image object

    :param image_path: The path to the image file
    :type image_path: str
    :return: An image object.
    """
    _, extension = os.path.splitext(image_path)
    if extension.strip('.') not in KNOWN_FORMATS:
        raise ValueError("{} is not a known format.".format(extension))

    return Image.open(image_path)


def check_formats(current_format: str, formats: list[str]):
    """
    It checks if the current format is in the list of formats, and if it is not, it raises a ValueError

    :param current_format: str
    :type current_format: str
    :param formats: list[str]
    :type formats: list[str]
    """

    if formats == []:
        raise ValueError("No formats selected.")

    if set(formats) | set(KNOWN_FORMATS) != set(KNOWN_FORMATS):
        raise ValueError(
            "Unknown format(s) encountered: {}".format(KNOWN_FORMATS - formats))

    if check_current_format_in_selection and current_format.lower() in formats:
        raise ValueError(
            "The selected image already is in {} format.".format(current_format))


def save_images(image: Image, formats: list[str]):
    """
    It takes an image and a list of formats, checks if the image format is in the list of formats, and
    then saves the image in each of the formats

    :param image: Image - the image to be saved
    :type image: Image
    :param formats: list[str]
    :type formats: list[str]
    """
    if is_checking_formats:
        check_formats(image.format, formats)

    image_name = image.filename.split('.')[0]

    for format in formats:
        saved_image_name = image_name + '.' + format.lower()
        if format not in TRANSPARENCY_CAPABLE_FORMATS:
            image.info.pop('background', None)
        if format == 'jpeg':
            rgb_image = image.convert("RGB")
            rgb_image.save(saved_image_name, format.lower(), lossless=True)
            return
        image.save(saved_image_name, format.lower(), lossless=True, save_all=True)


def convert_image():
    """
    It prompts the user for an image path and a list of image formats to convert to, then it loads the
    image, converts it to the selected formats, and saves the converted images in the same directory as
    the source image
    """
    answers = get_prompts_from_user()

    image_path = answers[IMAGE_PATH]
    selected_formats = answers[SELECTED_FORMATS]

    image = get_image(image_path)

    if image == None:
        raise ValueError("Could not load image")

    save_images(image, selected_formats)
    print("Images are now saved in the source image's directory")


def init_settings():
    """
    It reads the convert.config file and sets the global variables is_checking_formats and
    check_current_format_in_selection to the values in the file
    """
    try:
        config = configparser.ConfigParser()
        # Working directory is the parent directory of this file's directory
        config.read('image_convert/convert.ini')

        global is_checking_formats
        global check_current_format_in_selection

        is_checking_formats = bool(
            config.get('convert-image',
                       f'{is_checking_formats=}'.split('=')[0]))
        check_current_format_in_selection = bool(
            config.get('convert-image',
                       f'{check_current_format_in_selection=}'.split('=')[0]))
    except:
        print("Could not find config file. Default settings loaded")


if __name__ == '__main__':
    init_settings()
    convert_image()
