import json
from TextPersonality import NLUPersonalityInterface
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class CharDatabaseInterface:
    """ store the info of character """
    def add_char(self, char_name: str, char_info: dict):
        """ Adds character info to database"""
        pass

    def search_char(self, char_info: dict) -> (str, dict):
        """ Searches for character closest to passed in info and returns character name and personality fields """
        pass

    def find_char(self, name: str):
        """ Searches for character closest to passed in info and returns character name and personality fields """
        pass


class DiscoveryCharDatabase(CharDatabaseInterface):
    api_key = 'hCH8RRcfJEQUE6Ve8gCl_gsXKqM7Mkdusc6Mdnchb51s'
    url = 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/ed199079-a3d5-47be-ae2c-bac80e6582ae'
    version = '2019-04-30'
    conf_interval = 0.01

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

    def delete_collection(self):
        delete_collection = self.discovery.delete_collection(
            environment_id=self.environment_id,
            collection_id=self.collection_id).get_result()

        self.collection_id = None

        return 0

    def reset_db(self, collection_name):
        self.delete_collection()
        self.create_new_collection(collection_name)

        collection = self.discovery.get_collection(
            environment_id=self.environment_id,
            collection_id=self.collection_id).get_result()

        return collection["document_counts"]

    def add_char(self, char_name: str, char_info: dict):
        file_name = 'add_char.json'
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
        query_string = self.convert_to_discovery_query_str(char_personality)
        # print(query_string)
        query_results = self.discovery.query(
            environment_id=self.environment_id,
            collection_id=self.collection_id,
            query=query_string,
            offset=1
        ).get_result()
        # print(query_results)
        if not query_results["results"]:
            return "You are completely unique! There is no one else like you!", dict()
        book_result = query_results["results"][0]
        char_name = book_result.pop("extracted_metadata", None)["filename"]
        book_result.pop("id", None)
        book_result.pop("result_metadata", None)
        # print(book_result)
        return char_name, book_result

    def find_char(self, name: str, movie:str):
        char_name = "char_name: " + name + ", title: " + movie
        query_results = self.discovery.query(
            environment_id=self.environment_id,
            collection_id=self.collection_id,
            count=1,
            filter=char_name
        ).get_result()
        #print(query_results)
        if not query_results["results"]:
            return "Not in database"
        book_result = query_results["results"][0]
        char_name = book_result.pop("extracted_metadata", None)["filename"]
        book_result.pop("id", None)
        book_result.pop("result_metadata", None)
        book_result.pop("title", None)
        book_result.pop("char_name", None)
        book_result.pop("sentences", None)
        # print(book_result)
        return book_result

    def convert_to_discovery_query_str(self, query_dict: dict):
        query_str = ''
        emotions_dict, personality_dict = get_emotions_from_dict(query_dict)

        for emotion in emotions_dict:
            if query_str:
                query_str += ' | '
            value = emotions_dict[emotion]
            query_str += f'({emotion}<={value + self.conf_interval}, {emotion}>={max(value - self.conf_interval, 0.0001)})'

        for concept in personality_dict:
            if query_str:
                query_str += ' | '
            value = personality_dict[concept]
            query_str += f'({concept}:*^5)'
        return query_str


def get_emotions_from_dict(personality_dict):
    emotions_dict = dict()
    emotions_dict["sadness"] = personality_dict.pop("sadness", 0)
    emotions_dict["joy"] = personality_dict.pop("joy", 0)
    emotions_dict["fear"] = personality_dict.pop("fear", 0)
    emotions_dict["disgust"] = personality_dict.pop("disgust", 0)
    emotions_dict["anger"] = personality_dict.pop("anger", 0)
    return emotions_dict, personality_dict


if __name__ == "__main__":
    sample_text = "This is awful! I can't believe you did this to me? I was looking forward to this. How could you? You're disgusting!" # ==> outputs George Wickham
    sample_text_2 = "Oh, I'm quite downhearted that my brother is not here right now... However, I would love that! If you are talking about that! Then I must be part of the conversation! I sure that I would enjoy that very much! This would be delightful! " # ==> charlotte lucas
    sample_text_3 = "this is a test sentence"
    nlu = NLUPersonalityInterface()
    this_dict = nlu.get_personality(sample_text_3)
    full_dict = dict(this_dict[0])
    full_dict.update(this_dict[1])
    print(full_dict)
    ddb = DiscoveryCharDatabase("Collection 1")
    # document_counts = ddb.reset_db("Collection 1")
    # print(document_counts)
    char_match, personality = ddb.search_char(full_dict)
    print(char_match)
    print(personality)
    # this_dict = {
    #     "brasdfasdfand": "skd",
    #     "model": "kjhlkjh",
    #     "year": 1977
    # }
    # # ddb.convert_to_discovery_query_str(this_dict)
    # char_name = ddb.search_char(this_dict)
    # print(char_name)
