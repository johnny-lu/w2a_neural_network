import json
import os.path
import numpy as np
import graph_data_execute
from unittest import main, TestCase


class TestGraphData (TestCase):

    # ---------------
    # Reject Outliers
    # ---------------

    big_array = [30, 171, 184, 201, 212, 250, 265, 270, 272, 289,
                 305, 306, 322, 322, 336, 346, 351, 370, 390, 404,
                 409, 411, 436, 437, 439, 441, 444, 448, 451, 453,
                 470, 480, 482, 487, 494, 495, 499, 503, 514, 521,
                 522, 527, 548, 550, 559, 560, 570, 572, 574, 578,
                 585, 592, 592, 607, 616, 618, 621, 629, 637, 638,
                 640, 656, 668, 707, 709, 719, 737, 739, 752, 758,
                 766, 792, 792, 794, 802, 818, 830, 832, 843, 858,
                 860, 869, 918, 925, 953, 991, 1000, 1005, 1068, 1441]

    def test_ro1(self):
        my_list = np.array([1, 3, 4, 6, 7, 7, 8, 8, 10, 12, 17])
        new_list = graph_data_execute.reject_outliers(my_list, 3.5)
        new_list = new_list.tolist()
        assert new_list == [1, 3, 4, 6, 7, 7, 8, 8, 10, 12, 17]

    def test_ro2(self):
        my_list = np.array([1, 3, 4, 6, 7, 7, 8, 8, 10, 12, 17])
        new_list = graph_data_execute.reject_outliers(my_list, 2)
        new_list = new_list.tolist()
        assert new_list == [3, 4, 6, 7, 7, 8, 8, 10, 12]

    def test_ro3(self): # testing tolerance = 5. Only 1441 should be removed
        my_list = np.array(TestGraphData.big_array)
        new_list = graph_data_execute.reject_outliers(my_list, 5.)
        new_list = new_list.tolist()
        assert new_list == [30, 171, 184, 201, 212, 250, 265, 270, 272, 289,
                            305, 306, 322, 322, 336, 346, 351, 370, 390, 404,
                            409, 411, 436, 437, 439, 441, 444, 448, 451, 453,
                            470, 480, 482, 487, 494, 495, 499, 503, 514, 521,
                            522, 527, 548, 550, 559, 560, 570, 572, 574, 578,
                            585, 592, 592, 607, 616, 618, 621, 629, 637, 638,
                            640, 656, 668, 707, 709, 719, 737, 739, 752, 758,
                            766, 792, 792, 794, 802, 818, 830, 832, 843, 858,
                            860, 869, 918, 925, 953, 991, 1000, 1005, 1068]

    def test_ro4(self): # testing tolerance = 3.5; Only 1441 should be removed
        my_list = np.array(TestGraphData.big_array)
        new_list = graph_data_execute.reject_outliers(my_list, 3.5)
        new_list = new_list.tolist()
        assert new_list == [30, 171, 184, 201, 212, 250, 265, 270, 272, 289,
                            305, 306, 322, 322, 336, 346, 351, 370, 390, 404,
                            409, 411, 436, 437, 439, 441, 444, 448, 451, 453,
                            470, 480, 482, 487, 494, 495, 499, 503, 514, 521,
                            522, 527, 548, 550, 559, 560, 570, 572, 574, 578,
                            585, 592, 592, 607, 616, 618, 621, 629, 637, 638,
                            640, 656, 668, 707, 709, 719, 737, 739, 752, 758,
                            766, 792, 792, 794, 802, 818, 830, 832, 843, 858,
                            860, 869, 918, 925, 953, 991, 1000, 1005, 1068]

    # -------------
    # Get Filenames
    # -------------

    def test_gfn1(self):  # Capture filenames that start with a dot
        filename = ".logs"
        name = graph_data_execute.getFilename(filename)
        assert name == ".logs"

    def test_gfn2(self):  # Get everything but the last dot
        filename = "foo.bar.jpeg"
        name = graph_data_execute.getFilename(filename)
        assert name == "foo.bar"

    def test_gfn3(self):  # Handles files with no dots in name
        filename = "_hello-world"
        name = graph_data_execute.getFilename(filename)
        assert name == "_hello-world"

    # -----------
    # Test main()
    # -----------

    def test_mn1(self):
        assert (not os.path.isfile("gde_test.json"))
        with open("gde_test.json", "w") as outfile:  # make a test file
            json.dump(TestGraphData.big_array, outfile)

        graph_data_execute.main(["gde_test.json"])  # main takes in an array
        assert os.path.isfile("gde_test.pdf")  # check if graph is made
        assert os.path.isfile("gde_test_log.txt")  # check if log is made
        assert os.path.getsize("gde_test_log.txt") > 0  # check if not empty

        # test clean-up
        os.remove("gde_test.json")
        os.remove("gde_test.pdf")
        os.remove("gde_test_log.txt")

    def test_mn2(self):
        assert (not os.path.isfile("gde_test.json"))
        with open("gde_test.json", "w") as outfile:  # make a test file
            json.dump([1, 3, 4, 6, 7, 7, 8, 8, 10, 12, 17], outfile)

        graph_data_execute.main(["gde_test.json"])  # main takes in an array
        assert os.path.isfile("gde_test.pdf")  # check if graph is made
        assert os.path.isfile("gde_test_log.txt")  # check if log is made
        assert os.path.getsize("gde_test_log.txt") > 0  # check if not empty

        # test clean-up
        os.remove("gde_test.json")
        os.remove("gde_test.pdf")
        os.remove("gde_test_log.txt")


if __name__ == "__main__":
    main()
