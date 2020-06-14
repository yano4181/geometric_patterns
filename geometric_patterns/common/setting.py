# -*- coding: utf-8 -*-
"""Common setting."""
import pathlib
import json
from jsonschema import validate


class ImgSetting:
    """The setting for images.

    Args:
      number (int): The sequel number for the image
      img_file_path_without_ext (str): The image file path
          without the extention and the sequel number
      params (dict): The parameters from the json file
      IMG_DIR (str): The directory name for the images
      IMG_EXT (str): The extention for the images
      PRM_DIR (str): The directory name for the json file
      PRM_EXT (str): The extention for the json file
    """
    IMG_DIR = '/imgs/'
    IMG_EXT = '.png'
    PRM_DIR = '/params/'
    PRM_EXT = '.json'

    def __init__(self, py_file, schema):
        """Initialization.

        Args:
            py_file (str): The python file path
            schema (dict): The json schema for validation
        """
        self.number = 0
        self.set_img_file_path_without_ext(py_file)
        self.set_and_validate_params(
            self.get_params_file_path(py_file), schema)

    def set_img_file_path_without_ext(self, py_file):
        """Set the path for img_file_path_without_ext.

        Args:
            py_file (str): The python file path
        """
        p_py_file = pathlib.Path(py_file)
        img_dir = str(p_py_file.resolve().parent) + self.IMG_DIR
        img_file = p_py_file.stem
        self.img_file_path_without_ext = img_dir + img_file

    def get_params_file_path(self, py_file):
        """Get the parameters file path(json).

        Args:
            py_file (str): The python file path
        Returns:
            str: The parameters file path
        """
        p_py_file = pathlib.Path(py_file)
        prm_dir = str(p_py_file.resolve().parent) + self.PRM_DIR
        prm_file = p_py_file.stem[:7]
        return prm_dir + prm_file + self.PRM_EXT

    def set_and_validate_params(self, params_file_path, schema):
        """Validate the parameters file and set parameters.

        Args:
            params_file_path (str): The python file path
            schema (dict): The json schema for validation
        """
        with open(params_file_path) as f:
            self.params = json.load(f)
            validate(instance=self.params, schema=schema)

    def get_img_file_path(self):
        """Get the image file path.

        Returns:
            str: Image file path
        """
        self.number += 1
        number_padded = '_{0:03d}'.format(self.number)
        return self.img_file_path_without_ext + number_padded + self.IMG_EXT

    def get_param_each(self):
        """Get the value of the parameter "each"

        Returns:
            dict: The value of the parameter "each"
        """
        return self.params['each'][self.number]

    def get_param_each_count(self):
        """Get the count of the parameter "each" list items.

        Returns:
            int: the count of the parameter "each" list items.
        """
        return len(self.params['each'])
