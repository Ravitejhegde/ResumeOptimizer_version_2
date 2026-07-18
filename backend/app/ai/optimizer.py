from .parser import ResumeParser
from .section_optimizer import SectionOptimizer


class ResumeOptimizer:

    def __init__(self):
        self.parser = ResumeParser()
        self.section_optimizer = SectionOptimizer()

    def optimize(self, resume_path: str, job_description: str):

        parsed_resume = self.parser.parse(resume_path)

        optimized_sections = []

        for section in parsed_resume.sections:

            prompt = self.section_optimizer.get_prompt(
                section.title
            )

            optimized_sections.append(
                {
                    "title": section.title,
                    "original": section.content,
                    "prompt": prompt,
                    "job_description": job_description,
                }
            )

        return optimized_sections