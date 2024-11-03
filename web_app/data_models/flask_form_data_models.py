import re
from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError, field_validator
from typing import Optional, List, Dict, Sequence
from datetime import datetime

class CommonFunctionality:
    '''
    Common validators
    '''
    def __init__(self, v):
        self.v = v

    def if_none(self):
        if self.v == '' or self.v is None:
            return None
        return self.v

    def convert_to_list(self: str) -> list:
        '''
        Converts new line strings to list
        '''
        if isinstance(self.v, list):
            return self.v
        if isinstance(self.v, str):
            return [line.strip() for line in self.v.splitlines() if self.v]
        return []

class UserDataModel(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None

    @field_validator('linkedin', 'github', mode='before')
    def validate_urls(cls, v):
        return CommonFunctionality(v=v).if_none()

    @field_validator('phone_number', mode='before')
    def validate_phone(cls, v):
        # Check for letters in the input
        if re.search(r'[A-Za-z]', v):
            raise ValueError("Phone number must not contain letters.")

        cleaned_number = re.sub(r'\D', '', v)
        if not (7 <= len(cleaned_number) <= 12):
            raise ValueError("Phone number must be between 7 and 12 digits.")

        # Normalize to the desired format (e.g., 123-456-7891)
        if len(cleaned_number) == 10:
            return f"{cleaned_number[:3]}-{cleaned_number[3:6]}-{cleaned_number[6:]}"
        elif len(cleaned_number) == 7:
            return f"{cleaned_number[:3]}-{cleaned_number[3:]}"
        elif len(cleaned_number) == 11 and cleaned_number.startswith('1'):
            # For numbers like +1XXXXXXXXXX or 11234567891, return in standard format
            return f"{cleaned_number[1:4]}-{cleaned_number[4:7]}-{cleaned_number[7:]}"

        # If none of the formats matched, raise an error
        raise ValueError("Invalid phone number format.")


class EducationDataModel(BaseModel):
    university: Optional[str] = None
    location: Optional[str] = None
    degree: Optional[str] = None
    university_start_date: Optional[datetime] = None
    university_end_date: Optional[datetime] = None

    @field_validator('university_start_date', 'university_end_date', mode='before')
    def validate_dates(cls, v: datetime):
        return CommonFunctionality(v=v).if_none()

class ExperienceDataModel(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    job_functions: Optional[List[str]] = None

    @field_validator('job_functions', mode='before')
    def validate_job_functions(cls, v):
        return CommonFunctionality(v=v).convert_to_list()

class ProjectDataModel(BaseModel):
    project_name: Optional[str] = None
    github_repo_link: Optional[HttpUrl] = None
    skills_learned: Optional[List[str]] = None
    project_functions: Optional[List[str]] = None

    @field_validator('skills_learned', 'project_functions', mode='before')
    def validate_skills_learned_and_project_functions(cls, v):
        return CommonFunctionality(v=v).convert_to_list()
    @field_validator('github_repo_link', mode='before')
    def validate_github_repo_url(cls, v):
        return CommonFunctionality(v=v).if_none()

class SkillsDataModel(BaseModel):
    skills_list: Optional[List[str]] = None

    @field_validator('skills_list', mode='before')
    def validate_skills(cls, v):
        return CommonFunctionality(v=v).convert_to_list()

class CertsDataModel(BaseModel):
    certs_list: Optional[List[str]] = None

    @field_validator('certs_list', mode='before')
    def validate_certs(cls, v):
        return CommonFunctionality(v=v).convert_to_list()

class AiOptionsModel(BaseModel):
    add_summary: bool
    edit_attributes: bool
    job_desc: Optional[str]

class CompiledPayload(BaseModel):
    summary: Optional[str] = None
    user_data: UserDataModel
    education_data: Optional[List[EducationDataModel]] = None
    experience_data: Optional[List[ExperienceDataModel]] = None
    projects_data: Optional[List[ProjectDataModel]] = None
    skills_data: Optional[SkillsDataModel] = None
    certs_data: Optional[CertsDataModel] = None
