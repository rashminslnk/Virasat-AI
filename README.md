# 🏛️ Virasat AI: Multi-Agent Heritage Concierge

**Virasat AI** is an intelligent, multi-agent system designed to transform how users explore and plan visits to India’s iconic heritage sites. Built for the **Google Gen AI APAC Hackathon**, this project demonstrates the orchestration of specialized AI agents to handle real-world research and travel management workflows.

---

<img width="1910" height="936" alt="image" src="https://github.com/user-attachments/assets/bc47beaa-5af5-44d7-a679-63193e08a247" />


## 🚀 The Problem it Solves
Planning a cultural trip to India can be overwhelming due to the sheer volume of historical data and the logistical challenge of organizing itineraries. 

**Virasat AI solves this by:**
* **Bridging the Gap:** It connects high-level historical research (Wikipedia/LangChain) with structured personal data storage (Google Firestore).
* **Automating Tasks:** Instead of just chatting, the AI performs actions—specifically, managing a persistent "To-Visit" list.
* **Simplifying Discovery:** It provides a single conversational interface to learn about architectural styles, dynasties, and cultural significance while simultaneously building a travel plan.

---

## 🛠️ Tech Stack
* **Core Framework:** Google Agent Development Kit (ADK)
* **LLM:** Gemini 2.0 Flash (Vertex AI)
* **Database:** Google Cloud Firestore/Datastore (Database ID: `genrash`)
* **Deployment:** Google Cloud Run (Region: `europe-west1`)
* **Tools:** LangChain Wikipedia Integration, Custom Python Function Tools

---

## 🤖 Multi-Agent Architecture
The system utilizes a **Sequential & Orchestrated Workflow**:

1.  **Virasat Guide (Root Agent):** The primary entry point. It identifies user intent—whether they want to research a site or view their saved list.
2.  **Heritage Historian (Sub-Agent):** A research specialist that uses the Wikipedia Tool to fetch architectural and historical data.
3.  **Itinerary Manager (Sub-Agent):** A database specialist that writes and reads from the `genrash` Firestore database to track the user's "To-Visit" list.

---

## 📋 Environment Configuration
To run this project locally or deploy it, you must configure a `.env` file based on the template below:

```text
PROJECT_ID=your-google-cloud-project-id
PROJECT_NUMBER=your-project-number
SA_NAME=lab2-cr-service
SERVICE_ACCOUNT=your-service-account-email
MODEL="gemini-2.0-flash"
DB_ID="genrash"
GOOGLE_API_KEY=your-api-key-from-ai-studio
