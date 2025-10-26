"""
Unit tests for persistence layer.
"""

import pytest
import tempfile
import os
from pathlib import Path

from src.strange.persistence import Database
from src.strange.models import Decision, Option, Criteria, Score
from src.strange.repositories import (
    DecisionRepository,
    OptionRepository,
    CriteriaRepository,
    ScoreRepository
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_file.close()
    db = Database(temp_file.name)
    yield db
    db.close()
    os.unlink(temp_file.name)


class TestDatabase:
    """Test cases for the Database class."""
    
    def test_database_creates_default_path(self):
        """Test that database creates default path if none provided."""
        db = Database()
        assert db.db_path is not None
        assert '.strange' in db.db_path
        db.close()
    
    def test_database_creates_custom_path(self, temp_db):
        """Test that database uses custom path when provided."""
        assert temp_db.db_path is not None
        assert os.path.exists(temp_db.db_path)
    
    def test_database_creates_tables(self, temp_db):
        """Test that database creates all required tables."""
        with temp_db.get_cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = [row[0] for row in cursor.fetchall()]
        
        assert 'decisions' in tables
        assert 'options' in tables
        assert 'criteria' in tables
        assert 'scores' in tables
    
    def test_database_creates_indexes(self, temp_db):
        """Test that database creates indexes for performance."""
        with temp_db.get_cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND name NOT LIKE 'sqlite_%'
            """)
            indexes = [row[0] for row in cursor.fetchall()]
        
        assert 'idx_options_decision_id' in indexes
        assert 'idx_criteria_decision_id' in indexes
        assert 'idx_scores_option_id' in indexes
        assert 'idx_scores_criteria_id' in indexes
    
    def test_database_context_manager(self):
        """Test that database can be used as context manager."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        
        with Database(temp_file.name) as db:
            assert db.db_path == temp_file.name
        
        os.unlink(temp_file.name)


class TestDecisionRepository:
    """Test cases for the DecisionRepository class."""
    
    @pytest.fixture
    def decision_repo(self, temp_db):
        """Create a decision repository for testing."""
        return DecisionRepository(temp_db)
    
    def test_create_decision(self, decision_repo):
        """Test creating a decision."""
        decision = Decision(name="Choose a car")
        created = decision_repo.create(decision)
        
        assert created.id == decision.id
        assert created.name == decision.name
    
    def test_get_decision_by_id(self, decision_repo):
        """Test retrieving a decision by ID."""
        decision = Decision(name="Choose a car")
        decision_repo.create(decision)
        
        retrieved = decision_repo.get_by_id(decision.id)
        
        assert retrieved is not None
        assert retrieved.id == decision.id
        assert retrieved.name == decision.name
    
    def test_get_decision_by_id_not_found(self, decision_repo):
        """Test retrieving a non-existent decision."""
        retrieved = decision_repo.get_by_id("non-existent-id")
        assert retrieved is None
    
    def test_get_all_decisions(self, decision_repo):
        """Test retrieving all decisions."""
        decision1 = Decision(name="Choose a car")
        decision2 = Decision(name="Choose a house")
        
        decision_repo.create(decision1)
        decision_repo.create(decision2)
        
        all_decisions = decision_repo.get_all()
        
        assert len(all_decisions) == 2
        assert any(d.name == "Choose a car" for d in all_decisions)
        assert any(d.name == "Choose a house" for d in all_decisions)
    
    def test_update_decision(self, decision_repo):
        """Test updating a decision."""
        decision = Decision(name="Choose a car")
        decision_repo.create(decision)
        
        decision.name = "Choose a new car"
        decision.description = "Need to buy a car"
        updated = decision_repo.update(decision)
        
        retrieved = decision_repo.get_by_id(decision.id)
        assert retrieved.name == "Choose a new car"
        assert retrieved.description == "Need to buy a car"
    
    def test_delete_decision(self, decision_repo):
        """Test deleting a decision."""
        decision = Decision(name="Choose a car")
        decision_repo.create(decision)
        
        deleted = decision_repo.delete(decision.id)
        assert deleted is True
        
        retrieved = decision_repo.get_by_id(decision.id)
        assert retrieved is None
    
    def test_delete_non_existent_decision(self, decision_repo):
        """Test deleting a non-existent decision."""
        deleted = decision_repo.delete("non-existent-id")
        assert deleted is False


class TestOptionRepository:
    """Test cases for the OptionRepository class."""
    
    @pytest.fixture
    def repos(self, temp_db):
        """Create repositories for testing."""
        return {
            'decision': DecisionRepository(temp_db),
            'option': OptionRepository(temp_db)
        }
    
    @pytest.fixture
    def decision(self, repos):
        """Create a decision for testing."""
        decision = Decision(name="Choose a car")
        return repos['decision'].create(decision)
    
    def test_create_option(self, repos, decision):
        """Test creating an option."""
        option = Option(
            decision_id=decision.id,
            name="Toyota Camry"
        )
        created = repos['option'].create(option)
        
        assert created.id == option.id
        assert created.name == option.name
        assert created.decision_id == decision.id
    
    def test_get_option_by_id(self, repos, decision):
        """Test retrieving an option by ID."""
        option = Option(
            decision_id=decision.id,
            name="Toyota Camry"
        )
        repos['option'].create(option)
        
        retrieved = repos['option'].get_by_id(option.id)
        
        assert retrieved is not None
        assert retrieved.id == option.id
        assert retrieved.name == option.name
    
    def test_get_option_by_id_not_found(self, repos):
        """Test retrieving a non-existent option."""
        retrieved = repos['option'].get_by_id("non-existent-id")
        assert retrieved is None
    
    def test_get_options_by_decision_id(self, repos, decision):
        """Test retrieving all options for a decision."""
        option1 = Option(decision_id=decision.id, name="Toyota Camry")
        option2 = Option(decision_id=decision.id, name="Honda Accord")
        
        repos['option'].create(option1)
        repos['option'].create(option2)
        
        options = repos['option'].get_by_decision_id(decision.id)
        
        assert len(options) == 2
        assert any(o.name == "Toyota Camry" for o in options)
        assert any(o.name == "Honda Accord" for o in options)
    
    def test_get_all_options(self, repos, decision):
        """Test retrieving all options."""
        option1 = Option(decision_id=decision.id, name="Toyota Camry")
        option2 = Option(decision_id=decision.id, name="Honda Accord")
        
        repos['option'].create(option1)
        repos['option'].create(option2)
        
        all_options = repos['option'].get_all()
        
        assert len(all_options) == 2
    
    def test_update_option(self, repos, decision):
        """Test updating an option."""
        option = Option(decision_id=decision.id, name="Toyota Camry")
        repos['option'].create(option)
        
        option.name = "Toyota Camry 2025"
        option.description = "Latest model"
        updated = repos['option'].update(option)
        
        retrieved = repos['option'].get_by_id(option.id)
        assert retrieved.name == "Toyota Camry 2025"
        assert retrieved.description == "Latest model"
    
    def test_delete_option(self, repos, decision):
        """Test deleting an option."""
        option = Option(decision_id=decision.id, name="Toyota Camry")
        repos['option'].create(option)
        
        deleted = repos['option'].delete(option.id)
        assert deleted is True
        
        retrieved = repos['option'].get_by_id(option.id)
        assert retrieved is None
    
    def test_delete_non_existent_option(self, repos):
        """Test deleting a non-existent option."""
        deleted = repos['option'].delete("non-existent-id")
        assert deleted is False


class TestCriteriaRepository:
    """Test cases for the CriteriaRepository class."""
    
    @pytest.fixture
    def repos(self, temp_db):
        """Create repositories for testing."""
        return {
            'decision': DecisionRepository(temp_db),
            'criteria': CriteriaRepository(temp_db)
        }
    
    @pytest.fixture
    def decision(self, repos):
        """Create a decision for testing."""
        decision = Decision(name="Choose a car")
        return repos['decision'].create(decision)
    
    def test_create_criteria(self, repos, decision):
        """Test creating a criteria."""
        criteria = Criteria(
            decision_id=decision.id,
            name="Fuel Efficiency",
            weight=0.8
        )
        created = repos['criteria'].create(criteria)
        
        assert created.id == criteria.id
        assert created.name == criteria.name
        assert created.weight == criteria.weight
        assert created.decision_id == decision.id
    
    def test_get_criteria_by_id(self, repos, decision):
        """Test retrieving a criteria by ID."""
        criteria = Criteria(
            decision_id=decision.id,
            name="Fuel Efficiency"
        )
        repos['criteria'].create(criteria)
        
        retrieved = repos['criteria'].get_by_id(criteria.id)
        
        assert retrieved is not None
        assert retrieved.id == criteria.id
        assert retrieved.name == criteria.name
    
    def test_get_criteria_by_id_not_found(self, repos):
        """Test retrieving a non-existent criteria."""
        retrieved = repos['criteria'].get_by_id("non-existent-id")
        assert retrieved is None
    
    def test_get_criteria_by_decision_id(self, repos, decision):
        """Test retrieving all criteria for a decision."""
        criteria1 = Criteria(decision_id=decision.id, name="Fuel Efficiency", weight=0.8)
        criteria2 = Criteria(decision_id=decision.id, name="Safety Rating", weight=0.9)
        
        repos['criteria'].create(criteria1)
        repos['criteria'].create(criteria2)
        
        criteria_list = repos['criteria'].get_by_decision_id(decision.id)
        
        assert len(criteria_list) == 2
        assert any(c.name == "Fuel Efficiency" for c in criteria_list)
        assert any(c.name == "Safety Rating" for c in criteria_list)
    
    def test_get_all_criteria(self, repos, decision):
        """Test retrieving all criteria."""
        criteria1 = Criteria(decision_id=decision.id, name="Fuel Efficiency")
        criteria2 = Criteria(decision_id=decision.id, name="Safety Rating")
        
        repos['criteria'].create(criteria1)
        repos['criteria'].create(criteria2)
        
        all_criteria = repos['criteria'].get_all()
        
        assert len(all_criteria) == 2
    
    def test_update_criteria(self, repos, decision):
        """Test updating a criteria."""
        criteria = Criteria(decision_id=decision.id, name="Fuel Efficiency", weight=0.8)
        repos['criteria'].create(criteria)
        
        criteria.name = "Fuel Economy"
        criteria.weight = 0.9
        criteria.description = "MPG rating"
        updated = repos['criteria'].update(criteria)
        
        retrieved = repos['criteria'].get_by_id(criteria.id)
        assert retrieved.name == "Fuel Economy"
        assert retrieved.weight == 0.9
        assert retrieved.description == "MPG rating"
    
    def test_delete_criteria(self, repos, decision):
        """Test deleting a criteria."""
        criteria = Criteria(decision_id=decision.id, name="Fuel Efficiency")
        repos['criteria'].create(criteria)
        
        deleted = repos['criteria'].delete(criteria.id)
        assert deleted is True
        
        retrieved = repos['criteria'].get_by_id(criteria.id)
        assert retrieved is None
    
    def test_delete_non_existent_criteria(self, repos):
        """Test deleting a non-existent criteria."""
        deleted = repos['criteria'].delete("non-existent-id")
        assert deleted is False


class TestCascadeDelete:
    """Test cascade delete behavior."""
    
    @pytest.fixture
    def repos(self, temp_db):
        """Create all repositories for testing."""
        return {
            'decision': DecisionRepository(temp_db),
            'option': OptionRepository(temp_db),
            'criteria': CriteriaRepository(temp_db)
        }
    
    def test_deleting_decision_cascades_to_options(self, repos):
        """Test that deleting a decision also deletes its options."""
        decision = Decision(name="Choose a car")
        repos['decision'].create(decision)
        
        option = Option(decision_id=decision.id, name="Toyota Camry")
        repos['option'].create(option)
        
        repos['decision'].delete(decision.id)
        
        retrieved_option = repos['option'].get_by_id(option.id)
        assert retrieved_option is None
    
    def test_deleting_decision_cascades_to_criteria(self, repos):
        """Test that deleting a decision also deletes its criteria."""
        decision = Decision(name="Choose a car")
        repos['decision'].create(decision)
        
        criteria = Criteria(decision_id=decision.id, name="Fuel Efficiency")
        repos['criteria'].create(criteria)
        
        repos['decision'].delete(decision.id)
        
        retrieved_criteria = repos['criteria'].get_by_id(criteria.id)
        assert retrieved_criteria is None


class TestScoreRepository:
    """Test cases for the ScoreRepository class."""
    
    @pytest.fixture
    def repos(self, temp_db):
        """Create repositories for testing."""
        return {
            'decision': DecisionRepository(temp_db),
            'option': OptionRepository(temp_db),
            'criteria': CriteriaRepository(temp_db),
            'score': ScoreRepository(temp_db)
        }
    
    @pytest.fixture
    def sample_entities(self, repos):
        """Create sample decision, option, and criteria for testing scores."""
        decision = Decision(name="Choose a car")
        repos['decision'].create(decision)
        
        option = Option(decision_id=decision.id, name="Toyota Camry")
        repos['option'].create(option)
        
        criteria = Criteria(decision_id=decision.id, name="Fuel Efficiency")
        repos['criteria'].create(criteria)
        
        return {
            'decision': decision,
            'option': option,
            'criteria': criteria
        }
    
    def test_create_score(self, repos, sample_entities):
        """Test creating a score."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5,
            notes="Great fuel economy"
        )
        created = repos['score'].create(score)
        
        assert created.id == score.id
        assert created.option_id == score.option_id
        assert created.criteria_id == score.criteria_id
        assert created.value == score.value
        assert created.notes == score.notes
    
    def test_get_score_by_id(self, repos, sample_entities):
        """Test retrieving a score by ID."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        repos['score'].create(score)
        
        retrieved = repos['score'].get_by_id(score.id)
        
        assert retrieved is not None
        assert retrieved.id == score.id
        assert retrieved.value == score.value
    
    def test_get_score_by_id_not_found(self, repos):
        """Test retrieving a non-existent score."""
        retrieved = repos['score'].get_by_id("non-existent-id")
        assert retrieved is None
    
    def test_get_score_by_option_and_criteria(self, repos, sample_entities):
        """Test retrieving a score by option and criteria IDs."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        repos['score'].create(score)
        
        retrieved = repos['score'].get_by_option_and_criteria(
            sample_entities['option'].id,
            sample_entities['criteria'].id
        )
        
        assert retrieved is not None
        assert retrieved.id == score.id
        assert retrieved.value == score.value
    
    def test_get_score_by_option_and_criteria_not_found(self, repos, sample_entities):
        """Test retrieving a non-existent score by option and criteria."""
        retrieved = repos['score'].get_by_option_and_criteria(
            sample_entities['option'].id,
            sample_entities['criteria'].id
        )
        assert retrieved is None
    
    def test_get_scores_by_option_id(self, repos, sample_entities):
        """Test retrieving all scores for an option."""
        decision = sample_entities['decision']
        option = sample_entities['option']
        
        # Create multiple criteria
        criteria1 = Criteria(decision_id=decision.id, name="Fuel Efficiency")
        criteria2 = Criteria(decision_id=decision.id, name="Safety")
        repos['criteria'].create(criteria1)
        repos['criteria'].create(criteria2)
        
        # Create scores for both criteria
        score1 = Score(option_id=option.id, criteria_id=criteria1.id, value=8.5)
        score2 = Score(option_id=option.id, criteria_id=criteria2.id, value=9.0)
        repos['score'].create(score1)
        repos['score'].create(score2)
        
        scores = repos['score'].get_by_option_id(option.id)
        
        assert len(scores) == 2
        assert any(s.criteria_id == criteria1.id for s in scores)
        assert any(s.criteria_id == criteria2.id for s in scores)
    
    def test_get_scores_by_criteria_id(self, repos, sample_entities):
        """Test retrieving all scores for a criteria."""
        decision = sample_entities['decision']
        criteria = sample_entities['criteria']
        
        # Create multiple options
        option1 = Option(decision_id=decision.id, name="Toyota Camry")
        option2 = Option(decision_id=decision.id, name="Honda Accord")
        repos['option'].create(option1)
        repos['option'].create(option2)
        
        # Create scores for both options
        score1 = Score(option_id=option1.id, criteria_id=criteria.id, value=8.5)
        score2 = Score(option_id=option2.id, criteria_id=criteria.id, value=7.8)
        repos['score'].create(score1)
        repos['score'].create(score2)
        
        scores = repos['score'].get_by_criteria_id(criteria.id)
        
        assert len(scores) == 2
        assert any(s.option_id == option1.id for s in scores)
        assert any(s.option_id == option2.id for s in scores)
    
    def test_get_all_scores(self, repos, sample_entities):
        """Test retrieving all scores."""
        decision = sample_entities['decision']
        
        option1 = Option(decision_id=decision.id, name="Toyota Camry")
        option2 = Option(decision_id=decision.id, name="Honda Accord")
        repos['option'].create(option1)
        repos['option'].create(option2)
        
        criteria = Criteria(decision_id=decision.id, name="Fuel Efficiency")
        repos['criteria'].create(criteria)
        
        score1 = Score(option_id=option1.id, criteria_id=criteria.id, value=8.5)
        score2 = Score(option_id=option2.id, criteria_id=criteria.id, value=7.8)
        repos['score'].create(score1)
        repos['score'].create(score2)
        
        all_scores = repos['score'].get_all()
        
        assert len(all_scores) >= 2
        assert any(s.value == 8.5 for s in all_scores)
        assert any(s.value == 7.8 for s in all_scores)
    
    def test_update_score(self, repos, sample_entities):
        """Test updating a score."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5,
            notes="Initial evaluation"
        )
        repos['score'].create(score)
        
        score.value = 9.0
        score.notes = "Updated evaluation"
        updated = repos['score'].update(score)
        
        retrieved = repos['score'].get_by_id(score.id)
        assert retrieved.value == 9.0
        assert retrieved.notes == "Updated evaluation"
    
    def test_delete_score(self, repos, sample_entities):
        """Test deleting a score."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        repos['score'].create(score)
        
        deleted = repos['score'].delete(score.id)
        assert deleted is True
        
        retrieved = repos['score'].get_by_id(score.id)
        assert retrieved is None
    
    def test_delete_score_not_found(self, repos):
        """Test deleting a non-existent score."""
        deleted = repos['score'].delete("non-existent-id")
        assert deleted is False
    
    def test_unique_constraint_option_criteria(self, repos, sample_entities):
        """Test that a unique constraint exists on option_id and criteria_id."""
        import sqlite3
        
        score1 = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        repos['score'].create(score1)
        
        # Try to create another score for the same option-criteria pair
        score2 = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=9.0
        )
        
        with pytest.raises(sqlite3.IntegrityError):
            repos['score'].create(score2)
    
    def test_foreign_key_option_id(self, repos, sample_entities):
        """Test that foreign key constraint exists on option_id."""
        import sqlite3
        
        score = Score(
            option_id="non-existent-option-id",
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        
        with pytest.raises(sqlite3.IntegrityError):
            repos['score'].create(score)
    
    def test_foreign_key_criteria_id(self, repos, sample_entities):
        """Test that foreign key constraint exists on criteria_id."""
        import sqlite3
        
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id="non-existent-criteria-id",
            value=8.5
        )
        
        with pytest.raises(sqlite3.IntegrityError):
            repos['score'].create(score)
    
    def test_cascade_delete_option(self, repos, sample_entities):
        """Test that deleting an option cascades to its scores."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        repos['score'].create(score)
        
        # Delete the option
        repos['option'].delete(sample_entities['option'].id)
        
        # Score should be deleted too
        retrieved_score = repos['score'].get_by_id(score.id)
        assert retrieved_score is None
    
    def test_cascade_delete_criteria(self, repos, sample_entities):
        """Test that deleting a criteria cascades to its scores."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=8.5
        )
        repos['score'].create(score)
        
        # Delete the criteria
        repos['criteria'].delete(sample_entities['criteria'].id)
        
        # Score should be deleted too
        retrieved_score = repos['score'].get_by_id(score.id)
        assert retrieved_score is None
    
    def test_score_with_negative_value(self, repos, sample_entities):
        """Test creating a score with a negative value."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=-5.5
        )
        created = repos['score'].create(score)
        
        assert created.value == -5.5
    
    def test_score_with_zero_value(self, repos, sample_entities):
        """Test creating a score with a zero value."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=0.0
        )
        created = repos['score'].create(score)
        
        assert created.value == 0.0
    
    def test_score_with_large_value(self, repos, sample_entities):
        """Test creating a score with a very large value."""
        score = Score(
            option_id=sample_entities['option'].id,
            criteria_id=sample_entities['criteria'].id,
            value=999999.99
        )
        created = repos['score'].create(score)
        
        assert created.value == 999999.99

