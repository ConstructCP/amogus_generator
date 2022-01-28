import random
from typing import Tuple, List


class Amogus:
    def __init__(self, name: str = 'amogus'):
        self._name = name


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
            action = random.choices(['extend', 'cut', 'mirror'], weights=[9, 9, 5])[0]

        if action == 'extend':
            name = self.extend_amogus_name()
        elif action == 'cut':
            name = self.cut_amogus_name()
        elif action == 'mirror':
            name = self.mirror_amogus_name()
        else:
            raise ValueError('action must be extend, cut, mirror or None (for random action)')

        if name == self.name:
            return self.generate_amogus(action)

        return Amogus(name)

    def extend_amogus_name(self) -> str:
        """
        Generate Amogus name by extending base name. Basic name can be extended with prefix and/or postfix
        which are generated from base name. Base name itself can also be cut.
        :return: string with new Amogus name
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

    def cut_amogus_name(self) -> str:
        """
        Generate Amogus name by cutting base name from beginning and/or end.
        :return: string with new Amogus name
        """
        return self.get_random_substring()

    def mirror_amogus_name(self) -> str:
        """
        Generate Amogus name by cutting base name from beginning and/or end and mirroring it.
        :return: string with new Amogus name
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
        Generate random substring of given string
        :param name: string to generate substrings. If name is None - use basic name
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
        :param s: string for which weights are calculated
        :return: list of ints representing weights
        """
        mid_index = len(s) // 2
        is_len_even = len(s) % 2 == 0
        if is_len_even:
            return list(range(1, mid_index + 1)) + list(range(mid_index, 0, -1))
        else:
            return list(range(1, mid_index + 2)) + list(range(mid_index, 0, -1))
