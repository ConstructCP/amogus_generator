import pytest
from app.amogus_generator import AmogusFactory, Amogus


class TestAmogusGenerator:
    @pytest.mark.repeat(5)
    def test_get_random_substring(self):
        name = AmogusFactory().get_random_substring()
        assert name in 'amogus', f'Name {name} is not part of "amogus"'

    def test_get_random_substring_cut_begin_false(self):
        name = AmogusFactory().get_random_substring(cut_from_begin=False)
        assert name in 'amogus', f'Name {name} is not part of "amogus"'
        assert name.startswith('a'), 'Name should start with "a" with cut_from_begin=False'

    def test_get_random_substring_cut_end_false(self):
        name = AmogusFactory().get_random_substring(cut_from_end=False)
        assert name in 'amogus', f'Name {name} is not part of "amogus"'
        assert name.endswith('s'), 'Name should start with "a" with cut_from_end'

    @pytest.mark.repeat(5)
    def test_extend_amogus_name(self):
        name = AmogusFactory().extend_amogus_name()
        self.assert_subsequences(name)

    @pytest.mark.repeat(5)
    def test_cut_amogus_name(self):
        name = AmogusFactory().cut_amogus_name()
        assert name in 'amogus', 'Name is not a substring of "amogus"'

    def test_mirror_amogus_name(self):
        name = AmogusFactory().mirror_amogus_name()
        mid_letter_pos = len(name) // 2
        subname = name[:mid_letter_pos + 1]
        assert subname in "amogus" or subname[::-1] in "amogus", 'Name is not a mirrored substring of "amogus"'
        assert name[:mid_letter_pos] == name[:mid_letter_pos:-1]

    @pytest.mark.repeat(5)
    @pytest.mark.parametrize('action', ['extend', 'cut', 'mirror', None])
    def test_amogus_generation(self, action):
        amogus = AmogusFactory().generate_amogus(action)
        assert isinstance(amogus, Amogus)

    @staticmethod
    def assert_subsequences(name: str) -> None:
        # momogugus -> mo mogu gus
        sequence = 'amogus'
        letter_pos = {k: v for k, v in zip(sequence, range(len(sequence)))}
        name_as_letter_codes = list(map(lambda letter: letter_pos[letter], name))
        subsequences_found = 0
        prev_letter_code = name_as_letter_codes[0]
        for letter_code in name_as_letter_codes[1:]:
            if letter_code - prev_letter_code != 1:
                subsequences_found += 1
            prev_letter_code = letter_code
        assert subsequences_found <= 3, 'More than 3 subsequences of "amogus" found'
