from __future__ import annotations

import os
import unittest

from numpy.testing import assert_array_equal

from pymatgen.io.shengbte import Control
from pymatgen.util.testing import TEST_FILES_DIR, PymatgenTest

try:
    import f90nml
except ImportError:
    f90nml = None

test_dir = f"{TEST_FILES_DIR}/shengbte"

this_dir = os.path.dirname(os.path.abspath(__file__))


class TestShengBTE(PymatgenTest):
    def setUp(self):
        self.filename = f"{test_dir}/CONTROL-CSLD_Si"
        self.test_dict = {
            "nelements": 1,
            "natoms": 2,
            "ngrid": [25, 25, 25],
            "norientations": 0,
            "lfactor": 0.1,
            "lattvec": [
                [0.0, 2.734363999, 2.734363999],
                [2.734363999, 0.0, 2.734363999],
                [2.734363999, 2.734363999, 0.0],
            ],
            "elements": "Si",
            "types": [1, 1],
            "positions": [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]],
            "scell": [5, 5, 5],
            "t": 500,
            "scalebroad": 0.5,
            "isotopes": False,
            "onlyharmonic": False,
            "nonanalytic": False,
            "nanowires": False,
        }

    @unittest.skipIf(f90nml is None, "No f90nml")
    def test_from_file(self):
        io = Control.from_file(self.filename)
        assert io["nelements"] == 1
        assert io["natoms"] == 2
        assert_array_equal(io["ngrid"], [25, 25, 25])
        assert io["norientations"] == 0
        assert io["lfactor"] == 0.1
        assert io["lattvec"][0] == [0.0, 2.734363999, 2.734363999]
        assert io["lattvec"][1] == [2.734363999, 0.0, 2.734363999]
        assert io["lattvec"][2] == [2.734363999, 2.734363999, 0.0]
        assert isinstance(io["elements"], (list, str))
        if isinstance(io["elements"], list):
            all_strings = all(isinstance(item, str) for item in io["elements"])
            assert all_strings
        assert isinstance(io["types"], (list, int))
        if isinstance(io["types"], list):
            all_ints = all(isinstance(item, int) for item in io["types"])
            assert all_ints
        assert_array_equal(io["positions"], [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]])
        assert_array_equal(io["scell"], [5, 5, 5])
        assert io["t"] == 500
        assert io["scalebroad"] == 0.5
        assert not io["isotopes"]
        assert not io["onlyharmonic"]
        assert not io["nonanalytic"]
        assert not io["nanowires"]

        if os.path.exists(f"{test_dir}/test_control"):
            os.remove(f"{test_dir}/test_control")
        io.to_file(filename=f"{test_dir}/test_control")

        with open(f"{test_dir}/test_control") as file:
            test_string = file.read()
        with open(f"{test_dir}/CONTROL-CSLD_Si") as reference_file:
            reference_string = reference_file.read()
        assert test_string == reference_string
        os.remove(f"{test_dir}/test_control")

    @unittest.skipIf(f90nml is None, "No f90nml")
    def test_from_dict(self):
        io = Control.from_dict(self.test_dict)
        if os.path.exists(f"{test_dir}/test_control"):
            os.remove(f"{test_dir}/test_control")
        io.to_file(filename=f"{test_dir}/test_control")
        with open(f"{test_dir}/test_control") as file:
            test_string = file.read()
        with open(f"{test_dir}/CONTROL-CSLD_Si") as reference_file:
            reference_string = reference_file.read()
        assert test_string == reference_string
        os.remove(f"{test_dir}/test_control")

    @unittest.skipIf(f90nml is None, "No f90nml")
    def test_msonable_implementation(self):
        # tests as dict and from dict methods
        ctrl_from_file = Control.from_file(self.filename)
        control_from_dict = Control.from_dict(ctrl_from_file.as_dict())
        assert control_from_dict == ctrl_from_file
        assert control_from_dict.to_json() == ctrl_from_file.to_json()
