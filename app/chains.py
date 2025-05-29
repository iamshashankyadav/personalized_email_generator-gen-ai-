import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

os.getenv("GROQ_API_KEY")
print("Current working directory:", os.getcwd())
class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, user_name, user_role, user_company, user_company_pitch):
        # Set default values manually in Python, not inside the prompt template
        user_name = user_name if user_name else "Anonymous"
        user_role = user_role if user_role else "Aspiring Professional"
        user_company = user_company if user_company else "None"
        user_company_pitch = user_company_pitch if user_company_pitch else "Not Provided"

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### SENDER INFO:
            Name: {user_name}
            Role (if any): {user_role}
            Previous Company or Experience (if any): {user_company}
            Background Summary (optional): {user_company_pitch}

            ### INSTRUCTION:
            You are {user_name}, reaching out with interest in the job described above. 
            You are not representing a company or team — you're looking to personally contribute your skills and grow professionally.
            If you have prior experience or a background summary, mention it concisely.
            Craft a personalized and polite cold email showing genuine interest in the role, your motivation to contribute, and any relevant past work.

            Highlight any suitable work from these personal projects or links: {link_list}
            Avoid any preamble before the email. Write in a sincere, humble, and clear tone — as a person seeking an opportunity.

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links,
            "user_name": user_name,
            "user_role": user_role,
            "user_company": user_company,
            "user_company_pitch": user_company_pitch
        })
        return res.content



if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))