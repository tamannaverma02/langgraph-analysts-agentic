from pydantic import BaseModel, Field
from typing import List

#creating object Analyst 
class Analyst(BaseModel):
    affiliation : str = Field(description="Primary affiliation of the analyst")
    name : str = Field(description="Name of the analyst")
    role : str = Field(description="Role of the analyst in context of the topic")
    description : str = Field(description="Description of the analyst focus, concerns and  motives")

    @property
    def persona(self) -> str:
        return f"Name: {self.name} \n Role: {self.role}\n Affiliation: {self.affiliation}\n Description: {self.description}"


class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(description="Comprehensive list of analysts with their roles and affiliations")

class SearchQuery(BaseModel):
    search_query: str = Field(description="Search query to retrieve relevant documents or information")