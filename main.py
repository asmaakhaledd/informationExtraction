# dep
from typing import List, Optional
import pandas as pd
import openai
import os 
import json
import csv
import kor.encoders.csv_data

from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import document 
from langchain.text_splitter import RecursiveCharacterTextSplitter

from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number 
from kor import extract_from_documents, from_pydantic, create_extraction_chain

from pydantic import BaseModel, validator, Field


os.environ["OPENAI_API_KEY"] = "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"

# openai.api_key = "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"

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
)

schema = Object(
    id="personal_info",
    description="Personal information about a given person.",
    attributes=[
        Text(
            id="first_name",
            description="The first name of the person",
            examples=[("John Smith went to the store", "John")],
        ),
        Text(
            id="last_name",
            description="The last name of the person",
            examples=[("John Smith went to the store", "Smith")],
        ),
        Number(
            id="age",
            description="The age of the person in years.",
            examples=[("23 years old", "23"), ("I turned three on sunday", "3")],
        ),
    ],
    examples=[
        (
            "John Smith was 23 years old. He was very tall. He knew Jane Doe. She was 5 years old.",
            [
                {"first_name": "John", "last_name": "Smith", "age": 23},
                {"first_name": "Jane", "last_name": "Doe", "age": 5},
            ],
        )
    ],
    many=True,
)


chain = create_extraction_chain(llm, schema)
# print(chain.prompt.format_prompt(text="[user input]").to_string())
extracted_data=chain.predict_and_parse(text="David Jones was 34 years old a long time ago.")["data"]
print(extracted_data)