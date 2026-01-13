import json
import boto3
from app.core.config import Config

class BedrockLLM:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )

    def generate_response(self, query, context) -> str:
        prompt = f"""You are a AI assistant helping a user understand EULA (End User License Agreement) and ToS (Terms of Service) Documents.
        Based on the following excerpts from legal documents, provide a clear, accurate, and helpful answer to the user's question: 
        
        Document Excerpts:
        {context}
        
        User Question:
        {query}

        Please provide a comprehensive answer that:
        1. Directly addresses the user's question
        2. Referencees specific sections from the document when relevant
        3. Explains any legal terms in plain language
        4. Highlights important implications or requirements
        5. Notes if certain information is not available in the provided excerpts by simply stating "I don't know"
        
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
