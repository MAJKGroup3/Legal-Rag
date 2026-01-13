import json
import boto3
from app.core.config import Config

class BedrockLLM:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY
        )

    def generate_response(self, query, context) -> str:
        prompt = f"""You are a AI assistant helping a user understand EULA (End User License Agreement).
        Based on the following excerpts from legal documents, provide a clear, accurate, and helpful answer to the user's question: 
        
        Document Excerpts:
        {context}
        
        User Question:
        {query}

        Please provide a comprehensive answer that:
        1. Directly addresses the user's question
        2. Provides answers only from the context
        3. If you don't know something, please say say "I don't know".
        
        Answer:
        """

        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": 0.7,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            response = self.client.invoke_model(
                modelId=Config.BEDROCK_MODEL_ID,
                body=json.dumps(request_body),
            )
            response_body = json.loads(response["body"].read())
            return response_body["content"][0]["text"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
