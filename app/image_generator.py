from typing import List
from PIL import Image

BONE_UP_SYMBOL_NAME = 'bone_up'
BONE_DOWN_SYMBOL_NAME = 'bone_down'
block_width, block_height = Image.open('images/a.png').size


class AmogusImageGenerator:
    def __init__(self, name: str):
        self.name = name

    def generate_image(self) -> Image:
        """
        Create image for given name.
        :return: PIL image
        """
        image_block_names = self.get_list_of_image_parts()
        image = self.construct_image(image_block_names)
        return image

    def get_list_of_image_parts(self) -> List[str]:
        """
        Determine which sub-images should construct requested image
        If first letter is not 'a' and last is not 's' - prepend/append image with bone
        :return: list of sub-image names
        """
        image_parts = list(self.name)
        if not self.name.startswith('a'):
            image_parts.insert(0, 'bone_up')
        if not self.name.endswith('s'):
            image_parts.append('bone_down')

        return image_parts

    def construct_image(self, image_blocks: List[str]) -> Image:
        """
        Determine image size and construct image by merging several sub-images
        :param image_blocks: list of block names
        :return: PIL Image object
        """
        num_of_blocks_in_image = len(image_blocks)
        image_height = block_height * num_of_blocks_in_image

        amogus_image = Image.new('RGBA', (block_width, image_height))

        for number, symbol in enumerate(image_blocks):
            current_image = Image.open(f'images/{symbol}.png')
            amogus_image.paste(current_image, (0, number * block_height))

        return amogus_image
