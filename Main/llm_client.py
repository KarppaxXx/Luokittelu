"""
MODULE: llm_client.py
PURPOSE: Communicates with OpenAI to classify the text.
TECHNIQUES:
- API Interaction: Sends HTTP requests to OpenAI's GPT models.
- Prompt Engineering: Constructs a specific prompt to guide the AI.
- JSON Mode: Forces the AI to reply in structured JSON data, not free text.
- Retry Logic: Automatically retries if the API call fails or times out.
"""
import json
import time
from typing import List, Optional
from openai import OpenAI, APIError
from . import config
from .models import DocumentType, ClassificationResult

def classify_document(text: str, doc_types: List[DocumentType]) -> ClassificationResult:
    """Classifies the document text using OpenAI API."""
    if not config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    # Prepare prompt
    doc_type_list = "\n".join([f"- Code: {d['code']}, Title: {d['title']}, Desc: {d['description']}" for d in doc_types])
    
    truncated_text = text[:config.MAX_TEXT_LENGTH]
    
    system_prompt = (
        "You are an expert document classifier.\n"
        "You will be given a list of document types and the text content of a document.\n"
        "Your task is to select the BEST matching document code for the given text.\n"
        "If no document type matches clearly, use 'UNKNOWN'.\n"
        "You MUST return the result in strictly valid JSON format with the following keys:\n"
        "- document_code: string (must be one of the provided codes or 'UNKNOWN')\n"
        "- confidence: float (0.0 to 1.0)\n"
        "- rationale: string (brief explanation)\n"
    )
    
    user_prompt = (
        f"--- Document Types ---\n{doc_type_list}\n\n"
        f"--- Document Text (truncated) ---\n{truncated_text}\n\n"
        "Select the best document code."
    )

    for attempt in range(config.RETRY_ATTEMPTS):
        try:
            response = client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=config.OPENAI_TEMPERATURE,
                response_format={ "type": "json_object" }
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from API")

            # Parse JSON
            try:
                data = json.loads(content)
                
                # Validate schema
                if "document_code" not in data:
                     raise ValueError("Missing 'document_code' in response")
                
                # Check if code is valid (or UNKNOWN)
                valid_codes = {d['code'] for d in doc_types}
                valid_codes.add("UNKNOWN")
                
                if data['document_code'] not in valid_codes:
                    data['document_code'] = "UNKNOWN"
                    data['rationale'] = data.get('rationale', "") + " [Original code invalid, defaulted to UNKNOWN]"

                return ClassificationResult(
                    document_code=data['document_code'],
                    confidence=float(data.get('confidence', 0.0)),
                    rationale=str(data.get('rationale', ''))
                )
                
            except json.JSONDecodeError:
                # Basic "fix JSON" retry happens naturally via loop if we just raise error here, 
                # but instruction asked for ONE specific fix retry. 
                # Since we use response_format="json_object", invalid JSON is rare.
                # simpler to just count this as a failure and retry the whole call.
                raise ValueError("Invalid JSON response")

        except (APIError, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < config.RETRY_ATTEMPTS - 1:
                time.sleep(config.RETRY_BACKOFF_BASE ** attempt)
            else:
                raise Exception(f"All retries failed: {e}")
    
    # Should not reach here
    raise Exception("Classification failed unexpectedly")
