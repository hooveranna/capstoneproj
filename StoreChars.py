import json
import urllib
from TextPersonality import NLUPersonalityInterface
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class CharDatabaseInterface:
    """ store the info of character """
    def add_char(self, char_name: str, char_info: dict):
        """ Adds character info to database"""
        pass

    def search_char(self, char_info: dict) -> str:
        """ Searches for character closest to passed in info """
        pass


class DiscoveryCharDatabase(CharDatabaseInterface):
    api_key = 'hCH8RRcfJEQUE6Ve8gCl_gsXKqM7Mkdusc6Mdnchb51s'
    url = 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/ed199079-a3d5-47be-ae2c-bac80e6582ae'
    version = '2019-04-30'

    def __init__(self, collection_name):
        authenticator = IAMAuthenticator(self.api_key)
        self.discovery = DiscoveryV1(
            version=self.version,
            authenticator=authenticator
        )

        self.discovery.set_service_url(self.url)

        environments = self.discovery.list_environments().get_result()
        environments = [x for x in environments['environments'] if x['name'] != 'Watson System Environment']
        self.environment_id = environments[0]['environment_id']
        collections = self.discovery.list_collections(environment_id=self.environment_id).get_result()
        collections = [x for x in collections['collections'] if x['name'] == collection_name]
        self.collection_id = collections[0]["collection_id"]

    def create_new_collection(self, collection_name):
        collection_response = self.discovery.create_collection(
            environment_id=self.environment_id,
            name=collection_name).get_result()

        self.collection_id = collection_response["collection_id"]

        return 0

    def add_char(self, char_name: str, char_info: dict):
        file_name = 'test.json'
        with open(file_name, 'w') as fp:
            json.dump(char_info, fp)
        with open(file_name) as file_info:
            response = self.discovery.add_document(
                environment_id=self.environment_id,
                collection_id=self.collection_id,
                file=file_info,
                filename=char_name,
                file_content_type='application/json'
            )
        return response

    def search_char(self, char_personality: dict) -> str:
        # convert dict to a general query string
        # query_string = urllib.parse.urlencode(char_personality)
        query_string = self.convert_to_discovery_query_str(char_personality)
        print(query_string)
        query_results = self.discovery.query(
            environment_id=self.environment_id,
            collection_id=self.collection_id,
            query=query_string
        ).get_result()
        print(query_results)
        doc_id = query_results["results"][0]["id"]

        response = self.discovery.get_document_status(
            environment_id=self.environment_id,
            collection_id=self.collection_id,
            document_id=doc_id
        ).get_result()

        return response['filename']

    def convert_to_discovery_query_str(self, query_dict: dict):
        query_str = ''
        for key in query_dict:
            if query_str:
                query_str += ', '
            value = query_dict[key]
            query_str += f'{key}::!{value}'
        return query_str


if __name__ == "__main__":
    sample_text = "'Hello!' I said. 'It's nice to meet you!' I ran to the other side of the river. How are you doing today????"
    sample_text_2 = "There is no wind in the football..I talk, he talk, why you middle talk?.You rotate the ground 4 times..You go and understand the tree.I'll give you clap on your cheeks..Bring your parents and your mother and especially your father."
    nlu = NLUPersonalityInterface()
    this_dict = nlu.get_personality(sample_text_2)
    print(this_dict)
    ddb = DiscoveryCharDatabase("Collection 1")
    char_name = ddb.search_char(this_dict)
    print(char_name)
    # this_dict = {
    #     "brasdfasdfand": "skd",
    #     "model": "kjhlkjh",
    #     "year": 1977
    # }
    # # ddb.convert_to_discovery_query_str(this_dict)
    # char_name = ddb.search_char(this_dict)
    # print(char_name)
