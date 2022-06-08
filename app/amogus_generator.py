import random
from typing import Tuple, List
from PIL import Image

from app.helpers import unique_results
from app.image_generator import AmogusImageGenerator


class Amogus:
    def __init__(self, name: str = 'amogus'):
        self._name = name
        self._image = None

    @property
    def name(self) -> str:
        """
        Return Amogus name
        :return string with Amogus name
        """
        return self._name

    @property
    def image(self) -> Image:
        """
        Return Amogus image. If image wasn't generated yet - generate and return
        :return PIL Image object with amogus image
        """
        if self._image is None:
            self.generate_image()
        return self._image

    def generate_image(self) -> None:
        """
        Generate image basing on name
        """
        if self._image is None:
            image_generator = AmogusImageGenerator(self.name)
            self._image = image_generator.generate_image()


class AmogusFactory:
    name = 'amogus'

    def generate_amogus(self, action: str = None) -> Amogus:
        """
        Generate Amogus with random name.
        :param action: how to generate Amogus name: extend basic name, cut it or cut and mirror it.
        In case of None action is chosen semi-randomly with weights from original video.
        :returns Amogus object with random name
        """
        if action is None:
            action = random.choices(['extend', 'cut', 'mirror'], weights=[10, 1, 1])[0]

        name = self.generate_amogus_name(action)

        if name == self.name:
            return self.generate_amogus(action)

        return Amogus(name)

    def generate_amogus_name(self, action):
        """
        Generates amogus name
        :param action: how to generate Amogus name: extend basic name, cut it or cut and mirror it.
        :return: input_string with name
        """
        if action == 'extend':
            return self.extend_amogus_name()
        elif action == 'cut':
            return self.cut_amogus_name()
        elif action == 'mirror':
            return self.mirror_amogus_name()
        else:
            raise ValueError('action must be extend, cut, mirror or None (for random action)')

    @unique_results(cache_size=100)
    def extend_amogus_name(self) -> str:
        """
        Generate Amogus name by extending base name. Basic name can be extended with prefix and/or postfix
        which are generated from base name. Base name itself can also be cut.
        :return: input_string with new Amogus name
        """
        is_add_prefix, is_add_postfix, is_cut_middle = self.get_random_trasformation_parameters()

        result_name = ''
        if is_add_prefix:
            prefix = self.get_random_substring(cut_from_begin=False)
            result_name += prefix
        if is_cut_middle:
            result_name += self.get_random_substring()
        if is_add_postfix:
            postfix = self.get_random_substring(cut_from_end=False)
            result_name += postfix
        return result_name

    @unique_results(cache_size=10)
    def cut_amogus_name(self) -> str:
        """
        Generate Amogus name by cutting base name from beginning and/or end.
        :return: input_string with new Amogus name
        """
        return self.get_random_substring()

    @unique_results(cache_size=10)
    def mirror_amogus_name(self) -> str:
        """
        Generate Amogus name by cutting base name from beginning and/or end and mirroring it.
        :return: input_string with new Amogus name
        """
        name_part = self.get_random_substring()
        if name_part.startswith('a') and name_part.endswith('s'):
            return name_part[::-1]
        elif name_part.startswith('a'):
            return name_part + name_part[-2::-1]
        elif name_part.endswith('s'):
            return name_part[-1:0:-1] + name_part
        else:
            if random.getrandbits(1):
                return name_part + name_part[-2::-1]
            else:
                return name_part[-1:0:-1] + name_part

    def get_random_trasformation_parameters(self) -> Tuple[int, int, int]:
        """
        Generate random parameters for extend_amogus_name function. Get random 3-bit number (except 0), where each bit
        defines 1 parameter
        :return: tuple with 3 ints equal to 0 or 1
        """
        seed = random.choice(range(1, 8))
        is_add_prefix = seed & 0b001
        is_add_postfix = seed >> 1 & 0b001
        is_cut_middle = seed >> 2 & 0b001
        return is_add_prefix, is_add_postfix, is_cut_middle

    def get_random_substring(self, name: str = None, cut_from_begin: bool = True, cut_from_end: bool = True) -> str:
        """
        Generate random substring of given input_string
        :param name: input_string to generate substrings. If name is None - use basic name
        :param cut_from_begin: allow generation to cut name from beginning
        :param cut_from_end: allow generation to cut name from end
        :return: randomly generated substring of name
        """
        name = name or self.name
        if cut_from_begin:
            weights_for_begin_cut = self.get_pseudonormal_weights(name[:-1])
            begin_offset = random.choices(range(len(name) - 1), weights=weights_for_begin_cut)[0]
        else:
            begin_offset = 0
        if cut_from_end:
            weights_for_end_cut = self.get_pseudonormal_weights(name[begin_offset + 1:])
            end_offset = random.choices(range(begin_offset + 1, len(name)), weights=weights_for_end_cut)[0]
        else:
            end_offset = None

        return name[begin_offset:end_offset]

    def get_pseudonormal_weights(self, s: str) -> List[int]:
        """
        Calculate weights for random.choices. Weights should resemble normal distribution
        :param s: input_string for which weights are calculated
        :return: list of ints representing weights
        """
        mid_index = len(s) // 2
        is_len_even = len(s) % 2 == 0
        if is_len_even:
            return list(range(1, mid_index + 1)) + list(range(mid_index, 0, -1))
        else:
            return list(range(1, mid_index + 2)) + list(range(mid_index, 0, -1))
