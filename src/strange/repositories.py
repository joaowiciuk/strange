"""
Repository classes for CRUD operations on entities.

This module provides repository pattern implementations for accessing
and manipulating Decision, Option, Criteria, and Score entities.
"""

from typing import List, Optional
from datetime import datetime

from .models import Decision, Option, Criteria, Score
from .persistence import Database


class DecisionRepository:
    """Repository for managing Decision entities."""
    
    def __init__(self, database: Database):
        """
        Initialize the repository.
        
        Args:
            database: Database instance for persistence
        """
        self.db = database
    
    def create(self, decision: Decision) -> Decision:
        """
        Create a new decision in the database.
        
        Args:
            decision: Decision instance to persist
            
        Returns:
            The created decision
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO decisions (id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                decision.id,
                decision.name,
                decision.description,
                decision.created_at.isoformat(),
                decision.updated_at.isoformat()
            ))
        return decision
    
    def get_by_id(self, decision_id: str) -> Optional[Decision]:
        """
        Retrieve a decision by its ID.
        
        Args:
            decision_id: Unique identifier of the decision
            
        Returns:
            Decision instance if found, None otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name, description, created_at, updated_at
                FROM decisions
                WHERE id = ?
            """, (decision_id,))
            row = cursor.fetchone()
            
            if row:
                return Decision(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_all(self) -> List[Decision]:
        """
        Retrieve all decisions from the database.
        
        Returns:
            List of all Decision instances
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name, description, created_at, updated_at
                FROM decisions
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            
            return [
                Decision(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def update(self, decision: Decision) -> Decision:
        """
        Update an existing decision in the database.
        
        Args:
            decision: Decision instance with updated data
            
        Returns:
            The updated decision
        """
        decision.updated_at = datetime.now()
        
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE decisions
                SET name = ?, description = ?, updated_at = ?
                WHERE id = ?
            """, (
                decision.name,
                decision.description,
                decision.updated_at.isoformat(),
                decision.id
            ))
        return decision
    
    def delete(self, decision_id: str) -> bool:
        """
        Delete a decision from the database.
        
        Args:
            decision_id: Unique identifier of the decision to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM decisions WHERE id = ?", (decision_id,))
            return cursor.rowcount > 0


class OptionRepository:
    """Repository for managing Option entities."""
    
    def __init__(self, database: Database):
        """
        Initialize the repository.
        
        Args:
            database: Database instance for persistence
        """
        self.db = database
    
    def create(self, option: Option) -> Option:
        """
        Create a new option in the database.
        
        Args:
            option: Option instance to persist
            
        Returns:
            The created option
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO options (id, decision_id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                option.id,
                option.decision_id,
                option.name,
                option.description,
                option.created_at.isoformat(),
                option.updated_at.isoformat()
            ))
        return option
    
    def get_by_id(self, option_id: str) -> Optional[Option]:
        """
        Retrieve an option by its ID.
        
        Args:
            option_id: Unique identifier of the option
            
        Returns:
            Option instance if found, None otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, decision_id, name, description, created_at, updated_at
                FROM options
                WHERE id = ?
            """, (option_id,))
            row = cursor.fetchone()
            
            if row:
                return Option(
                    id=row['id'],
                    decision_id=row['decision_id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_by_decision_id(self, decision_id: str) -> List[Option]:
        """
        Retrieve all options for a specific decision.
        
        Args:
            decision_id: Unique identifier of the parent decision
            
        Returns:
            List of Option instances for the decision
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, decision_id, name, description, created_at, updated_at
                FROM options
                WHERE decision_id = ?
                ORDER BY created_at ASC
            """, (decision_id,))
            rows = cursor.fetchall()
            
            return [
                Option(
                    id=row['id'],
                    decision_id=row['decision_id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def get_all(self) -> List[Option]:
        """
        Retrieve all options from the database.
        
        Returns:
            List of all Option instances
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, decision_id, name, description, created_at, updated_at
                FROM options
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            
            return [
                Option(
                    id=row['id'],
                    decision_id=row['decision_id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def update(self, option: Option) -> Option:
        """
        Update an existing option in the database.
        
        Args:
            option: Option instance with updated data
            
        Returns:
            The updated option
        """
        option.updated_at = datetime.now()
        
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE options
                SET name = ?, description = ?, updated_at = ?
                WHERE id = ?
            """, (
                option.name,
                option.description,
                option.updated_at.isoformat(),
                option.id
            ))
        return option
    
    def delete(self, option_id: str) -> bool:
        """
        Delete an option from the database.
        
        Args:
            option_id: Unique identifier of the option to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM options WHERE id = ?", (option_id,))
            return cursor.rowcount > 0


class CriteriaRepository:
    """Repository for managing Criteria entities."""
    
    def __init__(self, database: Database):
        """
        Initialize the repository.
        
        Args:
            database: Database instance for persistence
        """
        self.db = database
    
    def create(self, criteria: Criteria) -> Criteria:
        """
        Create a new criteria in the database.
        
        Args:
            criteria: Criteria instance to persist
            
        Returns:
            The created criteria
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO criteria (id, decision_id, name, description, weight, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                criteria.id,
                criteria.decision_id,
                criteria.name,
                criteria.description,
                criteria.weight,
                criteria.created_at.isoformat(),
                criteria.updated_at.isoformat()
            ))
        return criteria
    
    def get_by_id(self, criteria_id: str) -> Optional[Criteria]:
        """
        Retrieve a criteria by its ID.
        
        Args:
            criteria_id: Unique identifier of the criteria
            
        Returns:
            Criteria instance if found, None otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, decision_id, name, description, weight, created_at, updated_at
                FROM criteria
                WHERE id = ?
            """, (criteria_id,))
            row = cursor.fetchone()
            
            if row:
                return Criteria(
                    id=row['id'],
                    decision_id=row['decision_id'],
                    name=row['name'],
                    description=row['description'],
                    weight=row['weight'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_by_decision_id(self, decision_id: str) -> List[Criteria]:
        """
        Retrieve all criteria for a specific decision.
        
        Args:
            decision_id: Unique identifier of the parent decision
            
        Returns:
            List of Criteria instances for the decision
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, decision_id, name, description, weight, created_at, updated_at
                FROM criteria
                WHERE decision_id = ?
                ORDER BY created_at ASC
            """, (decision_id,))
            rows = cursor.fetchall()
            
            return [
                Criteria(
                    id=row['id'],
                    decision_id=row['decision_id'],
                    name=row['name'],
                    description=row['description'],
                    weight=row['weight'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def get_all(self) -> List[Criteria]:
        """
        Retrieve all criteria from the database.
        
        Returns:
            List of all Criteria instances
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, decision_id, name, description, weight, created_at, updated_at
                FROM criteria
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            
            return [
                Criteria(
                    id=row['id'],
                    decision_id=row['decision_id'],
                    name=row['name'],
                    description=row['description'],
                    weight=row['weight'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def update(self, criteria: Criteria) -> Criteria:
        """
        Update an existing criteria in the database.
        
        Args:
            criteria: Criteria instance with updated data
            
        Returns:
            The updated criteria
        """
        criteria.updated_at = datetime.now()
        
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE criteria
                SET name = ?, description = ?, weight = ?, updated_at = ?
                WHERE id = ?
            """, (
                criteria.name,
                criteria.description,
                criteria.weight,
                criteria.updated_at.isoformat(),
                criteria.id
            ))
        return criteria
    
    def delete(self, criteria_id: str) -> bool:
        """
        Delete a criteria from the database.
        
        Args:
            criteria_id: Unique identifier of the criteria to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM criteria WHERE id = ?", (criteria_id,))
            return cursor.rowcount > 0


class ScoreRepository:
    """Repository for managing Score entities."""
    
    def __init__(self, database: Database):
        """
        Initialize the repository.
        
        Args:
            database: Database instance for persistence
        """
        self.db = database
    
    def create(self, score: Score) -> Score:
        """
        Create a new score in the database.
        
        Args:
            score: Score instance to persist
            
        Returns:
            The created score
            
        Raises:
            sqlite3.IntegrityError: If a score for this option-criteria pair already exists
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO scores (id, option_id, criteria_id, value, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                score.id,
                score.option_id,
                score.criteria_id,
                score.value,
                score.notes,
                score.created_at.isoformat(),
                score.updated_at.isoformat()
            ))
        return score
    
    def get_by_id(self, score_id: str) -> Optional[Score]:
        """
        Retrieve a score by its ID.
        
        Args:
            score_id: Unique identifier of the score
            
        Returns:
            Score instance if found, None otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, option_id, criteria_id, value, notes, created_at, updated_at
                FROM scores
                WHERE id = ?
            """, (score_id,))
            row = cursor.fetchone()
            
            if row:
                return Score(
                    id=row['id'],
                    option_id=row['option_id'],
                    criteria_id=row['criteria_id'],
                    value=row['value'],
                    notes=row['notes'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_by_option_and_criteria(self, option_id: str, criteria_id: str) -> Optional[Score]:
        """
        Retrieve a score by its option and criteria IDs.
        
        Args:
            option_id: Unique identifier of the option
            criteria_id: Unique identifier of the criteria
            
        Returns:
            Score instance if found, None otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, option_id, criteria_id, value, notes, created_at, updated_at
                FROM scores
                WHERE option_id = ? AND criteria_id = ?
            """, (option_id, criteria_id))
            row = cursor.fetchone()
            
            if row:
                return Score(
                    id=row['id'],
                    option_id=row['option_id'],
                    criteria_id=row['criteria_id'],
                    value=row['value'],
                    notes=row['notes'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
            return None
    
    def get_by_option_id(self, option_id: str) -> List[Score]:
        """
        Retrieve all scores for a specific option.
        
        Args:
            option_id: Unique identifier of the option
            
        Returns:
            List of Score instances for the option
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, option_id, criteria_id, value, notes, created_at, updated_at
                FROM scores
                WHERE option_id = ?
                ORDER BY created_at ASC
            """, (option_id,))
            rows = cursor.fetchall()
            
            return [
                Score(
                    id=row['id'],
                    option_id=row['option_id'],
                    criteria_id=row['criteria_id'],
                    value=row['value'],
                    notes=row['notes'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def get_by_criteria_id(self, criteria_id: str) -> List[Score]:
        """
        Retrieve all scores for a specific criteria.
        
        Args:
            criteria_id: Unique identifier of the criteria
            
        Returns:
            List of Score instances for the criteria
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, option_id, criteria_id, value, notes, created_at, updated_at
                FROM scores
                WHERE criteria_id = ?
                ORDER BY created_at ASC
            """, (criteria_id,))
            rows = cursor.fetchall()
            
            return [
                Score(
                    id=row['id'],
                    option_id=row['option_id'],
                    criteria_id=row['criteria_id'],
                    value=row['value'],
                    notes=row['notes'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def get_all(self) -> List[Score]:
        """
        Retrieve all scores from the database.
        
        Returns:
            List of all Score instances
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, option_id, criteria_id, value, notes, created_at, updated_at
                FROM scores
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            
            return [
                Score(
                    id=row['id'],
                    option_id=row['option_id'],
                    criteria_id=row['criteria_id'],
                    value=row['value'],
                    notes=row['notes'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in rows
            ]
    
    def update(self, score: Score) -> Score:
        """
        Update an existing score in the database.
        
        Args:
            score: Score instance with updated data
            
        Returns:
            The updated score
        """
        score.updated_at = datetime.now()
        
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE scores
                SET value = ?, notes = ?, updated_at = ?
                WHERE id = ?
            """, (
                score.value,
                score.notes,
                score.updated_at.isoformat(),
                score.id
            ))
        return score
    
    def delete(self, score_id: str) -> bool:
        """
        Delete a score from the database.
        
        Args:
            score_id: Unique identifier of the score to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM scores WHERE id = ?", (score_id,))
            return cursor.rowcount > 0

