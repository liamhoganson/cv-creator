from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, List, Dict
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
    phone_number: PhoneNumber
    email: EmailStr
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None

    @field_validator('linkedin', 'github', mode='before')
    def validate_urls(cls, v):
        return CommonFunctionality(v=v).if_none()

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

class CompiledPayload(BaseModel):
    user_data: UserDataModel
    education_data: Optional[List[EducationDataModel]] = None
    experience_data: Optional[List[ExperienceDataModel]] = None
    projects_data: Optional[List[ProjectDataModel]] = None
    skills_data: Optional[SkillsDataModel] = None
    certs_data: Optional[CertsDataModel] = None
    ai_options_data: AiOptionsModel
