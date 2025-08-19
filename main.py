# main.py
from agents import AnalysisAgent, StrategyAgent, CodingAgent, ValidationAgent
from rag_system import CPAssistant

def main():
    """
    The entry point of the system.
    Orchestrates the agents to solve a competitive programming problem.
    """
    print("🏆 ICPC AI AGENT SYSTEM (API Edition) 🏆")
    print("=" * 50)
    print("Paste the problem statement below. Type '---' on a new line to finish.")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == '---':
                break
            lines.append(line)
        except EOFError:
            break
    
    problem_text = '\n'.join(lines)
    
    if not problem_text.strip():
        print("❌ No problem statement provided. Exiting.")
        return

    # --- Step 1: Initialize Systems and Agents ---
    print("\n--- INITIALIZING SYSTEM ---")
    rag_system = CPAssistant()
    rag_system.initialize()
    
    analysis_agent = AnalysisAgent()
    strategy_agent = StrategyAgent(rag_system)
    coding_agent = CodingAgent(rag_system.llm) # Reuse the powerful LLM
    validation_agent = ValidationAgent()
    
    # --- Step 2: Start the Solver Pipeline ---
    print("\n--- STARTING SOLVER PIPELINE ---")
    problem = analysis_agent.analyze(problem_text)
    
    print("\n" + "="*60)
    print("📊 STRATEGY & RESULTS SUMMARY:")
    print("="*60)
    
    all_valid = True
    for subtask in problem.subtasks:
        print(f"\n--- Processing Subtask {subtask.id} (Difficulty: {subtask.difficulty}) ---")
        
        # Agent 1: Find a strategy
        strategy = strategy_agent.get_strategy(problem, subtask)
        
        # Agent 2: Write code
        cpp_code = coding_agent.generate(strategy, problem)
        
        # Save the generated code to a file
        filename = f"subtask_{subtask.id}_solution.cpp"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cpp_code)
        print(f"💾 Code for Subtask {subtask.id} saved to file: {filename}")
        
        # Agent 3: Validate the code
        is_valid = validation_agent.validate(cpp_code, problem.samples)
        if not is_valid:
            all_valid = False
            print(f"🚨 WARNING: Code for Subtask {subtask.id} failed sample validation!")

    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETE 🎉")
    if all_valid:
        print("✅ All generated solutions passed the sample tests.")
    else:
        print("⚠️  One or more solutions failed the sample tests. Please review the code.")

if __name__ == "__main__":
    main()