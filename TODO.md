# TODO: Replace GeminiService with CohereService in RAGService

- [x] Update class docstring: Change "with Gemini LLM" to "with Cohere LLM"
- [x] In __init__: Change parameter from gemini_service to cohere_service
- [x] In __init__: Update docstring from "gemini_service: Gemini AI service" to "cohere_service: Cohere AI service"
- [x] In __init__: Change assignment from self.gemini_service = gemini_service to self.cohere_service = cohere_service
- [x] In answer_question: Change question_embedding = await self.gemini_service.generate_embedding(question) to use self.cohere_service
- [x] In answer_question: Change answer = await self.gemini_service.generate_chat_response(...) to use self.cohere_service
- [x] Verify changes by reading the updated file