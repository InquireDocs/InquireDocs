#  Copyright 2024-present Julian Nonino
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging


logger = logging.getLogger(__name__)


SUMMARY_TYPES = {
    "concise": {
        "display_name": "Concise summary",
        "description": "Writes a concise summary of the text",
        "prompt": """Write a concise summary of the following:
{context}
Do not include any other text, return only the summary.
Generate the summary in the same language as the text provided.
CONCISE SUMMARY:
""",
    },
    "detailed": {
        "display_name": "Detailed summary",
        "description": "Provides a detailed summary of the text",
        "prompt": """Provide a detailed summary of the following text:
{context}
Do not include any other text, return only the summary.
Generate the summary in the same language as the text provided.
DETAILED SUMMARY:
""",
    },
    "quiz": {
        "display_name": "Generate questions",
        "description": "Generates questions based on the text",
        "prompt": """Generate a list of questions based on the following text:
{context}
Do not include any other text, return only the list of questions.
Do not include anything like here is the list of questions or similar.
Generate the questions in the same language as the text provided.
QUESTIONS:
""",
    },
}


def get_summary_types():
    """Return the supported summary types"""
    return [
        {
            "name": key,
            "display_name": value["display_name"],
            "description": value["description"],
        }
        for key, value in SUMMARY_TYPES.items()
    ]


def get_summary_type_details(summary_type):
    """Return details about the summary type requested"""
    return SUMMARY_TYPES[summary_type]
