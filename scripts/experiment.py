import boto3
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

bedrock = boto3.client(service_name="bedrock-runtime")

"""
{
  "modelId": "amazon.titan-embed-text-v1",
  "contentType": "application/json",
  "accept": "*/*",
  "body": {
    "inputText": "this is where you place your input text"
   } 
}
"""

DATA = """Greene sets sights on world title

Maurice Greene aims to wipe out the pain of losing his Olympic 100m title in Athens by winning a fourth World Championship crown this summer.

He had to settle for bronze in Greece behind fellow American Justin Gatlin and Francis Obikwelu of Portugal. "It really hurts to look at that medal. It was my mistake. I lost because of the things I did," said Greene, who races in Birmingham on Friday. "It's never going to happen again. My goal - I'm going to win the worlds." Greene crossed the line just 0.02 seconds behind Gatlin, who won in 9.87 seconds in one of the closest and fastest sprints of all time. But Greene believes he lost the race and his title in the semi-finals. "In my semi-final race, I should have won the race but I was conserving energy. "That's when Francis Obikwelu came up and I took third because I didn't know he was there. "I believe that's what put me in lane seven in the final and, while I was in lane seven, I couldn't feel anything in the race.

"I just felt like I was running all alone. "I believe if I was in the middle of the race I would have been able to react to people that came ahead of me." Greene was also denied Olympic gold in the 4x100m men's relay when he could not catch Britain's Mark Lewis-Francis on the final leg. The Kansas star is set to go head-to-head with Lewis-Francis again at Friday's Norwich Union Grand Prix. The pair contest the 60m, the distance over which Greene currently holds the world record of 6.39 seconds. He then has another indoor meeting in France before resuming training for the outdoor season and the task of recapturing his world title in Helsinki in August. Greene believes Gatlin will again prove the biggest threat to his ambitions in Finland. But he also admits he faces more than one rival for the world crown. "There's always someone else coming. I think when I was coming up I would say there was me and Ato (Boldon) in the young crowd," Greene said. "Now you've got about five or six young guys coming up at the same time."
"""

QUERY_1 = "Maurice Greene losing an Olympic Gold medal, but receives Bronze in Greece"

QUERY_2 = "New York pizza is really good. But I am on a diet and I should not have it!"

if __name__ == "__main__":
    data_body = json.dumps({"inputText": DATA})

    data_query_1 = json.dumps({"inputText": QUERY_1})

    data_query_2 = json.dumps({"inputText": QUERY_2})

    modelId = "amazon.titan-embed-text-v1"
    accept = "*/*"
    contentType = "application/json"

    response = bedrock.invoke_model(
        body=data_body, modelId=modelId, accept=accept, contentType=contentType
    )

    data_embedding = np.array([json.loads(response.get("body").read())["embedding"]])

    response_1 = bedrock.invoke_model(
        body=data_query_1, modelId=modelId, accept=accept, contentType=contentType
    )

    query_embedding_1 = np.array(
        [json.loads(response_1.get("body").read())["embedding"]]
    )

    response_2 = bedrock.invoke_model(
        body=data_query_2, modelId=modelId, accept=accept, contentType=contentType
    )

    query_embedding_2 = np.array(
        [json.loads(response_2.get("body").read())["embedding"]]
    )

    similarity_1 = cosine_similarity(data_embedding, query_embedding_1)
    similarity_2 = cosine_similarity(data_embedding, query_embedding_2)

    print(f"Query 1 Cosine Similarity is: {similarity_1}")

    print(f"Query 2 Cosine Similarity is: {similarity_2}")
