"""client test module"""
from getpass import getpass
import unittest
import aiman

class ClientServiceTest(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """
    pwd = "thorsten.atzeni@brandcompete.com42" #getpass()
    url_host = "https://aiman-api-dev.brandcompete.com"
    user_name = "thorsten.atzeni@brandcompete.com"
    client = aiman.AIManServiceClient(host_url=url_host, user_name=user_name, password=pwd)

    def test_login(self):
        """_summary_"""
        self.assertRaises(ValueError,aiman.AIManServiceClient, host_url="", user_name="", password="")
        self.assertIsNotNone(self.client.credential)
        self.assertGreater(len(self.client.credential.access.token), 0)

    def test_get_models(self):
        """_summary_"""
        models = self.client.get_models()
        self.assertIsNotNone(models)
        self.assertGreater(len(models),0)

    def test_simple_prompt(self):
        """_summary_""" 
        return
        models = self.client.get_models()
        response = self.client.prompt(
            model_tag_id=models[0].default_model_tag_id,
            query="Who is the current president of the usa")
        self.assertIsNotNone(response["responseText"])
        self.assertGreaterEqual(len(response["responseText"]),0)
