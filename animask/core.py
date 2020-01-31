import numpy as np
import cv2
import imageio

from .exceptions import ImreadException, InvalidSizeException
#TODO: typing
#TODO: pylint


class Animask:
    """
    Main class for animask.
    """
    # TODO: обобщить на случай нескольких картинок (делать коллаж)

    def __init__(self, image, bg_alpha=0.3, bg_gamma=0):
        """
        Create instance.
        Arguments:
            image {str|np.ndarray} -- path to image or image
        """
        if isinstance(image, str):
            try:
                image = cv2.imread(image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            except Exception as exc:
                raise ImreadException(exc)
        image = np.asarray(image, dtype=np.uint8)
        self.image = image
        self.mask_size = self.image.shape[:2]
        self.bg_alpha = bg_alpha
        self.bg_gamma = bg_gamma
        self.masks = list()
        self.descriptions = list()

    def _get_epoch(self):
        return len(self.masks) + 1

    def _get_layers(self):
        layers = list()
        for mask in self.masks:
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            layer = cv2.addWeighted(src1=self.image,
                                    alpha=self.bg_alpha,
                                    src2=mask,
                                    beta=1.0 - self.bg_alpha,
                                    gamma=self.bg_gamma)
            layers.append(layer)
        return layers

    def _add_annotations(self, layers):
        for i in np.arange(len(layers)):
            layers[i] = cv2.putText(img=layers[i],
                                    text=self.descriptions[i],
                                    org=(10, 20),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=1,
                                    color=(150, 0, 0),
                                    thickness=1,
                                    lineType=cv2.LINE_AA)
        return layers

    def add(self, mask, desc=None):
        """
        Call this method every epoch to add predicted mask.
        """
        mask = cv2.resize(mask, self.mask_size)
        mask = np.asarray(mask, dtype=np.uint8) * 255

        if desc is None:
            epoch = str(self._get_epoch())
            desc = "epoch {0}".format(epoch)
        self.masks.append(mask)
        self.descriptions.append(str(desc))

    def get_image(self, as_tensor=True):
        """
        Call this method to get original image for predictions.
        If you use flag 'as_tensor', the shape will be [1, C, H, W].
        Keyword Arguments:
            as_tensor {bool} -- [description] (default: {True})
        """
        if as_tensor:
            pass
            # T.unsqueeze(0).permute(0,3,1,2) # don't use torch!
        return self.image

    def save(self, filepath, duration=0.5, with_annots=True, with_background=False):
        layers = self.masks
        if with_background:
            layers = self._get_layers()
        if with_annots:
            layers = self._add_annotations(layers)
        imageio.mimsave(filepath, layers, duration=duration)
