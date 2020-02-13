"""Utilities"""
import cv2


def read_image(filepath):
    """
    Just read image as RGB
    """
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("Can't read 'image', there is no such path!")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def write_image(filepath, image):
    """
    Just save image as RGB
    """
    return cv2.imwrite(filepath, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def overlay_mask_on_image(image, mask, beta):
    """
    Result = image + mask
    """
    return cv2.addWeighted(src1=image,
                           alpha=0.9,
                           src2=mask,
                           beta=beta,
                           gamma=0)

def overlay_text_on_image(image, annotation):
    return cv2.putText(img=image,
                       text=annotation,
                       org=(25, 25),
                       fontFace=cv2.FONT_HERSHEY_PLAIN,
                       fontScale=2,
                       color=(150, 0, 0),
                       thickness=2,
                       lineType=cv2.LINE_AA)

