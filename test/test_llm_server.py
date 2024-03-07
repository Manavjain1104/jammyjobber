import unittest
from context import utils
from utils.llm_utils import *



class LLMServerTestCase(unittest.TestCase):
    def test_summariser(self):
        try:
            create_summary("This is a sample text for creating a summary")
        except Exception:
            self.fail("create_summary raised an exception!")

    def test_embedder(self):
        try:
            vector = create_embedding("This is a sample text for creating an embedding")
            assert(len(vector) == 384)
        except Exception:
            self.fail("create_embedding raised an exception!")

    def test_QA(self):
        try:
            get_job_details("This is a samplejob for getting job details and required skills")
            get_skills_required("This is a samplejob for getting job details and required skills")
            get_candidate_skills("This is a sample candidate query")
            get_suggested_job("This is a sample candidate query")
        except Exception:
            self.fail("Q&A model raised an exception!")


if __name__ == '__main__':
    unittest.main()