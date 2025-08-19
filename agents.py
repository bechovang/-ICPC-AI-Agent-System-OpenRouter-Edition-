# agents.py
import re
import os
import subprocess
from dataclasses import dataclass, field
from typing import List, Tuple
from rag_system import CPAssistant
from langchain_core.language_models.chat_models import BaseChatModel

# --- Data structures for storing problem information ---
@dataclass
class Subtask:
    id: int
    constraints: str
    difficulty: str

@dataclass
class Problem:
    title: str
    statement: str
    samples: List[Tuple[str, str]]
    subtasks: List[Subtask] = field(default_factory=list)

# --- Agent Definitions ---

class AnalysisAgent:
    """Agent specializing in parsing raw problem text, with improved logic."""
    def analyze(self, text: str) -> Problem:
        print("🕵️  Analysis Agent: Starting problem analysis...")
        title = self._extract_title(text)
        samples = self._extract_samples(text)
        subtasks = self._extract_subtasks(text)
            
        print(f"✅ Analysis Agent: Analysis complete. Found {len(subtasks)} subtask(s) and {len(samples)} sample(s).")
        return Problem(title=title, statement=text, samples=samples, subtasks=subtasks)

    def _extract_title(self, text: str) -> str:
        # Tries to find pattern like "A. Problem Title" first
        match = re.search(r'^[A-Z]\.\s*(.*?)\n', text) 
        if match:
            return match.group(1).strip()
        
        # Fallback to the original pattern
        match = re.search(r'Problem\s+[A-Z]?\s*[:.]?\s*(.+?)(?:\n|\r)', text, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown Problem"

    def _extract_samples(self, text: str) -> List[Tuple[str, str]]:
        """
        Extracts sample cases with a more robust, multi-pattern approach.
        """
        samples = []
        
        # Pattern 1: Look for a large "Example" block first
        example_block_match = re.search(r'Example\s*\n(.*?)(?=\n\n\w|$)', text, re.DOTALL | re.IGNORECASE)
        if example_block_match:
            example_block = example_block_match.group(1)
            # Now find Input/Output within this block, allowing for optional "Copy" text
            io_match = re.search(r'Input(?:Copy)?\s*\n(.*?)\s*Output(?:Copy)?\s*\n(.*?)$', example_block, re.DOTALL | re.IGNORECASE)
            if io_match:
                inp = io_match.group(1).strip()
                outp = io_match.group(2).strip()
                samples.append((inp, outp))
        
        # Pattern 2: Fallback to find any Input/Output pairs if the Example block fails
        if not samples:
            pattern_generic = r'Input\s*\n(.*?)\n\s*Output\s*\n(.*?)(?=\n\n\w|$)'
            matches_generic = re.finditer(pattern_generic, text, re.DOTALL | re.IGNORECASE)
            for match in matches_generic:
                inp = match.group(1).strip()
                outp = match.group(2).strip()
                samples.append((inp, outp))

        return samples

    def _extract_subtasks(self, text: str) -> List[Subtask]:
        subtasks = []
        subtasks_text = re.findall(r'Subtask\s+(\d+)\s*.*?:\s*(.*?)(?=Subtask|\Z)', text, re.DOTALL | re.IGNORECASE)
        
        if subtasks_text:
            for i, (sub_id, const) in enumerate(subtasks_text):
                subtasks.append(Subtask(id=int(sub_id), constraints=const.strip(), difficulty=self._classify(const)))
        else:
            subtasks.append(Subtask(id=1, constraints="Full constraints", difficulty="medium"))
        
        return subtasks

    def _classify(self, const: str) -> str:
        nums = [int(n) for n in re.findall(r'(\d+)', const)]
        max_n = max(nums) if nums else 0
        if max_n <= 2000: return "easy"
        if max_n <= 200000: return "medium"
        return "hard"

class StrategyAgent:
    """Agent specializing in finding solution strategies by querying the RAG system."""
    def __init__(self, rag_system: CPAssistant):
        self.rag = rag_system

    def get_strategy(self, problem: Problem, subtask: Subtask) -> str:
        """Finds a strategy by describing the problem in detail to the RAG."""
        print(f"🤔 Strategy Agent: Finding strategy for Subtask {subtask.id} ({subtask.difficulty})...")
        query = f"""
        Analyze the following competitive programming problem and suggest the best C++ algorithm or data structure.
        Problem Summary: {problem.statement[:700]}... 
        Constraints: {subtask.constraints}
        Your answer should be based on matching the problem's core idea with examples from your knowledge base. Provide a full contextual explanation.
        """
        response = self.rag.ask(query)
        strategy = response.get("result", "Default to brute force or a simple simulation.")
        print(f"✅ Strategy Agent: Strategy found.")
        return strategy

class CodingAgent:
    """Agent specializing in writing C++ code based on a given strategy."""
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        try:
            with open('data/templates/cpp_template.cpp', 'r', encoding='utf-8') as f:
                self.template = f.read()
        except FileNotFoundError:
            print("❌ Error: Template file 'data/templates/cpp_template.cpp' not found.")
            self.template = "// Template not found"

    def generate(self, strategy: str, problem: Problem) -> str:
        """Generates a complete C++ solution based on a highly detailed prompt."""
        print("💻 Coding Agent: Starting C++ code generation...")
        prompt = f"""
You are an elite C++ competitive programmer, known for writing clean, efficient, and bug-free code that passes under tight time limits.
Your task is to write a complete C++ solution for the given problem, following the provided strategy.

**PROBLEM STATEMENT:**
---
{problem.statement}
---

**STRATEGY & CONTEXT FROM KNOWLEDGE BASE:**
---
{strategy}
---

**INSTRUCTIONS:**
1.  Your final output MUST be a single, complete, runnable C++ code block and nothing else.
2.  Incorporate the provided C++ template structure: use fast I/O, put the main logic in a `solve()` function, and handle multiple test cases if the problem requires it.
3.  Adapt any example code from the context to perfectly match the specific input/output format and constraints of the current problem.
4.  Pay close attention to any "Common Pitfalls" mentioned in the context and write robust code to avoid them (e.g., use `long long` for large sums, handle 1-based vs 0-based indexing correctly).
5.  Do NOT include any explanations, comments, or text outside of the final ````cpp ... ```` code block.

COMPLETE C++ SOLUTION:
"""
        response = self.llm.invoke(prompt)
        final_code = self._extract_cpp_code(response.content)
        
        print("✅ Coding Agent: Code generation complete.")
        return final_code
    
    def _extract_cpp_code(self, text: str) -> str:
        match = re.search(r'```(?:cpp)?\n(.*?)```', text, re.DOTALL)
        return match.group(1).strip() if match else text

class ValidationAgent:
    """Agent specializing in compiling and testing code against sample cases."""
    def validate(self, code: str, samples: List[Tuple[str, str]]) -> bool:
        print("🧪 Validation Agent: Starting validation...")
        if not samples:
            print("⚠️  Validation Agent: No samples to validate against.")
            return True
        
        try:
            with open("temp_solution.cpp", "w", encoding='utf-8') as f: f.write(code)
            compile_result = subprocess.run(["g++", "temp_solution.cpp", "-o", "temp_solution", "-std=c++17", "-O2"], capture_output=True, text=True)
            if compile_result.returncode != 0:
                print(f"❌ Validation Agent: Compilation error!\n{compile_result.stderr}")
                return False
            
            for i, (inp, outp) in enumerate(samples):
                run_result = subprocess.run(["./temp_solution"], input=inp, capture_output=True, text=True, timeout=3)
                if run_result.returncode != 0:
                    print(f"❌ Validation Agent: Runtime error on sample {i+1}!\n{run_result.stderr}")
                    return False
                if run_result.stdout.strip() != outp.strip():
                    print(f"❌ Validation Agent: Wrong answer on sample {i+1}!")
                    print(f"   - Expected: '{outp.strip()}'")
                    print(f"   - Got:      '{run_result.stdout.strip()}'")
                    return False
            
            print("✅ Validation Agent: All samples passed!")
            return True
        finally:
            for f in ["temp_solution.cpp", "temp_solution", "temp_solution.exe"]:
                if os.path.exists(f): os.remove(f)