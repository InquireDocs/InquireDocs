# import httpx
import logging
# import os
# import tempfile
from typing import Optional, Dict, Any

# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama

from app.core.config import settings
from app.core.summarizer.base import BaseSummarizer


logger = logging.getLogger(__name__)


class OllamaSummarizer(BaseSummarizer):
    """Ollama summarizer implementation"""

    def __init__(self):
        """Initialize Ollama with base URL from settings"""
        self.server_url = settings.ollama_base_url

    @property
    def provider_name(self) -> str:
        return "ollama"

    async def summarize_text(
        self,
        text: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = settings.ollama_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: Optional[int] = settings.default_model_temperature,
    ) -> Dict[str, Any]:
        """Summarize text using Ollama"""
        try:
            # Prepare LLM
            llm = ChatOllama(
                base_url=self.server_url,
                model=model,
                temperature=temperature,
                num_predict=max_length
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
        model: Optional[str] = settings.ollama_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: Optional[int] = settings.default_model_temperature,
    ) -> Dict[str, Any]:
        """Summarize PDF using Ollama"""
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
        #         prompt = f"summarize the PDF document in {max_length} words:\n\n{text}"

        #         # Prepare request data
        #         request_data = {
        #             "model": model_name,
        #             "prompt": prompt,
        #             "temperature": 0.5,
        #         }

        #         async with httpx.AsyncClient() as client:
        #             response = await client.post(
        #                 f"{self.base_url}/api/generate",
        #                 json=request_data,
        #                 timeout=90.0  # Longer timeout for PDF processing
        #             )
        #             response.raise_for_status()
        #             result = response.json()

        #         return {
        #             "summary": result.get("response", ""),
        #             "model": model_name,
        #             "provider": self.provider_name,
        #             "source": "pdf"
        #         }

        # finally:
        #     # Clean up temp file
        #     if os.path.exists(temp_file_path):
        #         os.unlink(temp_file_path)
