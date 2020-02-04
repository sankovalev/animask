"""Core of animask"""
import numpy as np
import cv2
import imageio

from .utils import read_image
#TODO: typing


# TODO: обобщить на случай нескольких картинок (делать коллаж) [как отдельный класс]
    # TODO: рисовать маску не поверх изображения, а рядом
class Animask:
    """
    Base class for animask.
    """

    def __init__(self,
                 image,
                 bg_beta=0.5,
                 mask_rgb_color=None):
        """
        Create instance.
        Arguments:
            image {str|np.ndarray} -- image or path to image
        Keyword Arguments:
            bg_beta {float} -- mask opacity (default: {0.5})
            mask_rgb_color {tuple} -- RGB mask color in animation (default: {None})
        """
        if bg_beta < 0.0 or bg_beta > 1.0:
            raise ValueError("'bg_beta' must be from 0 to 1")
        if mask_rgb_color is not None:
            if len(mask_rgb_color) != 3:
                raise ValueError("'mask_rgb_color' must has format (R, G, B)")
        if isinstance(image, str):
            image = read_image(image)
        image = np.asarray(image, dtype=np.uint8)
        self.image = image
        self.mask_size = self.image.shape[:2]
        self.bg_beta = bg_beta
        self.mask_rgb_color = mask_rgb_color
        self.masks = list()
        self.annotations = list()

    def _get_epoch(self):
        return len(self.masks) + 1

    def _get_layers(self):
        layers = list()
        for mask in self.masks:
            if len(mask.shape) == 2:
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            if self.mask_rgb_color:
                indices = np.where(mask != (0, 0, 0))
                mask[indices[0], indices[1], :] = self.mask_rgb_color
            layer = cv2.addWeighted(src1=self.image,
                                    alpha=0.9,
                                    src2=mask,
                                    beta=self.bg_beta,
                                    gamma=0)
            layers.append(layer)
        return layers

    def _add_annotations(self, layers):
        # TODO: переделать, чтобы всегда было видно аннотации
        for i in np.arange(len(layers)):
            layers[i] = cv2.putText(img=layers[i],
                                    text=self.annotations[i],
                                    org=(25, 25),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=2,
                                    color=(150, 0, 0),
                                    thickness=2,
                                    lineType=cv2.LINE_AA)
        return layers

    def add(self, mask, desc=None):
        """
        Call this method every epoch to add predicted mask.
        Arguments:
            mask {np.ndarray} -- predicted mask for original image
        Keyword Arguments:
            desc {str} -- description of current epoch; 'epoch [N]' if None (default: {None})
        """
        mask = np.asarray(mask, dtype=np.uint8) * 255
        mask = cv2.resize(mask, self.mask_size[:2])
        if desc is None:
            epoch = str(self._get_epoch())
            desc = "epoch {0}".format(epoch)
        self.masks.append(mask)
        self.annotations.append(str(desc))

    def get_image(self):
        """
        Call this method to get original image for predictions.
        """
        return self.image

    def save(self, filepath, duration=0.5, with_background=False, with_annots=True):
        """
        Save GIF for current animask state.
        Call this method no more than once per epoch.
        Arguments:
            filepath {str} -- path where to save GIF
        Keyword Arguments:
            duration {float} -- seconds to show one epoch (default: {0.5})
            with_background {bool} -- show background under mask (default: {False})
            with_annots {bool} -- show annotations (default: {True})
        """
        layers = self.masks
        if with_background:
            layers = self._get_layers()
        if with_annots:
            layers = self._add_annotations(layers)
        imageio.mimsave(filepath, layers, duration=duration)
