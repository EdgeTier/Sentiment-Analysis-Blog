from zenpy import Zenpy
import pandas as pd
from textblob import TextBlob
import os

# add Zendesk credential to a dict
credentials = {
    "email": "test@edgetier.com",
    "subdomain": "edgetier",
    "token":os.environ.get("ZENDESK_TOKEN")
}

# create a Zenpy client
zenpy_client = Zenpy(**credentials)

# read in all tickets from view_id 100
view_id = 100
tickets = zenpy_client.views.tickets(int(view_id))

# create a list to save data to
ticket_data = []
# iterate through each ticket
for ticket in tickets: 
    # then iterate through the comments in each ticket
    for comment in zenpy_client.tickets.comments(ticket=ticket.id):
        ticket_dict = {
            "ticket_id": ticket.id,
            "comment":comment.body
        }
        ticket_data.append(ticket_dict)
        
# convert to a Pandas DataFrame
ticket_comments_df = pd.DataFrame(ticket_data)

# iterate through our dataframe and get a polarity score for each comment
for index, row in ticket_comments_df.iterrows():
    text = TextBlob(row['comment'])
    ticket_comments_df.at[index, 'polarity'] = text.sentiment.polarity
    
ticket_comments_df.head()
