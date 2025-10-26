"""
Service layer for managing decision-making operations.
"""

from typing import Optional, List, Dict, Any
from .models import Decision, Option, Criteria, Score
from .repositories import OptionRepository, CriteriaRepository, ScoreRepository


class DecisionService:
    """Service for managing CRUD operations on Options, Criteria, and Scores."""
    
    def __init__(
        self,
        decision: Decision,
        option_repository: OptionRepository,
        criteria_repository: CriteriaRepository,
        score_repository: ScoreRepository
    ):
        if decision is None:
            raise ValueError("Decision cannot be None")
        
        self.decision = decision
        self.option_repository = option_repository
        self.criteria_repository = criteria_repository
        self.score_repository = score_repository
    
    def create_option(self, name: str, description: str = "") -> Option:
        if not name or not name.strip():
            raise ValueError("Option name cannot be empty")
        
        option = Option(
            decision_id=self.decision.id,
            name=name,
            description=description
        )
        return self.option_repository.create(option)
    
    def get_option(self, option_id: str) -> Optional[Option]:
        return self.option_repository.get_by_id(option_id)
    
    def get_all_options(self) -> List[Option]:
        return self.option_repository.get_by_decision_id(self.decision.id)
    
    def update_option(
        self,
        option_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Option:
        option = self.option_repository.get_by_id(option_id)
        if option is None:
            raise ValueError(f"Option with id {option_id} not found")
        
        if name is not None:
            option.name = name
        if description is not None:
            option.description = description
        
        return self.option_repository.update(option)
    
    def delete_option(self, option_id: str) -> bool:
        return self.option_repository.delete(option_id)
    
    def create_criteria(
        self,
        name: str,
        description: str = "",
        weight: float = 1.0
    ) -> Criteria:
        if not name or not name.strip():
            raise ValueError("Criteria name cannot be empty")
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        
        criteria = Criteria(
            decision_id=self.decision.id,
            name=name,
            description=description,
            weight=weight
        )
        return self.criteria_repository.create(criteria)
    
    def get_criteria(self, criteria_id: str) -> Optional[Criteria]:
        return self.criteria_repository.get_by_id(criteria_id)
    
    def get_all_criteria(self) -> List[Criteria]:
        return self.criteria_repository.get_by_decision_id(self.decision.id)
    
    def update_criteria(
        self,
        criteria_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        weight: Optional[float] = None
    ) -> Criteria:
        criteria = self.criteria_repository.get_by_id(criteria_id)
        if criteria is None:
            raise ValueError(f"Criteria with id {criteria_id} not found")
        
        if name is not None:
            criteria.name = name
        if description is not None:
            criteria.description = description
        if weight is not None:
            criteria.weight = weight
        
        return self.criteria_repository.update(criteria)
    
    def delete_criteria(self, criteria_id: str) -> bool:
        return self.criteria_repository.delete(criteria_id)
    
    def create_score(
        self,
        option_id: str,
        criteria_id: str,
        value: float,
        notes: str = ""
    ) -> Score:
        if not option_id or not option_id.strip():
            raise ValueError("Option ID cannot be empty")
        if not criteria_id or not criteria_id.strip():
            raise ValueError("Criteria ID cannot be empty")
        if not isinstance(value, (int, float)):
            raise ValueError("Score value must be numeric")
        
        score = Score(
            option_id=option_id,
            criteria_id=criteria_id,
            value=float(value),
            notes=notes
        )
        return self.score_repository.create(score)
    
    def get_score(self, score_id: str) -> Optional[Score]:
        return self.score_repository.get_by_id(score_id)
    
    def get_score_by_option_and_criteria(
        self,
        option_id: str,
        criteria_id: str
    ) -> Optional[Score]:
        return self.score_repository.get_by_option_and_criteria(option_id, criteria_id)
    
    def get_scores_by_option(self, option_id: str) -> List[Score]:
        return self.score_repository.get_by_option_id(option_id)
    
    def get_scores_by_criteria(self, criteria_id: str) -> List[Score]:
        return self.score_repository.get_by_criteria_id(criteria_id)
    
    def update_score(
        self,
        score_id: str,
        value: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Score:
        score = self.score_repository.get_by_id(score_id)
        if score is None:
            raise ValueError(f"Score with id {score_id} not found")
        
        if value is not None:
            score.value = value
        if notes is not None:
            score.notes = notes
        
        return self.score_repository.update(score)
    
    def delete_score(self, score_id: str) -> bool:
        return self.score_repository.delete(score_id)
    
    def calculate_weighted_scores(self) -> List[Dict[str, Any]]:
        """
        Calculate weighted scores for all options in the decision.
        
        Returns a list of dictionaries, each containing:
        - 'option': The Option object
        - 'weighted_score': The calculated weighted score (sum of score * weight for all criteria)
        
        The list is sorted in descending order by weighted_score.
        Missing scores are treated as 0.0.
        """
        options = self.option_repository.get_by_decision_id(self.decision.id)
        if not options:
            return []
        
        criteria = self.criteria_repository.get_by_decision_id(self.decision.id)
        criteria_weights = {c.id: c.weight for c in criteria}
        
        results = []
        for option in options:
            weighted_score = 0.0
            
            if not criteria_weights:
                results.append({'option': option, 'weighted_score': weighted_score})
                continue
            
            scores = self.score_repository.get_by_option_id(option.id)
            score_values = {s.criteria_id: s.value for s in scores}
            
            for criteria_id, weight in criteria_weights.items():
                score_value = score_values.get(criteria_id, 0.0)
                weighted_score += score_value * weight
            
            results.append({'option': option, 'weighted_score': weighted_score})
        
        results.sort(key=lambda x: x['weighted_score'], reverse=True)
        return results

