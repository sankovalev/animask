"""Tests for Animask base class"""
import os
import pytest
import cv2
import numpy as np

from animask import Animask


class TestAnimask:
    """
    One test == one method.
    """

    @classmethod
    def setup_class(cls):
        """
        Executed before all methods of the class.
        """
        cls.f_image = os.path.abspath("tests/images/image.png")
        cls.f_masks = [
            os.path.abspath("tests/images/mask0.tif"),
            os.path.abspath("tests/images/mask1.tif"),
            os.path.abspath("tests/images/mask2.tif")
            ]

    @classmethod
    def _read_image(cls, filepath, channels=3):
        """
        Helper function for tests.
        """
        img = cv2.imread(filepath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if channels == 1:
            img = img[:, :, 0]
        return img

    @pytest.mark.parametrize("bg_beta", [0, 0.5, 1])
    @pytest.mark.parametrize("mask_rgb_color", [(1, 1, 1), (255, 0, 0), None])
    def test_animask_init(self, bg_beta, mask_rgb_color):
        """
        Test init parameters.
        """
        Animask(image=self.f_image,
                bg_beta=bg_beta,
                mask_rgb_color=mask_rgb_color)

    @pytest.mark.parametrize("bg_beta, mask_rgb_color", [
        pytest.param(-1, (255, 255, 255), marks=pytest.mark.xfail),
        pytest.param(.5, (255, 255, 255), marks=pytest.mark.xfail),
        pytest.param(.5, (255, 255), marks=pytest.mark.xfail)
    ])
    def test_animask_init_bad_params(self, bg_beta, mask_rgb_color):
        """
        When initializing with incorrect parameters, an exception is thrown.
        """
        Animask(image=self.f_image,
                bg_beta=bg_beta,
                mask_rgb_color=mask_rgb_color)

    def test_animask_get_image(self):
        """
        Check that original image is correct.
        """
        animated = Animask(image=self.f_image)
        original_image = self._read_image(self.f_image)
        assert np.array_equal(original_image, animated.get_image())

    @pytest.mark.parametrize("channels", [1, 3])
    def test_animask_add(self, channels):
        """
        The mask can be either single-channel or have RGB channels.
        """
        animated = Animask(image=self.f_image)
        masks = list()
        for file in self.f_masks:
            mask = self._read_image(file, channels=channels)
            masks.append(mask)
            animated.add(mask)
        assert len(masks) == len(animated.masks)

    @pytest.mark.parametrize("duration", [0.5, 1, 5])
    @pytest.mark.parametrize("with_background", [False, True])
    @pytest.mark.parametrize("with_annots", [False, True])
    def test_animask_save(self, duration, with_background, with_annots):
        """
        Test all possible combinations of output GIF.
        """
        animated = Animask(image=self.f_image, mask_rgb_color=(255, 0, 0))
        for file in self.f_masks:
            animated.add(self._read_image(file, channels=1))
        gif_name = os.path.abspath("tests/gifs/d:{0}_bg:{1}_a:{2}.gif".format(duration,
                                                                              with_background,
                                                                              with_annots))
        animated.save(gif_name, duration, with_background, with_annots)
