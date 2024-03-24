# other_file.py
from perspective import Attributes
from perspect import analyze_text

# Use the function to analyze text
# There are a lot of attributes
response = analyze_text("Your example text here", [Attributes.TOXICITY, Attributes.INSULT, Attributes.INFLAMMATORY])
print(response)