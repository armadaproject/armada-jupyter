# """
# Testing the submit function in __main__.py
# """

# import os
# from armada_jupyter.__main__ import submit_worker

# from armada_jupyter.submissions import Submission, Job


# TEST_FILE = "tests/files/general.yml"

# # set variables in environment
# os.environ["ARMADA_HOST"] = "localhost"
# os.environ["ARMADA_PORT"] = "50051"
# os.environ["DISABLE_SSL"] = "True"


# class FakeArmadaClient:
#     pass


# def test_submit():
#     """
#     Test the submit function
#     """

#     submit_worker(TEST_FILE, FakeArmadaClient)
