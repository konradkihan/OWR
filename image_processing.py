"""
This is main code that is responsible for reading and converting images and feeding neural network with them.
Konrad Kihan 2021
"""
from os import listdir, rename
from os.path import exists, join, dirname, abspath
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor
import functools


"""
returns a list of all images in all directiories that that Image_manager will be fed with
""" 
def seek_images(directory: str) -> list:
    correctExt: list = ("webp", "jpg", "png")
    # look for all directiories
    dirs: list = [
        join(dirname(abspath(__file__)), directory)
        +"\\"+
        d for d in listdir(join(dirname(abspath(__file__)), directory))
    ]
    files : list = []
    for dir in dirs:
        try:     
            f_dir = listdir(dir)
        except NotADirectoryError as e:
                exit(f"{e} - data is not sorted properly")

        for f in f_dir:
            if f.endswith(correctExt):
                if not f[0].isalnum():
                    rename(f"{dir}\{f}", f"{dir}\_{f[1:]}")
                files.append(f"{dir}\{f}")
            



    return files
# TODO optimize process                                                                                                                                                                         (maybe)


"""
reads and converts images using PIL module
"""
class Image_manager():
    def __init__(self, 
                imagePath: str,
                imageExtension: str,
                newImage: str = None, 
                createCopy: bool = True):
        if not exists(self.image):
            self.image: str = join(dirname(abspath(__file__)), imagePath)
        
        self.imgExt: str = imageExtension,
        self.extLen: int = len(imageExtension)+1                # it is a length of extension including the dot character
        if exists(self.image):
            if createCopy:                                      # if user wants to create copy and gives custom name
                self.newImage = newImage
            elif newImage is None and createCopy:               # if user wants to create copy but does not give custom name
                self.newImage = f"{self.image[:self.extLen]}_copy.{self.imgExt}"
            else:                                               # if user does not want to create copy
                self.newImage = self.image
        else:
            exit(f"File {imagePath} does not exist. Exitting.")
        print(self.newImage)


    def size(self) ->  tuple:
        with Image.open(self.image) as img:
            return img.size     # (width, height)
    

    def img_resize(self, size: tuple = (300, 300)) -> None:
        self.size: tuple = size
        with Image.open(self.image) as img:
            try:
                img.resize(self.size, Image.ANTIALIAS).save(self.newImage)
            except TypeError as e:
                raise f"{e} - wrong size type {size}"


    def convert_greyscale(self) -> None:
        with Image.open(self.image) as img:
            img.convert("L").save(self.newImage)


    def rotation(self, rotation: set, nameSuffix: bool = True) -> None:
        with Image.open(self.image) as img:
            for deg in rotation:
                try:
                    if nameSuffix: 
                        name: str = f"{self.newImage[:self.extLen]}_rot{abs(deg)}.{self.imgExt}"
                    else: 
                        name: str = self.newImage
                    img.rotate(abs(deg)).save(name)
                except TypeError as e:
                    raise f"{e} - wrong rotation angle {deg}"


    def flipping(self, nameSuffix: bool = True) -> None:
        with Image.open(self.image) as img:
            if nameSuffix: 
                name: str = f"{self.newImage[:self.imgExt]}_flip.{self.imgExt}"
            else: 
                name: str = self.newImage
            img.transpose(Image.FLIP_LEFT_RIGHT).save(name)


    def color_enhance(self, level: int, nameSuffix: bool = True) -> None:
        with Image.open(self.image) as img:
            if nameSuffix:
                name: str = f"{self.newImage[:self.extLen]}_enh_by{level}.{self.imgExt}"
            else:
                name: str = self.newImage
            contrast = ImageEnhance.Contrast(img)
            contrast.enhance(level).save(name)


# TODO deciede if setting new method in Image_manager for bulk processing wouldn't be more effective
"""# makes bulk processing images easier"""
def process_image(imagePath: str,
                imageExtension: str,
                newImage: str = None, 
                createCopy: bool = True) -> None:
    d = Image_manager(imagePath).convert_greyscale()
    

if __name__ == "__main__":
    images = seek_images("images")
    print(images)
    imgList: list = seek_images("images")
    with ThreadPoolExecutor() as executor:
        executor.map(functools.partial(process_image("images"), ))
    