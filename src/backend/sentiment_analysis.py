from google.cloud import language_v2
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_CLOUD_API = os.environ.get("GOOGLE_CLOUD_API_KEY")

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
    
    # # Get overall sentiment of the input document
    # print(f"Document sentiment score: {response.document_sentiment.score}")
    # print(f"Document sentiment magnitude: {response.document_sentiment.magnitude}")
    # # Get sentiment for all sentences in the document
    # for sentence in response.sentences:
    #     print(f"Sentence text: {sentence.text.content}")
    #     print(f"Sentence sentiment score: {sentence.sentiment.score}")
    #     print(f"Sentence sentiment magnitude: {sentence.sentiment.magnitude}")

    # # Get the language of the text, which will be the same as
    # # the language specified in the request or, if not specified,
    # # the automatically-detected language.
    # print(f"Language of the text: {response.language_code}")
    
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