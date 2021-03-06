from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, ConceptsOptions


class PersonalityInterface:
    def get_personality(self, text):
        """ Get personality of the text as a dictionary"""
        pass


class NLUPersonalityInterface:
    api_key = '12YdTwvTRClHxgrpQM_gWs_e0Bli6YNgvCQfF_OlBpKb'
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e9d863c5-d9a1-4199-a371-0ef40dfcb96e'
    version = '2020-08-01'

    def __init__(self):
        authenticator = IAMAuthenticator(self.api_key)
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=self.version,
            authenticator=authenticator)

        self.natural_language_understanding.set_service_url(self.url)

    def get_personality(self, text):
        number_concepts = 5
        concept_dict = {}

        emotion_response = self.natural_language_understanding.analyze(
            text=text,
            features=Features(
                emotion=EmotionOptions(document=True))).get_result()

        concept_response = self.natural_language_understanding.analyze(
            text=text,
            features=Features(
                concepts=ConceptsOptions(limit=number_concepts))).get_result()

        personality_dict = emotion_response["emotion"]["document"]["emotion"]
        for concept in concept_response["concepts"]:
            concept_dict[concept["text"].replace(" ", "_")] = concept["relevance"]

        return [personality_dict, concept_dict]


if __name__ == "__main__":
    nlu = NLUPersonalityInterface()
    # test_str = 'But the black kitten had been finished with earlier in the afternoon, and so, while Alice was sitting curled up in a corner of the great arm-chair, half talking to herself and half asleep, the kitten had been having a grand game of romps with the ball of worsted Alice had been trying to wind up, and had been rolling it up and down till it had all come undone again; and there it was, spread over the hearth-rug, all knots and tangles, with the kitten running after its own tail in the middle.'
    test_str = 'I like to read about Mysteries and Courtship'
    print(nlu.get_personality(test_str))
