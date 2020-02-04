"""Utilities"""
import cv2

def read_image(filepath):
    """
    Just read image as RGB
    """
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("Can't read 'image', there is no such path!")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
