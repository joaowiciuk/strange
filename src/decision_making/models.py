"""
Data models for the decision-making tool.

This module defines the core entities for decision-making:
- Decision: The root entity representing a decision to be made
- Option: Alternative choices for a decision
- Criteria: Factors to evaluate options against
- Score: Bridge model associating options with criteria and their scores
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4


@dataclass
class Decision:
    """
    Root entity representing a decision to be made.
    
    Attributes:
        id: Unique identifier for the decision
        name: Name/title of the decision
        description: Detailed description of the decision
        created_at: Timestamp when the decision was created
        updated_at: Timestamp when the decision was last updated
        options: List of options associated with this decision
        criteria: List of criteria to evaluate options
    """
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate the decision data."""
        if not self.name or not self.name.strip():
            raise ValueError("Decision name cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert the decision to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Decision':
        """Create a Decision instance from a dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )


@dataclass
class Option:
    """
    Represents an alternative choice for a decision.
    
    Attributes:
        id: Unique identifier for the option
        decision_id: Foreign key to the parent decision
        name: Name of the option
        description: Detailed description of the option
        created_at: Timestamp when the option was created
        updated_at: Timestamp when the option was last updated
    """
    decision_id: str
    name: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate the option data."""
        if not self.name or not self.name.strip():
            raise ValueError("Option name cannot be empty")
        if not self.decision_id or not self.decision_id.strip():
            raise ValueError("Option must be associated with a decision")
    
    def to_dict(self) -> dict:
        """Convert the option to a dictionary."""
        return {
            'id': self.id,
            'decision_id': self.decision_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Option':
        """Create an Option instance from a dictionary."""
        return cls(
            id=data['id'],
            decision_id=data['decision_id'],
            name=data['name'],
            description=data.get('description', ''),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )


@dataclass
class Criteria:
    """
    Represents a factor to evaluate options against.
    
    Attributes:
        id: Unique identifier for the criteria
        decision_id: Foreign key to the parent decision
        name: Name of the criteria
        description: Detailed description of the criteria
        weight: Importance weight of this criteria (0.0 to 1.0)
        created_at: Timestamp when the criteria was created
        updated_at: Timestamp when the criteria was last updated
    """
    decision_id: str
    name: str
    weight: float = 1.0
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate the criteria data."""
        if not self.name or not self.name.strip():
            raise ValueError("Criteria name cannot be empty")
        if not self.decision_id or not self.decision_id.strip():
            raise ValueError("Criteria must be associated with a decision")
        if not isinstance(self.weight, (int, float)):
            raise ValueError("Weight must be a numeric value")
        if self.weight < 0:
            raise ValueError("Weight cannot be negative")
    
    def to_dict(self) -> dict:
        """Convert the criteria to a dictionary."""
        return {
            'id': self.id,
            'decision_id': self.decision_id,
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Criteria':
        """Create a Criteria instance from a dictionary."""
        return cls(
            id=data['id'],
            decision_id=data['decision_id'],
            name=data['name'],
            description=data.get('description', ''),
            weight=data.get('weight', 1.0),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )


@dataclass
class Score:
    """
    Bridge model associating an Option with a Criteria and assigning a score.
    
    This model represents the evaluation of a specific option against a specific
    criteria, capturing how well the option performs on that criteria.
    
    Attributes:
        id: Unique identifier for the score
        option_id: Foreign key to the option being scored
        criteria_id: Foreign key to the criteria being evaluated against
        value: The numeric score value (real number)
        notes: Optional notes or justification for the score
        created_at: Timestamp when the score was created
        updated_at: Timestamp when the score was last updated
    """
    option_id: str
    criteria_id: str
    value: float
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate the score data."""
        if not self.option_id or not self.option_id.strip():
            raise ValueError("Score must be associated with an option")
        if not self.criteria_id or not self.criteria_id.strip():
            raise ValueError("Score must be associated with a criteria")
        if not isinstance(self.value, (int, float)):
            raise ValueError("Score value must be a numeric value")
        # Convert int to float for consistency
        if isinstance(self.value, int):
            self.value = float(self.value)
    
    def to_dict(self) -> dict:
        """Convert the score to a dictionary."""
        return {
            'id': self.id,
            'option_id': self.option_id,
            'criteria_id': self.criteria_id,
            'value': self.value,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Score':
        """Create a Score instance from a dictionary."""
        return cls(
            id=data['id'],
            option_id=data['option_id'],
            criteria_id=data['criteria_id'],
            value=data['value'],
            notes=data.get('notes', ''),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )

