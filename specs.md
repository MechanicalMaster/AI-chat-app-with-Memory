Below is a detailed technical specification (tech spec) for an MVP chat application that incorporates robust memory management and strict adherence to a guiding script (for example, a bank’s loan policy). This spec outlines the system architecture, major components, data flow, and implementation steps, focusing on:

1. **Memory Management:** Using a mix of full conversation history, sliding windows, and summarization for long-term memory.
2. **Script Adherence:** Enforcing a fixed “system prompt” or guiding script that constrains the LLM to answer only on-policy questions.

---

# Technical Specification for a Domain-Specific LLM Chat App (MVP)

## 1. Overview

**Objective:**  
Develop an MVP chatbot application that:
- Maintains conversation context (memory management) over multiple turns.
- Strictly adheres to a predefined guiding script (e.g., a bank’s loan policy).
- Rejects off-topic queries with a standardized refusal message.
- Provides an interface for both end-users and administrators (for monitoring and troubleshooting).

**Target Audience:**  
Bank customers seeking loan-related information.

**Primary Features:**
- Persistent conversation memory using multiple memory strategies.
- Strict system prompt that enforces domain adherence.
- Input and output filtering to prevent off-topic interactions.
- Lightweight, scalable architecture suitable for production (MVP).

---

## 2. Architecture Overview

### 2.1. High-Level Architecture Diagram

```
                    +-------------------------+
                    |     Frontend UI       |  <-- Web/Mobile Client
                    +-------------------------+
                              |
                              | REST/WebSocket API
                              v
                    +-------------------------+
                    |  Chat App Backend API   |  
                    |  (Flask/FastAPI/Django) |
                    +-------------------------+
                              |
                              |  (Conversation Data)
                              v
                    +-------------------------+         +------------------------+
                    |    Memory Management    |  <----> |    Database (Optional) |
                    | (Buffer, Summarization,  |         |   (Chat History, Logs) |
                    |  Sliding Window)        |         +------------------------+
                    +-------------------------+
                              |
                              |  Context + Guiding Script
                              v
                    +-------------------------+
                    |   LLM Chat Engine       |   <-- OpenAI GPT-3.5/4 (via LangChain)
                    +-------------------------+
                              |
                              v
                    +-------------------------+
                    |   Output Filtering      |  <-- Ensures responses adhere to script
                    +-------------------------+
```

### 2.2. Main Components

1. **Frontend UI:**  
   - Web or mobile interface where users can input questions and view responses.
   - Displays controls (e.g., “View History”, “Clear History”).

2. **Backend API:**  
   - Developed in Python (Flask/FastAPI) to handle user requests.
   - Routes to the LLM Chat Engine and Memory Management module.
   - Implements input validation and filtering.

3. **Memory Management Module:**  
   - Implements conversation history using LangChain memory types:
     - **Buffer Memory:** For full conversation history (for short interactions).
     - **Sliding Window Memory:** Retains the most recent N messages.
     - Offers functions to load, update, and clear chat history.

4. **LLM Chat Engine:**  
   - Integrates with Gemini 1.5 via LangChain.
   - Uses a fixed system prompt (guiding script) to enforce domain-specific behavior.
   - Accepts concatenated context from the memory module and the current user query.

5. **Output Filtering/Guardrails:**  
   - Post-processes LLM responses to ensure adherence to the guiding script.
   - If a response is off-policy, returns a standard refusal message (“I’m sorry, I can only answer questions related to our loan policy.”).

---

## 3. Detailed Component Specifications

### 3.1. Frontend UI

- **Framework:** Basic HTML and TS rendered in the browser for web
- **Features:**
  - Chat window for input and output.
  - Buttons for “View History” and “Clear Chat”.
  - Responsive design and minimal latency.

### 3.2. Backend API

- **Language/Framework:** Python with Flask or FastAPI.
- **Endpoints:**
  - `POST /chat`: Receives user message, returns LLM response.
  - `GET /history`: Retrieves conversation history.
  - `POST /clear`: Clears conversation history.
- **Security:**
  - API key-based authentication.
  - Input sanitization to prevent injection attacks.
  
### 3.3. Memory Management Module

- **Implementation:** Use LangChain’s memory modules.
  - **Buffer Memory:** `ConversationBufferMemory` for initial prototyping.
  - **Sliding Window Memory:** `ConversationBufferWindowMemory(k=N)` where N is configurable (e.g., 10).
 - **APIs:**
  - `load_memory(session_id)`: Loads memory for current session.
  - `save_context(session_id, user_input, llm_response)`: Appends new messages.
  - `clear_memory(session_id)`: Clears history.
- **Design Note:** Ensure that the guiding script (system prompt) is always prepended to every LLM request.

### 3.4. LLM Chat Engine

- **Integration:** Via LangChain.
- **Prompt Template:**
  - **System Prompt (Guiding Script):**  
    > "You are a bank loan officer. Answer only questions about our bank’s loan policy. If asked something else, reply: 'I'm sorry, I can only answer questions related to our loan policy.'"
  - **User Input:** Concatenate memory (history) and the current user message.
- **Configuration:**
  - Temperature: Low (e.g., 0.3) for deterministic output.
  - Max tokens: Set according to response length requirements.

### 3.5. Output Filtering/Guardrails

- **Method:**
  - After receiving the LLM response, run it through a filter (could be a simple function or a second LLM call) to check for off-topic content.
  - If detected, override the output with a standard message.
- **Algorithm:**
  - Keyword matching against off-policy terms.
  - Check if response deviates from expected tone (using regular expressions or similarity metrics).
  
## 4. Data Flow and Interaction Sequence

1. **User sends a message** via the Frontend UI.
2. **Backend API receives the message**, validates and sanitizes it.
3. **Memory Management Module** loads the current conversation history (sliding window or summarized memory).
4. **LLM Chat Engine constructs the prompt**:  
   - Prepend the system prompt (guiding script).
   - Append the conversation history.
   - Append the current user query.
5. **LLM generates a response**.
6. **Output Filtering** checks the response for policy adherence:
   - If compliant, return response.
   - If off-topic, return a standard refusal message.
7. **Memory Management Module updates the conversation history** with the new exchange.
8. **Backend API sends the response** to the Frontend UI.
9. **Frontend UI displays the response**, optionally showing response time.
10. **User may view or clear history** via designated buttons, triggering API calls.

---

## 5. Development Milestones and Timeline

### Milestone 1: Environment Setup and Basic Chatbot
- Set up Python environment, install LangChain and necessary libraries.
- Develop basic backend API endpoints.
- Integrate Gemini 1.5 LLM via LangChain.


### Milestone 2: Memory Management Module
- Implement ConversationBufferWindowMemory.
- Implement summarization module for long histories.
- Integrate memory management into the backend.


### Milestone 3: Script Adherence and Output Filtering
- Develop system prompt with strict domain instructions.
- Build output filtering functions to enforce script adherence.
- Test with various off-topic queries.


### Milestone 4: Frontend UI and Integration
- Develop a minimal chat interface.
- Connect frontend to backend API.
- Implement “View History” and “Clear Chat” features.


### Milestone 5: Testing, Debugging, and Documentation
- Conduct integration tests and debugging.
- Write technical documentation and user guide.




