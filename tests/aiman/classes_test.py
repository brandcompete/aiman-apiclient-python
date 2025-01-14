"""client test module"""
import unittest
from aiman.core.classes import AIModel, Prompt, PromptOptions

class ClassesTest(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """
    def test_model_class(self):
        """_summary_"""
        result = AIModel.from_dict({})
        self.assertEqual(result.name, "")

        result = AIModel.from_dict({"name":"TEST"})
        self.assertEqual(result.name, "TEST")

        to_dict = AIModel.to_dict()
        self.assertEqual(to_dict["name"], "TEST")

    def test_prompt_class(self):
        """_summary_"""
        result = Prompt.from_dict({})
        self.assertEqual(result.prompt, "")
        to_compare = "this is my prompt"
        result = Prompt.from_dict({"prompt": to_compare})
        self.assertEqual(result.prompt, to_compare)
        to_dict = Prompt.to_dict()
        self.assertEqual(to_dict["prompt"], to_compare)

    def test_prompt_options_class(self):
        """_summary_"""
        prompt_options = PromptOptions()
        self.assertEqual(prompt_options.mirostat, 0)
        self.assertEqual(prompt_options.mirostat_eta, 0.1)
        self.assertEqual(prompt_options.mirostat_tau, 5)
        self.assertEqual(prompt_options.raw, False)
        self.assertEqual(prompt_options.keep_context, True)

        po_dict  = prompt_options.to_dict()
        self.assertEqual(po_dict["mirostat"], 0)
        self.assertEqual(po_dict["mirostat_eta"], 0.1)
        self.assertEqual(po_dict["mirostat_tau"], 5)
        self.assertEqual(po_dict["raw"], False)
        self.assertEqual(po_dict["keep_context"], True)
