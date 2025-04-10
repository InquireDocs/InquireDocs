# import os
import logging
# import tempfile
from typing import Optional, Dict, Any

# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.core.summarizer.base import BaseSummarizer


logger = logging.getLogger(__name__)


class OpenAISummarizer(BaseSummarizer):
    """OpenAI summarizer implementation"""

    def __init__(self):
        """Initialize OpenAI client with API key from settings"""
        self.api_key = settings.openai_api_key
        self.default_model = settings.openai_default_model

    @property
    def provider_name(self) -> str:
        return "openai"

    async def summarize_text(
        self,
        text: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = settings.openai_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: int = settings.default_max_tokens,
    ) -> Dict[str, Any]:
        """Summarize text using OpenAI"""
        try:
            # Prepare LLM
            llm = ChatOpenAI(
                api_key=self.api_key,
                temperature=temperature,
                model_name=model,
                max_tokens=max_length
            )

            generated_summary = await self.generate_text_summary(summary_type, llm, text)

            return {
                "model": model,
                "provider": self.provider_name,
                "response_max_tokens": max_length,
                "summary": generated_summary,
                "summary_type": summary_type,
                "source": "text",
                "temperature": temperature
            }
        except (ValueError, Exception) as e:
            msg = "Error summarizing text"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e

    async def summarize_pdf(
        self,
        file_content: bytes,
        file_name: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = settings.openai_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: int = settings.default_max_tokens,
    ) -> Dict[str, Any]:
        """Summarize PDF using OpenAI"""
        pass
        # # Use default model if none provided
        # model_name = model or self.default_model

        # # Create temporary file to process the PDF
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        #     temp_file.write(file_content)
        #     temp_file_path = temp_file.name

        # try:
        #     # Load PDF
        #     loader = PyPDFLoader(temp_file_path)
        #     documents = loader.load()

        #     # Combine all text from the PDF
        #     text = " ".join([doc.page_content for doc in documents])

        #     # For very large PDFs, we might want to split and summarize in chunks
        #     if len(text) > 100000:  # If text is very large
        #         # Split text
        #         text_splitter = RecursiveCharacterTextSplitter(
        #             chunk_size=50000,
        #             chunk_overlap=5000
        #         )
        #         chunks = text_splitter.split_text(text)

        #         # Summarize each chunk
        #         summaries = []
        #         for chunk in chunks:
        #             chunk_summary = await self.summarize_text(
        #                 text=chunk,
        #                 model=model_name,
        #                 max_length=max(100, max_length // len(chunks))
        #             )
        #             summaries.append(chunk_summary["summary"])

        #         # Combine summaries and create a final summary
        #         combined_summary = " ".join(summaries)
        #         final_summary = await self.summarize_text(
        #             text=combined_summary,
        #             model=model_name,
        #             max_length=max_length
        #         )

        #         result = final_summary
        #         result["source"] = "pdf"

        #         return result
        #     else:
        #         # Prepare prompt for summarization
        #         prompt = f"Please the PDF document in {max_length} words:\n\n{text}"

        #         completion = self.client.chat.completions.create(
        #             model=model_name,
        #             messages=[
        #                 {"role": "user", "content": prompt}
        #             ],
        #             temperature=0.5
        #         )

        #         return {
        #             "summary": completion.choices[0].message.content,
        #             "model": model_name,
        #             "provider": self.provider_name,
        #             "source": "pdf"
        #         }

        # finally:
        #     # Clean up temp file
        #     if os.path.exists(temp_file_path):
        #         os.unlink(temp_file_path)
