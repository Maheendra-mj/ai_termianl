# 🖥️ AI Terminal: A Stateful, AI-Powered Command Line Interface

**AI Terminal** is a fully-featured, hybrid command-line interface that integrates the power of a fine-tuned language model directly into your shell. It allows users to execute standard shell commands while also providing the ability to translate natural language into complex bash commands through a stateful, AI-powered backend.

This project was developed in two distinct phases: first, the fine-tuning of a specialized language model, and second, the construction of a robust client-server application to serve and interact with that model.

---

## 🚀 Key Features

- **Hybrid Terminal**  
  Seamlessly run standard commands (`ls -l`, `git status`) and AI-powered queries (`? find all python files modified in the last 2 days`).

- **Stateful AI**  
  The terminal remembers the context of your conversation via a custom **Model Context Protocol (MCP)**, allowing for follow-up questions.

- **Specialized Fine-Tuned Model**  
  At its heart is a **Qwen/Qwen2-1.5B-Instruct** model, fine-tuned on the `nl2bash` dataset using **LoRA** for high accuracy in command generation.

- **Robust Client-Server Architecture**  
  A decoupled frontend (**AI Terminal Client**) and backend (**MCP Server**) built with modern technologies like **FastAPI** and **asyncio**.

- **User-Friendly Interface**  
  Built with **rich** and **prompt_toolkit** for a polished experience with command history, syntax highlighting, and clean output.

- **Persistent Command History**  
  A local **SQLite database** logs all executed commands for your records.

---

## 🏛️ Project Evolution & Architecture

This project is the result of a two-phase development process, evolving from a machine learning experiment into a complete application.

### � Phase 1: Model Fine-Tuning

The core intelligence was developed in a Jupyter Notebook. The process involved:

- **Base Model:** `Qwen/Qwen2-1.5B-Instruct`  
- **Dataset:** `jiacheng-ye/nl2bash`  
- **Technique:** Parameter-Efficient Fine-Tuning (**PEFT**) using **LoRA (Low-Rank Adaptation)**  

The dataset was preprocessed into a structured JSON schema, and the model was trained to replicate this format. This forces the model to provide not just a command, but also a clear explanation, making its output more reliable. By using LoRA, we trained only ~0.14% of the model's parameters, achieving a **BLEU score of 30.12** on the test set.

### 🔹 Phase 2: Application Architecture

With a powerful model ready, the next step was to build a real-world application around it. We chose a robust client-server architecture:

- **The MCP Server (Backend):**  
  A stateful FastAPI server that acts as the "brain." It hosts the AI logic, manages the connection to the Gemini API, and implements the Model Context Protocol (MCP) by creating and managing a conversation history for each client session.

- **The AI Terminal Client (Frontend):**  
  The installable command-line application you run. It provides the UI, captures input, and decides whether to execute a command locally or send it to the MCP Server for AI processing.

---


## 📊 System Architecture (ASCII Diagram)

```text
+---------------------------------+      (HTTP Request)      +-----------------------------------------+
|                                 |   AI Query (? prefix)    |                                         |
|      AI Terminal Client         +------------------------> |               MCP Server                |
|    (User's Local Machine)       |      & session_id        |            (Backend Service)            |
|                                 |                          |                                         |
|---------------------------------|                          |-----------------------------------------|
| - Captures user input           |                          | - Hosts stateful AI Logic (FastAPI)     |
| - Manages local shell execution |                          | - Manages Session History (MCP)         |
| - Displays plans and output     |                          | - Calls Gemini API / Fine-Tuned Model   |
| - Stores command history (DB)   |                          | - Returns structured JSON plan          |
|                                 |   <------------------------+                                       |
|                                 |    JSON Command Plan     |                                         |
|                                 |     (HTTP Response)      |                                         |
+---------------------------------+                          +-----------------------------------------+
```

---


## ⚙️ Installation & Setup

### 📌 Prerequisites
- Python **3.10+**
- A **Google Gemini API Key**

### 1. Clone the Repository
```bash
git clone https://github.com/Maheendra-mj/ai_termianl.git
cd ai_termianl
```

### 2. Run the Installer
This script will create a virtual environment, install all dependencies, and make the `ai-terminal` command available.

```bash
chmod +x install.sh
./install.sh
```

### 3. Set Your API Key
The MCP Server requires your Gemini API key to function.

```bash
export GEMINI_API_KEY='YOUR_API_KEY_HERE'
```

---

## ▶️ How to Run

Because this is a client-server application, you need to run the two components in two separate terminals.

### 1. In Terminal A - Start the MCP Server
```bash
# Make sure you are in the project directory and have set your API key
source venv/bin/activate
uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000
```
(Leave this terminal running.)

### 2. In Terminal B - Launch the AI Terminal Client
```bash
# Make sure you are in the project directory
source venv/bin/activate
ai-terminal
```

You will see the welcome message and the `➤` prompt. You are now ready to go!

---

## 🧑‍💻 Example Usage

### Standard Command
```bash
➤ ls -la
```

### AI-Powered Query
```bash
➤ ? find all markdown files in my home directory and count their lines
```

### Follow-up Query (using conversational memory)
```bash
➤ ? now, copy the largest one to a backup folder
```

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.

