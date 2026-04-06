# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyễn Hoàng Nghĩa
- **Student ID**: 2A202600161
- **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: `src/tools/calculate_course_fee.py`
- **Code Highlights**:
```python
def calculate_course_fee(total_fee: Any, total_hours: Any) -> str:
    try:
        # Converting string inputs from LLM to float for calculation
        fee = float(total_fee)
        hours = float(total_hours)
        if hours <= 0: 
            return "Error: Total hours must be greater than 0."
        
        fee_per_hour = fee / hours
        return f"{fee_per_hour:,.0f} VNĐ/hour"
    except Exception as e:
        return f"Calculation Error: {str(e)}"

CALC_TOOL_METADATA = {
    "name": "calculate_course_fee",
    "description": "Calculates the average tuition fee per study hour based on total cost and duration.",
    "parameters": "total_fee (float), total_hours (int)",
    "func": calculate_course_fee 
}
```

- **Documentation**: My tool serves as the "Mathematical Reasoning" component of the agent. While the Search Tool retrieves raw tuition data from the web, my module processes these numerical values into a standardized hourly rate. It interacts with the ReAct loop by providing a structured Observation, allowing the Agent to form a logical comparison in its Final Answer.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: The Agent correctly identified the necessary tool (search_course_info) and generated the correct Action format. However, the program immediately crashed with a TypeError: expected string or bytes-like object, got 'dict'. This error occurred right after the LLM response, preventing the Agent from proceeding to the tool execution step.
- **Log Source**: logs/2026-04-06.log - Event: LLM_GENERATE_OUTPUT.
The log data showed that the response returned from the LLM provider was a structured Dictionary: {'text': 'Thought: I need to search...', 'usage': {...}, 'model': 'gemini-2.5-flash'} rather than a raw text string.
- **Diagnosis**: The generate() method in the GeminiProvider class was designed to return the full response object (including metadata like token usage) from the API. Meanwhile, the ReAct parser in agent.py uses the re.search() function to extract Action: and Thought: keywords. Since Python’s re module only accepts strings or bytes-like objects, passing a Dictionary directly triggered a TypeError.
- **Solution**: Change the run() method of ReActAgent

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: How did the `Thought` block help the agent compared to a direct Chatbot answer?
    The Thought block acts as a "Chain of Thought" mechanism. Unlike a standard chatbot that might guess a price, the ReAct Agent "realizes" it lacks specific information, triggers a search, and then performs calculations. This transparency significantly reduces hallucinations.
2.  **Reliability**: In which cases did the Agent actually perform *worse* than the Chatbot?
    The Agent can be less reliable than a simple chatbot when external tools return messy or unstructured data (e.g., complex JSON from a search API). In những trường hợp này, Agent có thể bị lặp (loop) khi cố gắng xử lý các đầu vào không hợp lệ.
3.  **Observation**: How did the environment feedback (observations) influence the next steps?
    Observations provide the necessary "Grounding." When my calculation tool returned an error due to missing duration data, the Agent used that Observation to refine its next Thought, deciding to search cụ thể cho "course duration" thay vì bỏ cuộc.
---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Implement Tool Parallelism using Python's asyncio. This would allow the agent to fetch data from multiple tuition sources simultaneously instead of waiting for one search to finish.
- **Safety**: Add a Validation Layer for tool arguments. Using Pydantic models to validate the total_fee and total_hours before they reach the function would prevent runtime crashes and improve security.
- **Performance**: Implement Long-term Memory (Vector Database). If a user asks the same comparison question later, the agent could retrieve previous observations from memory instead of performing expensive API search calls again.
---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
