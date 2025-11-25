from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, CodeInterpreterTool
from typing import List
from pharma_researcher import schemas
from .tools.FDAAdverseEventsTool import FDAAdverseEventsTool
from .tools.FDADrugsFDATool import FDADrugsFDATool
from .tools.FDAEnforcementTool import FDAEnforcementTool
from .tools.FDANDCTool import FDANDCTool
from .tools.FDAProductLabelTool import FDAProductLabelTool
from .tools.ClinicalTrialsTool import ClinicalTrialsTool
from .tools.NCBIEntrezTool import NCBIEntrezTool
from .tools.EMAMedicinesTool import EMAMedicinesTool
from .tools.EMAMedicineShortagesTool import EMAMedicineShortagesTool
from .tools.PatentsViewTool import PatentsViewTool
from .tools.EXIMTool import EXIMTool
from .tools.ChEMBLTool import ChEMBLTool
from .tools.OpenTargetsTool import OpenTargetsTool
from .tools.OpenTargetsDrugIndicationTool import OpenTargetsDrugIndicationTool


@CrewBase
class PharmaResearcher():
    """PharmaResearcher crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ---- AGENTS ----

    @agent
    def market_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['market_insights_agent'], 
            verbose = True, 
            tools=[SerperDevTool(), FDAAdverseEventsTool(), FDADrugsFDATool(), FDAEnforcementTool(), FDANDCTool(), FDAProductLabelTool(), EMAMedicinesTool(), EMAMedicineShortagesTool()])
    
    @agent
    def exim_trends_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['exim_trends_agent'], 
            verbose = True, 
            tools=[EXIMTool(), SerperDevTool()])
    
    @agent
    def patent_landscape_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['patent_landscape_agent'], 
            verbose = True, 
            tools=[PatentsViewTool(), SerperDevTool()])
    
    @agent
    def clinical_trials_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['clinical_trials_agent'], 
            verbose = True, 
            tools=[ClinicalTrialsTool(), SerperDevTool()])
    
    @agent
    def web_intelligence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['web_intelligence_agent'], 
            verbose = True, 
            tools=[SerperDevTool(), NCBIEntrezTool()])
    
    @agent
    def chembl_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chembl_insights_agent'],
            verbose=True,
            tools=[ChEMBLTool(), SerperDevTool()])
    
    @agent
    def open_targets_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['open_targets_research_agent'],
            verbose=True,
            tools=[OpenTargetsTool(), SerperDevTool()])
    
    @agent
    def open_targets_drug_indication_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['open_targets_drug_indication_agent'],
            verbose=True,
            tools=[OpenTargetsDrugIndicationTool(), SerperDevTool()])
    
    @agent
    def report_title_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_title_generator_agent'],
            verbose=True)
    
    @agent
    def report_abstract_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_abstract_generator_agent'],
            verbose=True)
    
    @agent
    def report_body_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_body_writer_agent'],
            verbose=True)
    
    @agent
    def visualization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['visualization_agent'],
            verbose=True)
    
    @agent
    def report_generation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generation_agent'],
            verbose = True)
    

    # ---- TASKS ----

    @task
    def market_insights_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_insights_task'], # type: ignore[index]
        )
    
    @task
    def exim_trade_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['exim_trade_analysis_task'], # type: ignore[index]
        )
    
    @task
    def patent_landscape_task(self) -> Task:
        return Task(
            config=self.tasks_config['patent_landscape_task'], # type: ignore[index]
        )
    
    @task
    def clinical_trials_pipeline_task(self) -> Task:
        return Task(
            config=self.tasks_config['clinical_trials_pipeline_task'], # type: ignore[index]
        )
    
    @task
    def web_intelligence_scan_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_intelligence_scan_task'], # type: ignore[index]
        )
    
    @task
    def chembl_insights_task(self) -> Task:
        return Task(
            config=self.tasks_config['chembl_insights_task'] # type: ignore[index]
        )
    
    @task
    def open_targets_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['open_targets_research_task'] # type: ignore[index]
        )
    
    @task
    def open_targets_drug_indication_task(self) -> Task:
        return Task(
            config=self.tasks_config['open_targets_drug_indication_task'] # type: ignore[index]
        )
    
    @task
    def generate_report_title_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_title_task'] # type: ignore[index]
        )
    
    @task
    def generate_report_abstract_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_abstract_task'] # type: ignore[index]
        )
    
    @task
    def generate_report_body_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report_body_task'] # type: ignore[index]
        )
    
    @task
    def generate_visualizations_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_visualizations_task'] # type: ignore[index]
        )
    
    @task
    def generate_final_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_final_report_task'], # type: ignore[index]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the PharmaResearcher crew"""
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            max_retry_limit=2,  # Prevent infinite retry loops
            verbose=True
        )
