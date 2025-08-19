# ICPC AI Agent System (OpenRouter Edition)

An autonomous multi-agent system designed to assist in solving competitive programming problems, powered by high-performance Large Language Models (LLMs) via the OpenRouter API. This system analyzes problems, devises strategies, generates C++ code, and validates solutions in a streamlined pipeline.

## 🏆 Core Philosophy

The goal of this project is not to replace the human competitor but to act as an incredibly fast and knowledgeable **AI Assistant**. By leveraging powerful remote LLMs, it automates complex reasoning and coding tasks, allowing the competitor to focus on high-level strategy and nuanced problem-solving.

## ✨ Why OpenRouter?

This edition moves from running local LLMs to using the OpenRouter API, which provides several key advantages:

1.  **Access to State-of-the-Art Models:** Use powerful, proprietary models (like GPT-4o, Claude 3 Opus, and various DeepSeek versions) that are too large to run locally.
2.  **Zero Local Resource Cost:** All intensive computation is offloaded to the cloud. This frees up your computer's CPU and RAM, allowing the system to run smoothly even on less powerful laptops.
3.  **Flexibility:** Easily switch between different models—including free-tier options—by changing a single line of code, allowing you to balance cost, speed, and intelligence.
4.  **Constant Updates:** Gain immediate access to the latest and greatest models as soon as they are added to the OpenRouter platform.

## 🛠️ System Architecture

The system operates as a pipeline of specialized agents, managed by an orchestrator:

1.  **Orchestrator (`main.py`):** The main entry point. It takes a raw problem statement as input and coordinates the workflow between agents.
2.  **Analysis Agent:** Parses the raw text of a problem statement, extracting structured data like the problem title, subtasks, constraints, and sample input/output cases.
3.  **Strategy Agent:** The "coach" of the team. For each subtask, it queries the RAG knowledge base to find the most suitable algorithm or data structure.
4.  **Coding Agent:** The primary programmer. It takes the strategy and problem context, then prompts the remote LLM via OpenRouter to generate a complete, runnable C++ solution.
5.  **Validation Agent:** The tester. It automatically compiles the generated C++ code (using a local G++ compiler) and runs it against the sample cases.

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   A C++ compiler (G++). See the [**G++ Installation Guide**](./INSTALL_GXX.md) for detailed instructions.
-   An active internet connection.

### 1. (IMPORTANT) Get and Set Your OpenRouter API Key

This system requires an API key to communicate with OpenRouter.

#### a. Get Your Key

