"""
AI Resume Tailoring Service
"""

import os
from typing import Optional


def tailor_resume_with_ai(job_description: str, current_resume_text: str) -> str:
    """
    Use AI to rewrite resume to match job description
    
    Args:
        job_description: The target job description
        current_resume_text: The current resume text
    
    Returns:
        str: AI-tailored resume text
    """
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        # Return demo response following the same structured format
        return f"""## 🔍 KEY CHANGES & IMPROVEMENTS
* **Demo Mode:** Add your OpenAI API key to enable real AI-powered tailoring
* **Placeholder Response:** This is a template showing the expected format
* **To Enable:** Add OPENAI_API_KEY to your .env file

## 📄 TAILORED RESUME CONTENT
{current_resume_text}

---
NOTE: This is DEMO MODE. To enable AI-powered resume tailoring with keyword optimization 
and intelligent rewriting, please add your OpenAI API key to the .env file."""
    
    try:
        # Import ChatOpenAI and message types
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        
        # Create the structured prompt
        system_prompt = """You are an expert resume writer and ATS optimization specialist. 
Your task is to analyze a resume and job description, then provide a detailed breakdown of changes 
followed by the complete tailored resume."""
        
        user_prompt = f"""Job Description:
{job_description}

Current Resume:
{current_resume_text}

Please provide your response in this EXACT format:

## 🔍 KEY CHANGES & IMPROVEMENTS
* **Added Keyword:** [List specific keywords from the JD that you added]
* **Rewrote:** [Show before -> after examples of significant changes]
* **Focus Shift:** [Explain what skills/experiences you emphasized and why]
* **ATS Optimization:** [Mention any changes to improve ATS compatibility]

## 📄 TAILORED RESUME CONTENT
[Write the complete, polished, tailored resume here. Make it professional, achievement-oriented, and keyword-rich. 
Keep the same general structure but optimize all content to match the job description requirements.]

IMPORTANT: 
- The KEY CHANGES section should be bullet points explaining your changes
- The TAILORED RESUME CONTENT section should be the complete, final resume ready for submission
- Include ALL relevant keywords from the job description naturally
- Maintain a professional tone throughout
- Focus on quantifiable achievements where possible"""
        
        # Call the LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        return response.content
    
    except ImportError as e:
        return f"""## 🔍 KEY CHANGES & IMPROVEMENTS
* **Error:** langchain-openai not installed properly
* **Fix Required:** Run: pip install langchain-openai
* **Details:** {str(e)}

## 📄 TAILORED RESUME CONTENT
{current_resume_text}

---
ERROR: Please install required dependencies to enable AI features."""
    
    except Exception as e:
        return f"""## 🔍 KEY CHANGES & IMPROVEMENTS
* **Error during AI processing:** {str(e)}
* **Fallback:** Returning original resume without modifications
* **Suggestion:** Check your OpenAI API key and network connection

## 📄 TAILORED RESUME CONTENT
{current_resume_text}

---
ERROR: AI processing failed. Please check the error message above."""
