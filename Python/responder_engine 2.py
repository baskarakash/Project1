import os
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

GPT_AZURE_KEY = os.getenv("GPT_AZURE_KEY")
GPT_AZURE_ENDPOINT = os.getenv("GPT_AZURE_ENDPOINT")
GPT_AZURE_DEPLOYMENT = os.getenv("GPT_AZURE_DEPLOYMENT")
GPT_AZURE_API_VERSION = os.getenv("GPT_AZURE_API_VERSION", "2024-12-01-preview")

class ResponderEngine:
    def __init__(self):
        self.api_url = (
            f"{GPT_AZURE_ENDPOINT}openai/deployments/"
            f"{GPT_AZURE_DEPLOYMENT}/chat/completions"
            f"?api-version={GPT_AZURE_API_VERSION}"
        )
        self.headers = {
            "Content-Type": "application/json",
            "api-key": GPT_AZURE_KEY,
        }

    def query(self, prompt: str, system_prompt: str):
        body = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2048
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=body)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            return f"Error communicating with Azure OpenAI: {str(e)}"

    def run_quality_analysis(self, code, repo_name):
        system_prompt = f"""You are a code reviewer. Analyze this code from {repo_name} for general quality and provide the basic feedback
          on its structure, readability and naming conventions precisely. DO NOT ADD ANY SUGGESTIONS FOR IMPROVEMENT HERE"""
        prompt = f"""Code to Analyze: {code}"""
        return self.query(prompt, system_prompt)

    def run_bug_detection(self, code):
        system_prompt = """You are a bug detection expert. Analyze the following code and identify any possible bugs, logic errors, or syntax issues.
For each bug, make sure you mention the line where the issue is sugges the fixed code there only."""
        prompt = f"code: {code}"
        return self.query(prompt, system_prompt)

    def run_optimization(self, code):
        system_prompt = """You are a performance optimization expert. Suggest optimizations to improve speed, memory usage, standards and security vulnerabilities for the following code.
Only include practical improvements."""
        prompt = f"code: {code}"
        return self.query(prompt, system_prompt)

    # def run_standards_compliance(self, code):
    #     system_prompt = """You are a Standard Compliance Agent. Your task is to review the provided code and ensure it adheres to the coding standards and best practices of the respective programming language.
    #      The languages and their standards are as follows:
    #      Python: PEP8
    #     Java: Google Java Style Guide
    #     JavaScript: Airbnb JavaScript Style Guide
    #     C++: C++ Core Guidelines
    #     HTML: W3C HTML5 Specification"""
    #     prompt = f"code: {code}"
    #     return self.query(prompt, system_prompt)

    # def run_security_analysis(self, code):
    #     system_prompt = """You are a Security Analysis Agent. Your task is to review the provided code and ensure it is secure,
    #       free from data leaks, memory leaks, and vulnerabilities. The languages and their security standards are as follows:
    #       Python: OWASP Python Security Guidelines
    #     Java: OWASP Java Security Guidelines
    #     JavaScript: OWASP JavaScript Security Guidelines
    #     C++: CERT C++ Secure Coding Standard
    #     HTML: OWASP HTML Security Guidelines"""
    #     prompt = f"code: {code}"
    #     return self.query(prompt, system_prompt)

#     def run_docstring_generation(self, code):
#         system_prompt = """You are a code documentation assistant. Add or improve docstrings for all functions and classes in the given code.
# Ensure clarity and completeness."""
#         prompt = f"code: {code}"
#         return self.query(prompt, system_prompt)

    def run_unit_test_suggestions(self, code):
        system_prompt = """You are a Unit Test Case Suggestion Agent. Your task is to review the provided codebase and suggest relevant unit test cases
        to ensure the code functions correctly and handles edge cases. Make sure you give the code with that respective framework for testing. The languages and their testing frameworks are as follows:

        Python: unittest or pytest
        Java: JUnit
        JavaScript: Jest or Mocha
        C++: Google Test
        HTML/JavaScript (Frontend): Jasmine or Mocha with Chai"""
        prompt = f"code: {code}"
        return self.query(prompt, system_prompt)
    
    def run_final_code_generator(self, quality, bugs, optimizations):
        system_prompt = """You are a senior software engineer. Generate an improved version of the code by incorporating:
    - Code Quality Suggestions
    - Bug Fixes
    - Optimization Suggestions
    The final code should be production-ready. ADD THE OPTIMIZED CODE MANDATORILY DO NOT JUST GIVE SUGGESTIONS."""
        prompt = f"""

        --- Reviews ---
        Quality: {quality}
        Bugs: {bugs}
        optimizations: {optimizations}"""
        return self.query(prompt, system_prompt)

    def run_report_generation(self, quality, bugs, optimizations, tests, final_code, repo_name):
        system_prompt = f"""You are the report generator. Use the analysis results below to create a structured and comprehensive markdown review report for the repository "{repo_name}".

                                Follow these formatting rules **strictly**:
                                - Use `###` for section headings
                                - use '####' for Sub sections do not use '###' for subsections also
                                - Use bullet points (`-`) instead of numbered lists
                                -DO NOT USE NUMBERED LISTS
                                - Use bold for keywords and issues (e.g., **Fix**, **Issue**, **Suggestion**)
                                - Format code blocks using triple backticks and specify the language
                                - Do NOT include HTML tags or numbered lists
                                - Do NOT invent any sections outside the ones provided"""
        prompt = f"""
                        ### Quality Analysis:
                        {quality}

                        ### Bug Detection:
                        {bugs}

                        ### Optimization Suggestions:
                        {optimizations}

                        ### Unit Test Suggestions:
                        {tests}

                        ### Final Optimized Code:
                        {final_code}

                        ### Summary
                        - Code Quality: [Excellent / Good / Needs Improvement]
                        - Bugs: [None / Minor / Major]
                        -Optimizations[None/ Minor/ Major]
                        - Testing: [Well Covered / Needs More Tests / No Tests]

                        ###Conclusion
                        Provide a final recommendation on whether the code is production-ready, needs revisions, or should be refactored.
                        Follow this template given STRICTLY do not add any other sections.
                        """
        return self.query(prompt , system_prompt)