1.  Go to [OpenRouter.ai](https://openrouter.ai/) and sign in.
2.  Click your profile icon in the top-right corner, then select **Keys**.
3.  Click **+ Create Key**, give it a name (e.g., `icpc-assistant`), and click **Create**.
4.  **Copy the key immediately.** It will be shown only once. The key looks like `sk-or-...`.

#### b. Set the Environment Variable

You must store your key as an environment variable for security. **Do not paste it directly into the code.**

**On Windows:**

1.  Open Command Prompt (cmd) **as Administrator**.
2.  Run the following command, replacing `<YOUR_API_KEY>` with the key you copied:
    ```cmd
    setx OPENROUTER_API_KEY "<YOUR_API_KEY>"
    ```
3.  **Close and reopen** any terminal or code editor windows for the change to take effect.

**On macOS / Linux:**

1.  Open your terminal.
2.  Edit your shell's configuration file (e.g., `~/.zshrc`, `~/.bashrc`):
    ```bash
    nano ~/.zshrc
    ```
3.  Add this line to the end of the file, replacing `<YOUR_API_KEY>`:
    ```bash
    export OPENROUTER_API_KEY="<YOUR_API_KEY>"
    ```
4.  Save the file, exit, and then apply the changes by running `source ~/.zshrc` or by restarting your terminal.

### 2. Setup the Project

Clone the repository and install the required Python packages using a virtual environment.

```bash
# Clone the repository
git clone <your-repo-url>
cd ICPC_AI_Assistant_openrouter

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

### 3. Choose Your LLM

Open the `rag_system.py` file and locate the `setup_llm` function. You can change the `model` string to any model available on OpenRouter. The current default is a powerful free-tier model.

```python
# In rag_system.py
self.llm = ChatOpenAI(
    # Find model names on openrouter.ai/models
    model="deepseek/deepseek-r1-0528:free", 
    ...
)
```

### 4. Build the Knowledge Base

Before the first run, or anytime you update the `data/` directory, you must build the vector store:

```bash
# This will read all JSON files, process them, and create the `vectorstore` directory.
python rag_system.py```

### 5. Run the Solver

To solve a problem, run the main orchestrator:

```bash
python main.py
```

The system will prompt you to paste the problem statement. After pasting, type `---` on a new line and press Enter. The agents will then begin their work, communicating with OpenRouter to generate a solution.

---

## 🚧 Current Issues & Future Development Roadmap

This project is in active development. The following are known issues and areas for future improvement.

### 📌 Known Issues (Short-Term Fixes)

1.  **Network Dependency & Errors:**
    -   **Problem:** The system is entirely dependent on an internet connection and the status of the OpenRouter API. Network timeouts or API errors can halt the entire process.
    -   **Proposed Solution:** A `request_timeout` has been added. Further improvements would include implementing a retry-mechanism (e.g., using the `tenacity` library) to automatically retry failed API calls.

2.  **Prompt Sensitivity:**
    -   **Problem:** The quality of the generated code is highly sensitive to the prompt sent to the `CodingAgent`. A slight change in the problem's phrasing can sometimes confuse the LLM.
    -   **Proposed Solution:** Continuously refine the prompts in `agents.py`. Implement a "Few-Shot Prompting" technique where the prompt includes 1-2 examples of a (problem, strategy, code) triplet to give the model a better template to follow.

3.  **Context Window Limitations:**
    -   **Problem:** For extremely long problem statements or very detailed knowledge base entries, the combined context might exceed the model's context window limit, leading to errors or truncated information.
    -   **Proposed Solution:** Switch the `RetrievalQA` chain's type from `"stuff"` (which stuffs all context in one go) to a more advanced type like `"map_reduce"` or `"refine"`, which can handle larger amounts of context by processing it in chunks.

### 🌱 Future Development (Long-Term Vision)

1.  **Dynamic Model Selection Agent:**
    -   **Vision:** Create a "cost-control" agent that runs before the `StrategyAgent`. It would analyze the problem's difficulty and decide which model to use. For easy, ad-hoc problems, it might choose a fast, cheap model. For complex graph or DP problems, it would escalate to a top-tier model like GPT-4o or Claude 3 Opus to ensure the highest quality strategy and code.

2.  **Automated Knowledge Base Expansion:**
    -   **Vision:** Create an agent that can browse contest sites like Codeforces. When it finds a new problem and its official "editorial" (solution analysis), it can automatically use a powerful LLM to parse the editorial and accepted solutions, generating a new `.json` knowledge file to add to the `data/algorithms` directory. This would make the system self-improving.

3.  **Interactive Debugging Agent:**
    -   **Vision:** When a solution fails validation, an `InteractiveDebuggerAgent` would take the code and the failing test case. It would then use an LLM to analyze the code, hypothesize the bug's location, and suggest specific fixes or print statements to add, simulating a pair-programming debugging session.

4.  **Local Fallback Mechanism:**
    -   **Vision:** For offline use or API failures, the system could automatically fall back to a local LLM (like Ollama with a small model). The `main.py` orchestrator would detect the lack of an API key or network connection and dynamically switch the `llm` instance in the agents to a locally-run one.
    
-------------------------------------


## Installation Guide for G++ (MinGW-w64) on Windows using MSYS2

### **English Version**

#### Introduction

This document provides a detailed guide on how to install the GNU C/C++ compiler toolchain (which includes `g++`) on the Windows operating system. This is a mandatory step for the project's `ValidationAgent` to compile and test the C++ files generated by the AI.

We will use **MSYS2**, a modern and powerful software distribution platform, to install the latest version of MinGW-w64.

#### Installation Steps

##### Step 1: Download MSYS2

1.  Go to the official MSYS2 website: [https://www.msys2.org/](https://www.msys2.org/)
2.  Click the download button to get the installer (e.g., `msys2-x86_64-YYYYMMDD.exe`).

##### Step 2: Install MSYS2

1.  Run the installer you just downloaded.
2.  Follow the on-screen instructions.
3.  **❗ Important:** It is highly recommended to keep the default installation path `C:\msys64` to ensure the following configuration steps are accurate.

##### Step 3: Update the Package Database

1.  After installation, an MSYS2 terminal window will open automatically. If not, search for "MSYS2 UCRT64" in your Start Menu and open it.
2.  Run the following command to perform a full system update:
    ```bash
    pacman -Syu
    ```
3.  The process might ask you to close the terminal window. If you see the message `warning: terminate MSYS2 without returning to shell? [Y/n]`, type `Y` and press Enter. Then, **re-open "MSYS2 UCRT64" from the Start Menu** and run the `pacman -Syu` command again to complete the update.

##### Step 4: Install the C++ Toolchain

1.  In the MSYS2 terminal window, run the following command to install the required MinGW-w64 toolchain (which includes `gcc`, `g++`, `gdb`, `make`, etc.):
    ```bash
    pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain
    ```
2.  The system will list the packages in the toolchain and prompt you for a selection.
    
    *   `Enter a selection (default=all):`
    *   Simply **press Enter** to accept the default choice (install all).
3.  The system will ask for confirmation again. Type `Y` and press `Enter` to begin the download and installation process.

##### Step 5: (MOST IMPORTANT) Configure the PATH Environment Variable

To allow Windows to find the `g++` command from any directory, you must add its location to the system `PATH`.

1.  Open the Start Menu, type `env`, and select **"Edit the system environment variables"**.
2.  In the System Properties window, click the **"Environment Variables..."** button.
3.  In the **"System variables"** section (the bottom box), find and select the variable named `Path`, then click **"Edit..."**.
4.  In the Edit environment variable window, click **"New"**.
5.  Paste the exact path to the compiler's `bin` directory. If you used the default installation location, the path is:
    ```
    C:\msys64\ucrt64\bin
    ```
6.  Click **OK** on all windows to save the changes.

##### Step 6: Verify the Installation

1.  **❗ Crucial:** **Close all** open Terminal, Command Prompt, PowerShell, and code editor (VS Code) windows.
2.  Open a **brand new Command Prompt (cmd)**.
3.  Type the following command and press Enter:
    ```bash
    g++ --version
    ```
4.  If the installation was successful, you will see output similar to this, showing the G++ version:
    ```
    g++ (ucrt64-14.0.0-1) 14.0.0
    Copyright (C) 2024 Free Software Foundation, Inc.
    ...
    ```5.  If you receive a `'g++' is not recognized...` error, carefully re-check **Step 5**, ensuring you entered the correct path and have restarted your terminal.

**🚀 Congratulations! Your C++ compilation environment is now ready.**