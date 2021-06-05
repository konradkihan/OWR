from os.path import join, dirname, abspath
from os import listdir


class ImageRecgonition:
    def __init__(self, path: str):
        self.path = path
        

    def find_categories(self) -> list:
        # look for all subdirectories and name categories from them 
        return [ d for d in listdir(join(dirname(abspath(__file__)), self.path)) ]


if __name__ == "__main__":
    ImageRecgonition("images").find_categories()
