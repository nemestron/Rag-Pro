# User Manual

Welcome to RAG Pro. This application allows you to "talk" to your documents securely and accurately.

## Step 1: Uploading Data
1. Open the application. On the left-hand sidebar, you will see the **Document Ingestion** panel.
2. Select your data source type:
   * **URL**: Paste links to web articles or documentation.
   * **PDF / DOCX / TXT**: Upload local files from your computer.
   * **Raw Text**: Paste text directly into the provided text box.
3. Click the primary **Process Documents** button. 
4. Wait for the success message confirming that the documents have been chunked and indexed.

## Step 2: Asking Questions
1. Once processing is complete, the main chat interface will unlock.
2. Type your question in the chat input box at the bottom of the screen.
3. The AI will analyze your provided documents and generate an answer.

## Step 3: Verifying the Answer
1. Below the AI's response, click the expander titled **"View Retrieved Context"**.
2. This will reveal the exact paragraphs the AI used to formulate its answer, allowing you to manually verify the factual accuracy of the response.
3. If you ask a question unrelated to the uploaded documents, the system will actively refuse to answer to prevent hallucination.
