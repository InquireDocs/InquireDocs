from pathlib import Path
import sys


class Settings():
    """ Application settings
    """

    def __init__(self):
        self.__app_path = Path.home().joinpath('.inquiredocs')
        self.__app_path.mkdir(parents=True, exist_ok=True)

        self.__data_path = self.__app_path.joinpath('data')
        self.__data_path.mkdir(parents=True, exist_ok=True)

        self.__model_path = self.__app_path.joinpath('model')
        self.__model_path.mkdir(parents=True, exist_ok=True)

    def get_app_path(self):
        """ Public getter for __app_path
        Path for app config files and data.
        """
        return self.__app_path

    def get_data_path(self):
        """ Public getter for __data_path
        Path for all data generated for the application.
        """
        return self.__data_path

    def get_model_path(self):
        """ Public getter for __model_path
        Path for files related to the LLM used to answer questions.
        """
        return self.__model_path


#################
# Global instance
config = Settings()
