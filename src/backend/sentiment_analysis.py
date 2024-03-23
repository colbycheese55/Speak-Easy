from google.cloud import language_v2
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EmotionOptions
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_CLOUD_API = os.environ.get("GOOGLE_CLOUD_API_KEY")
IBM_API_KEY = os.environ.get("IBM_API_KEY")
IBM_URL = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/56903cc9-7715-42b6-8b54-708da4e773ca"

def ibm_analysis(text_content = ""):
    authenticator = IAMAuthenticator(IBM_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(IBM_URL)
    response = natural_language_understanding.analyze(text=text_content, features=Features(emotion=EmotionOptions())).get_result()
    
    return response["emotion"]["document"]["emotion"]  # returns a dictionary with keys "sadness", "joy", "fear", "disgust", "anger"

def return_client_sent(api_key, project_id):
    return language_v2.LanguageServiceClient(
        client_options={"api_key": api_key, "quota_project_id": project_id}
    )

def sentiment_analysis(text_content = ""):
    client = return_client_sent(GOOGLE_CLOUD_API, "HooHacks2024")

    # Available types: PLAIN_TEXT, HTML
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language_code = "en"
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    # See https://cloud.google.com/natural-language/docs/reference/rest/v2/EncodingType.
    encoding_type = language_v2.EncodingType.UTF8

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    
    return response.document_sentiment.score, response.document_sentiment.magnitude
    
# Returns more information along with the sentiment
def annotate_text(text_content = ""):
    client = return_client_sent(GOOGLE_CLOUD_API, "HooHacks2024")
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
    language_code = "en"
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    encoding_type = language_v2.EncodingType.UTF8
    
    features = {
        "extract_entities": True,
        "extract_document_sentiment": True,
        "classify_text": True,
        "moderate_text": True
    }
    
    response = client.annotate_text(request={"document": document, "features": features, "encoding_type": encoding_type})
    
    return response.document_sentiment, response.categories, response.moderation_categories