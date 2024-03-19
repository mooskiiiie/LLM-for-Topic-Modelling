# Import packages
import os
import pandas as pd
import google.generativeai as palm

# Insert API Key from Google AI Studio
palm.configure(api_key = 'INSERT API KEY')
os.environ('API KEY')

# Read data (Make use of your own text data)
df = pd.read_csv('Responses 2023.csv')

# This function gets the sentiment based on the rating. Rating is used as it better represents the sentiment compared to polarity
def get_sentiment_from_rating(rating):
  if rating in ["Somewhat Dissatisfied", "Very Dissatisfied"]:
    return 'Negative'
  elif rating in ["Very Satisfied", "Somewhat Satisfied"]:
    return 'Positive'
  else:
    return 'Neutral'

# This function handles the prompt and the output that the LLM will give
# Feel free to change the prompt and engineer it to a better one
def summarize(reviews, model):
  prompt = """ 
              All the reviews below are all negative. I can't read through each one by one, so I need your help to help me understand what the reviews
              are saying. Can you help me by doing topic modelling on it? Include as well their corresponding keywords taken from the reviews itself? Make sure the topic labels itself are descriptive.
              An example of a topic label would be Unsuccessful delivery. Lastly, please summarize the reviews as well. Here is the data. \n
            """
  for review in reviews:
    prompt += '\n' + review
        
  completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=1000,
        )

# Pre-processing (Adjust the pre-processing steps accd to your own data)
# Create Reviews column and make it string format
df['Reviews'] = df['Can you tell us your experience? How can we improve to serve you better?'].astype(str)

# Apply our sentiment formula to CSAT Rating to get Sentiment label
df['Sentiment'] = df['CSAT Rating'].apply(get_sentiment_from_rating)

# Filter the data to only the Negative sentiments
df = df[df['Sentiment'] == 'Negative']

# Only select the necessary columns
df = df[['Transaction Name', 'Sentiment', 'Reviews']]
specified_transaction_names = ["Card Delivery Request", "Card Delivery Inquiry", "Tagging Of Lost/Stolen Card Request", "Card Replacement Request", "Card Pick Up Request", "Card Pick Up Inquiry"]
df = df[df['Transaction Name'].isin(specified_transaction_names)]

# Only take a subset of the data as the free version of the API has a limit. A suggestion is to iterate different subsets to produce different topics and compare
df = df['Reviews'][0:9]

# Select the model that you will be using. This is a given code in the Palm API in order to select a model
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

# Transform the dataframe into a list to pass it into the prompt. Then apply the summarize function to get the results
reviews = df1.tolist()
result = summarize(reviews, model)

print(result)
