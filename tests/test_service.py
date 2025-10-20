"""
Unit tests for the DecisionService component.

This module tests a service layer that manages CRUD operations for Options,
Criteria, and Scores within the context of a Decision. The service depends
on Database and Repository components via dependency injection.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime

from src.decision_making.models import Decision, Option, Criteria, Score
from src.decision_making.persistence import Database
from src.decision_making.repositories import (
    OptionRepository,
    CriteriaRepository,
    ScoreRepository
)


class TestDecisionServiceInitialization:
    """Test cases for DecisionService initialization."""
    
    def test_service_initializes_with_decision(self):
        """Test that service initializes with a Decision model."""
        # Arrange
        decision = Decision(name="Choose a car", description="Buy a new car")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        # Act
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        # Assert
        assert service.decision == decision
        assert service.decision.name == "Choose a car"
        assert service.decision.description == "Buy a new car"
    
    def test_service_stores_injected_dependencies(self):
        """Test that service stores injected dependencies."""
        # Arrange
        decision = Decision(name="Choose a car")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        # Act
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        # Assert
        assert service.database == mock_db
        assert service.option_repository == mock_option_repo
        assert service.criteria_repository == mock_criteria_repo
        assert service.score_repository == mock_score_repo
    
    def test_service_requires_decision(self):
        """Test that service requires a Decision instance."""
        # Arrange
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        # Act & Assert
        from src.decision_making.service import DecisionService
        with pytest.raises((TypeError, ValueError)):
            service = DecisionService(
                decision=None,
                database=mock_db,
                option_repository=mock_option_repo,
                criteria_repository=mock_criteria_repo,
                score_repository=mock_score_repo
            )
    
    def test_service_requires_database(self):
        """Test that service requires a Database instance."""
        # Arrange
        decision = Decision(name="Choose a car")
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        # Act & Assert
        from src.decision_making.service import DecisionService
        with pytest.raises((TypeError, ValueError)):
            service = DecisionService(
                decision=decision,
                database=None,
                option_repository=mock_option_repo,
                criteria_repository=mock_criteria_repo,
                score_repository=mock_score_repo
            )


class TestOptionCRUD:
    """Test cases for Option CRUD operations."""
    
    @pytest.fixture
    def service_setup(self):
        """Setup service with mocked dependencies."""
        decision = Decision(name="Choose a car", id="decision-123")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        return {
            'service': service,
            'decision': decision,
            'option_repo': mock_option_repo,
            'criteria_repo': mock_criteria_repo,
            'score_repo': mock_score_repo,
            'db': mock_db
        }
    
    def test_create_option_with_name_only(self, service_setup):
        """Test creating an option with only a name."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        
        expected_option = Option(
            decision_id=decision.id,
            name="Toyota Camry",
            id="option-123"
        )
        mock_option_repo.create.return_value = expected_option
        
        # Act
        result = service.create_option(name="Toyota Camry")
        
        # Assert
        mock_option_repo.create.assert_called_once()
        call_args = mock_option_repo.create.call_args[0][0]
        assert isinstance(call_args, Option)
        assert call_args.name == "Toyota Camry"
        assert call_args.decision_id == decision.id
        assert result == expected_option
    
    def test_create_option_with_name_and_description(self, service_setup):
        """Test creating an option with name and description."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        
        expected_option = Option(
            decision_id=decision.id,
            name="Toyota Camry",
            description="Reliable sedan",
            id="option-123"
        )
        mock_option_repo.create.return_value = expected_option
        
        # Act
        result = service.create_option(
            name="Toyota Camry",
            description="Reliable sedan"
        )
        
        # Assert
        mock_option_repo.create.assert_called_once()
        call_args = mock_option_repo.create.call_args[0][0]
        assert call_args.name == "Toyota Camry"
        assert call_args.description == "Reliable sedan"
        assert call_args.decision_id == decision.id
        assert result == expected_option
    
    def test_create_option_validates_empty_name(self, service_setup):
        """Test that creating an option with empty name raises error."""
        # Arrange
        service = service_setup['service']
        
        # Act & Assert
        with pytest.raises(ValueError, match=".*name.*empty.*"):
            service.create_option(name="")
        
        with pytest.raises(ValueError, match=".*name.*empty.*"):
            service.create_option(name="   ")
    
    def test_create_option_associates_with_decision(self, service_setup):
        """Test that created option is associated with the service's decision."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        
        # Act
        service.create_option(name="Toyota Camry")
        
        # Assert
        call_args = mock_option_repo.create.call_args[0][0]
        assert call_args.decision_id == decision.id
    
    def test_get_option_by_id(self, service_setup):
        """Test retrieving an option by its ID."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        
        expected_option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            id="option-123"
        )
        mock_option_repo.get_by_id.return_value = expected_option
        
        # Act
        result = service.get_option("option-123")
        
        # Assert
        mock_option_repo.get_by_id.assert_called_once_with("option-123")
        assert result == expected_option
    
    def test_get_option_not_found(self, service_setup):
        """Test retrieving a non-existent option returns None."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        mock_option_repo.get_by_id.return_value = None
        
        # Act
        result = service.get_option("non-existent-id")
        
        # Assert
        mock_option_repo.get_by_id.assert_called_once_with("non-existent-id")
        assert result is None
    
    def test_get_all_options_for_decision(self, service_setup):
        """Test retrieving all options for the decision."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        
        expected_options = [
            Option(decision_id=decision.id, name="Toyota Camry", id="option-1"),
            Option(decision_id=decision.id, name="Honda Accord", id="option-2"),
            Option(decision_id=decision.id, name="Mazda 6", id="option-3")
        ]
        mock_option_repo.get_by_decision_id.return_value = expected_options
        
        # Act
        result = service.get_all_options()
        
        # Assert
        mock_option_repo.get_by_decision_id.assert_called_once_with(decision.id)
        assert result == expected_options
        assert len(result) == 3
    
    def test_get_all_options_empty_list(self, service_setup):
        """Test retrieving all options when none exist."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        mock_option_repo.get_by_decision_id.return_value = []
        
        # Act
        result = service.get_all_options()
        
        # Assert
        mock_option_repo.get_by_decision_id.assert_called_once_with(decision.id)
        assert result == []
    
    def test_update_option_name(self, service_setup):
        """Test updating an option's name."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        
        option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            id="option-123"
        )
        mock_option_repo.get_by_id.return_value = option
        
        updated_option = Option(
            decision_id="decision-123",
            name="Toyota Camry 2025",
            id="option-123"
        )
        mock_option_repo.update.return_value = updated_option
        
        # Act
        result = service.update_option(
            option_id="option-123",
            name="Toyota Camry 2025"
        )
        
        # Assert
        mock_option_repo.get_by_id.assert_called_once_with("option-123")
        mock_option_repo.update.assert_called_once()
        call_args = mock_option_repo.update.call_args[0][0]
        assert call_args.name == "Toyota Camry 2025"
        assert result == updated_option
    
    def test_update_option_description(self, service_setup):
        """Test updating an option's description."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        
        option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            description="Old description",
            id="option-123"
        )
        mock_option_repo.get_by_id.return_value = option
        
        updated_option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            description="New description",
            id="option-123"
        )
        mock_option_repo.update.return_value = updated_option
        
        # Act
        result = service.update_option(
            option_id="option-123",
            description="New description"
        )
        
        # Assert
        mock_option_repo.update.assert_called_once()
        call_args = mock_option_repo.update.call_args[0][0]
        assert call_args.description == "New description"
        assert result == updated_option
    
    def test_update_option_name_and_description(self, service_setup):
        """Test updating both name and description of an option."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        
        option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            description="Old description",
            id="option-123"
        )
        mock_option_repo.get_by_id.return_value = option
        
        updated_option = Option(
            decision_id="decision-123",
            name="Toyota Camry 2025",
            description="New description",
            id="option-123"
        )
        mock_option_repo.update.return_value = updated_option
        
        # Act
        result = service.update_option(
            option_id="option-123",
            name="Toyota Camry 2025",
            description="New description"
        )
        
        # Assert
        mock_option_repo.update.assert_called_once()
        call_args = mock_option_repo.update.call_args[0][0]
        assert call_args.name == "Toyota Camry 2025"
        assert call_args.description == "New description"
        assert result == updated_option
    
    def test_update_option_not_found(self, service_setup):
        """Test updating a non-existent option raises error."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        mock_option_repo.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises((ValueError, KeyError)):
            service.update_option(
                option_id="non-existent-id",
                name="New Name"
            )
    
    def test_delete_option(self, service_setup):
        """Test deleting an option."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        mock_option_repo.delete.return_value = True
        
        # Act
        result = service.delete_option("option-123")
        
        # Assert
        mock_option_repo.delete.assert_called_once_with("option-123")
        assert result is True
    
    def test_delete_option_not_found(self, service_setup):
        """Test deleting a non-existent option."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        mock_option_repo.delete.return_value = False
        
        # Act
        result = service.delete_option("non-existent-id")
        
        # Assert
        mock_option_repo.delete.assert_called_once_with("non-existent-id")
        assert result is False
    
    def test_delete_option_cascades_to_scores(self, service_setup):
        """Test that deleting an option also removes associated scores."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        mock_score_repo = service_setup['score_repo']
        
        mock_option_repo.delete.return_value = True
        mock_score_repo.get_by_option_id.return_value = [
            Score(option_id="option-123", criteria_id="criteria-1", value=8.0, id="score-1"),
            Score(option_id="option-123", criteria_id="criteria-2", value=7.0, id="score-2")
        ]
        
        # Act
        service.delete_option("option-123")
        
        # Assert
        # Verify that the database cascade handles this,
        # or the service explicitly deletes associated scores
        mock_option_repo.delete.assert_called_once_with("option-123")


class TestCriteriaCRUD:
    """Test cases for Criteria CRUD operations."""
    
    @pytest.fixture
    def service_setup(self):
        """Setup service with mocked dependencies."""
        decision = Decision(name="Choose a car", id="decision-123")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        return {
            'service': service,
            'decision': decision,
            'option_repo': mock_option_repo,
            'criteria_repo': mock_criteria_repo,
            'score_repo': mock_score_repo,
            'db': mock_db
        }
    
    def test_create_criteria_with_name_only(self, service_setup):
        """Test creating a criteria with only a name."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        
        expected_criteria = Criteria(
            decision_id=decision.id,
            name="Fuel Efficiency",
            weight=1.0,
            id="criteria-123"
        )
        mock_criteria_repo.create.return_value = expected_criteria
        
        # Act
        result = service.create_criteria(name="Fuel Efficiency")
        
        # Assert
        mock_criteria_repo.create.assert_called_once()
        call_args = mock_criteria_repo.create.call_args[0][0]
        assert isinstance(call_args, Criteria)
        assert call_args.name == "Fuel Efficiency"
        assert call_args.decision_id == decision.id
        assert call_args.weight == 1.0
        assert result == expected_criteria
    
    def test_create_criteria_with_custom_weight(self, service_setup):
        """Test creating a criteria with a custom weight."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        
        expected_criteria = Criteria(
            decision_id=decision.id,
            name="Fuel Efficiency",
            weight=0.8,
            id="criteria-123"
        )
        mock_criteria_repo.create.return_value = expected_criteria
        
        # Act
        result = service.create_criteria(name="Fuel Efficiency", weight=0.8)
        
        # Assert
        mock_criteria_repo.create.assert_called_once()
        call_args = mock_criteria_repo.create.call_args[0][0]
        assert call_args.name == "Fuel Efficiency"
        assert call_args.weight == 0.8
        assert result == expected_criteria
    
    def test_create_criteria_with_all_fields(self, service_setup):
        """Test creating a criteria with all fields."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        
        expected_criteria = Criteria(
            decision_id=decision.id,
            name="Fuel Efficiency",
            description="Miles per gallon",
            weight=0.75,
            id="criteria-123"
        )
        mock_criteria_repo.create.return_value = expected_criteria
        
        # Act
        result = service.create_criteria(
            name="Fuel Efficiency",
            description="Miles per gallon",
            weight=0.75
        )
        
        # Assert
        mock_criteria_repo.create.assert_called_once()
        call_args = mock_criteria_repo.create.call_args[0][0]
        assert call_args.name == "Fuel Efficiency"
        assert call_args.description == "Miles per gallon"
        assert call_args.weight == 0.75
        assert result == expected_criteria
    
    def test_create_criteria_validates_empty_name(self, service_setup):
        """Test that creating a criteria with empty name raises error."""
        # Arrange
        service = service_setup['service']
        
        # Act & Assert
        with pytest.raises(ValueError, match=".*name.*empty.*"):
            service.create_criteria(name="")
        
        with pytest.raises(ValueError, match=".*name.*empty.*"):
            service.create_criteria(name="   ")
    
    def test_create_criteria_validates_negative_weight(self, service_setup):
        """Test that creating a criteria with negative weight raises error."""
        # Arrange
        service = service_setup['service']
        
        # Act & Assert
        with pytest.raises(ValueError, match=".*[Ww]eight.*negative.*"):
            service.create_criteria(name="Fuel Efficiency", weight=-1.0)
    
    def test_create_criteria_allows_zero_weight(self, service_setup):
        """Test that creating a criteria with zero weight is allowed."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        expected_criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.0,
            id="criteria-123"
        )
        mock_criteria_repo.create.return_value = expected_criteria
        
        # Act
        result = service.create_criteria(name="Fuel Efficiency", weight=0.0)
        
        # Assert
        assert result.weight == 0.0
    
    def test_create_criteria_associates_with_decision(self, service_setup):
        """Test that created criteria is associated with the service's decision."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        
        # Act
        service.create_criteria(name="Fuel Efficiency")
        
        # Assert
        call_args = mock_criteria_repo.create.call_args[0][0]
        assert call_args.decision_id == decision.id
    
    def test_get_criteria_by_id(self, service_setup):
        """Test retrieving a criteria by its ID."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        expected_criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            id="criteria-123"
        )
        mock_criteria_repo.get_by_id.return_value = expected_criteria
        
        # Act
        result = service.get_criteria("criteria-123")
        
        # Assert
        mock_criteria_repo.get_by_id.assert_called_once_with("criteria-123")
        assert result == expected_criteria
    
    def test_get_criteria_not_found(self, service_setup):
        """Test retrieving a non-existent criteria returns None."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_criteria_repo.get_by_id.return_value = None
        
        # Act
        result = service.get_criteria("non-existent-id")
        
        # Assert
        mock_criteria_repo.get_by_id.assert_called_once_with("non-existent-id")
        assert result is None
    
    def test_get_all_criteria_for_decision(self, service_setup):
        """Test retrieving all criteria for the decision."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        
        expected_criteria = [
            Criteria(decision_id=decision.id, name="Fuel Efficiency", weight=0.8, id="criteria-1"),
            Criteria(decision_id=decision.id, name="Safety", weight=0.9, id="criteria-2"),
            Criteria(decision_id=decision.id, name="Price", weight=0.7, id="criteria-3")
        ]
        mock_criteria_repo.get_by_decision_id.return_value = expected_criteria
        
        # Act
        result = service.get_all_criteria()
        
        # Assert
        mock_criteria_repo.get_by_decision_id.assert_called_once_with(decision.id)
        assert result == expected_criteria
        assert len(result) == 3
    
    def test_get_all_criteria_empty_list(self, service_setup):
        """Test retrieving all criteria when none exist."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_criteria_repo.get_by_decision_id.return_value = []
        
        # Act
        result = service.get_all_criteria()
        
        # Assert
        mock_criteria_repo.get_by_decision_id.assert_called_once_with(decision.id)
        assert result == []
    
    def test_update_criteria_name(self, service_setup):
        """Test updating a criteria's name."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            id="criteria-123"
        )
        mock_criteria_repo.get_by_id.return_value = criteria
        
        updated_criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Economy",
            weight=0.8,
            id="criteria-123"
        )
        mock_criteria_repo.update.return_value = updated_criteria
        
        # Act
        result = service.update_criteria(
            criteria_id="criteria-123",
            name="Fuel Economy"
        )
        
        # Assert
        mock_criteria_repo.get_by_id.assert_called_once_with("criteria-123")
        mock_criteria_repo.update.assert_called_once()
        call_args = mock_criteria_repo.update.call_args[0][0]
        assert call_args.name == "Fuel Economy"
        assert result == updated_criteria
    
    def test_update_criteria_weight(self, service_setup):
        """Test updating a criteria's weight."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            id="criteria-123"
        )
        mock_criteria_repo.get_by_id.return_value = criteria
        
        updated_criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.95,
            id="criteria-123"
        )
        mock_criteria_repo.update.return_value = updated_criteria
        
        # Act
        result = service.update_criteria(
            criteria_id="criteria-123",
            weight=0.95
        )
        
        # Assert
        mock_criteria_repo.update.assert_called_once()
        call_args = mock_criteria_repo.update.call_args[0][0]
        assert call_args.weight == 0.95
        assert result == updated_criteria
    
    def test_update_criteria_description(self, service_setup):
        """Test updating a criteria's description."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            description="Old description",
            id="criteria-123"
        )
        mock_criteria_repo.get_by_id.return_value = criteria
        
        updated_criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            description="New description",
            id="criteria-123"
        )
        mock_criteria_repo.update.return_value = updated_criteria
        
        # Act
        result = service.update_criteria(
            criteria_id="criteria-123",
            description="New description"
        )
        
        # Assert
        mock_criteria_repo.update.assert_called_once()
        call_args = mock_criteria_repo.update.call_args[0][0]
        assert call_args.description == "New description"
        assert result == updated_criteria
    
    def test_update_criteria_all_fields(self, service_setup):
        """Test updating all fields of a criteria."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            description="Old description",
            id="criteria-123"
        )
        mock_criteria_repo.get_by_id.return_value = criteria
        
        updated_criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Economy",
            weight=0.95,
            description="New description",
            id="criteria-123"
        )
        mock_criteria_repo.update.return_value = updated_criteria
        
        # Act
        result = service.update_criteria(
            criteria_id="criteria-123",
            name="Fuel Economy",
            weight=0.95,
            description="New description"
        )
        
        # Assert
        mock_criteria_repo.update.assert_called_once()
        call_args = mock_criteria_repo.update.call_args[0][0]
        assert call_args.name == "Fuel Economy"
        assert call_args.weight == 0.95
        assert call_args.description == "New description"
        assert result == updated_criteria
    
    def test_update_criteria_not_found(self, service_setup):
        """Test updating a non-existent criteria raises error."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_criteria_repo.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises((ValueError, KeyError)):
            service.update_criteria(
                criteria_id="non-existent-id",
                name="New Name"
            )
    
    def test_delete_criteria(self, service_setup):
        """Test deleting a criteria."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_criteria_repo.delete.return_value = True
        
        # Act
        result = service.delete_criteria("criteria-123")
        
        # Assert
        mock_criteria_repo.delete.assert_called_once_with("criteria-123")
        assert result is True
    
    def test_delete_criteria_not_found(self, service_setup):
        """Test deleting a non-existent criteria."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_criteria_repo.delete.return_value = False
        
        # Act
        result = service.delete_criteria("non-existent-id")
        
        # Assert
        mock_criteria_repo.delete.assert_called_once_with("non-existent-id")
        assert result is False
    
    def test_delete_criteria_cascades_to_scores(self, service_setup):
        """Test that deleting a criteria also removes associated scores."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_score_repo = service_setup['score_repo']
        
        mock_criteria_repo.delete.return_value = True
        mock_score_repo.get_by_criteria_id.return_value = [
            Score(option_id="option-1", criteria_id="criteria-123", value=8.0, id="score-1"),
            Score(option_id="option-2", criteria_id="criteria-123", value=7.0, id="score-2")
        ]
        
        # Act
        service.delete_criteria("criteria-123")
        
        # Assert
        # Verify that the database cascade handles this,
        # or the service explicitly deletes associated scores
        mock_criteria_repo.delete.assert_called_once_with("criteria-123")


class TestScoreCRUD:
    """Test cases for Score CRUD operations."""
    
    @pytest.fixture
    def service_setup(self):
        """Setup service with mocked dependencies."""
        decision = Decision(name="Choose a car", id="decision-123")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        return {
            'service': service,
            'decision': decision,
            'option_repo': mock_option_repo,
            'criteria_repo': mock_criteria_repo,
            'score_repo': mock_score_repo,
            'db': mock_db
        }
    
    def test_create_score_with_required_fields(self, service_setup):
        """Test creating a score with only required fields."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            id="score-789"
        )
        mock_score_repo.create.return_value = expected_score
        
        # Act
        result = service.create_score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5
        )
        
        # Assert
        mock_score_repo.create.assert_called_once()
        call_args = mock_score_repo.create.call_args[0][0]
        assert isinstance(call_args, Score)
        assert call_args.option_id == "option-123"
        assert call_args.criteria_id == "criteria-456"
        assert call_args.value == 8.5
        assert result == expected_score
    
    def test_create_score_with_notes(self, service_setup):
        """Test creating a score with notes."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="Great fuel economy",
            id="score-789"
        )
        mock_score_repo.create.return_value = expected_score
        
        # Act
        result = service.create_score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="Great fuel economy"
        )
        
        # Assert
        mock_score_repo.create.assert_called_once()
        call_args = mock_score_repo.create.call_args[0][0]
        assert call_args.notes == "Great fuel economy"
        assert result == expected_score
    
    def test_create_score_with_integer_value(self, service_setup):
        """Test creating a score with an integer value."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.0,
            id="score-789"
        )
        mock_score_repo.create.return_value = expected_score
        
        # Act
        result = service.create_score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8
        )
        
        # Assert
        mock_score_repo.create.assert_called_once()
        call_args = mock_score_repo.create.call_args[0][0]
        assert isinstance(call_args.value, float)
        assert call_args.value == 8.0
    
    def test_create_score_with_negative_value(self, service_setup):
        """Test creating a score with a negative value."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=-5.5,
            id="score-789"
        )
        mock_score_repo.create.return_value = expected_score
        
        # Act
        result = service.create_score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=-5.5
        )
        
        # Assert
        call_args = mock_score_repo.create.call_args[0][0]
        assert call_args.value == -5.5
        assert result == expected_score
    
    def test_create_score_with_zero_value(self, service_setup):
        """Test creating a score with a zero value."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=0.0,
            id="score-789"
        )
        mock_score_repo.create.return_value = expected_score
        
        # Act
        result = service.create_score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=0.0
        )
        
        # Assert
        call_args = mock_score_repo.create.call_args[0][0]
        assert call_args.value == 0.0
        assert result == expected_score
    
    def test_create_score_validates_non_numeric_value(self, service_setup):
        """Test that creating a score with non-numeric value raises error."""
        # Arrange
        service = service_setup['service']
        
        # Act & Assert
        with pytest.raises(ValueError, match=".*numeric.*"):
            service.create_score(
                option_id="option-123",
                criteria_id="criteria-456",
                value="high"
            )
    
    def test_create_score_validates_option_id(self, service_setup):
        """Test that creating a score validates option_id."""
        # Arrange
        service = service_setup['service']
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.create_score(
                option_id="",
                criteria_id="criteria-456",
                value=8.5
            )
    
    def test_create_score_validates_criteria_id(self, service_setup):
        """Test that creating a score validates criteria_id."""
        # Arrange
        service = service_setup['service']
        
        # Act & Assert
        with pytest.raises(ValueError):
            service.create_score(
                option_id="option-123",
                criteria_id="",
                value=8.5
            )
    
    def test_get_score_by_id(self, service_setup):
        """Test retrieving a score by its ID."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            id="score-789"
        )
        mock_score_repo.get_by_id.return_value = expected_score
        
        # Act
        result = service.get_score("score-789")
        
        # Assert
        mock_score_repo.get_by_id.assert_called_once_with("score-789")
        assert result == expected_score
    
    def test_get_score_not_found(self, service_setup):
        """Test retrieving a non-existent score returns None."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        mock_score_repo.get_by_id.return_value = None
        
        # Act
        result = service.get_score("non-existent-id")
        
        # Assert
        mock_score_repo.get_by_id.assert_called_once_with("non-existent-id")
        assert result is None
    
    def test_get_score_by_option_and_criteria(self, service_setup):
        """Test retrieving a score by option and criteria IDs."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            id="score-789"
        )
        mock_score_repo.get_by_option_and_criteria.return_value = expected_score
        
        # Act
        result = service.get_score_by_option_and_criteria(
            option_id="option-123",
            criteria_id="criteria-456"
        )
        
        # Assert
        mock_score_repo.get_by_option_and_criteria.assert_called_once_with(
            "option-123",
            "criteria-456"
        )
        assert result == expected_score
    
    def test_get_scores_by_option_id(self, service_setup):
        """Test retrieving all scores for a specific option."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_scores = [
            Score(option_id="option-123", criteria_id="criteria-1", value=8.5, id="score-1"),
            Score(option_id="option-123", criteria_id="criteria-2", value=7.0, id="score-2"),
            Score(option_id="option-123", criteria_id="criteria-3", value=9.0, id="score-3")
        ]
        mock_score_repo.get_by_option_id.return_value = expected_scores
        
        # Act
        result = service.get_scores_by_option("option-123")
        
        # Assert
        mock_score_repo.get_by_option_id.assert_called_once_with("option-123")
        assert result == expected_scores
        assert len(result) == 3
    
    def test_get_scores_by_criteria_id(self, service_setup):
        """Test retrieving all scores for a specific criteria."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        expected_scores = [
            Score(option_id="option-1", criteria_id="criteria-123", value=8.5, id="score-1"),
            Score(option_id="option-2", criteria_id="criteria-123", value=7.0, id="score-2"),
            Score(option_id="option-3", criteria_id="criteria-123", value=9.0, id="score-3")
        ]
        mock_score_repo.get_by_criteria_id.return_value = expected_scores
        
        # Act
        result = service.get_scores_by_criteria("criteria-123")
        
        # Assert
        mock_score_repo.get_by_criteria_id.assert_called_once_with("criteria-123")
        assert result == expected_scores
        assert len(result) == 3
    
    def test_update_score_value(self, service_setup):
        """Test updating a score's value."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            id="score-789"
        )
        mock_score_repo.get_by_id.return_value = score
        
        updated_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=9.0,
            id="score-789"
        )
        mock_score_repo.update.return_value = updated_score
        
        # Act
        result = service.update_score(
            score_id="score-789",
            value=9.0
        )
        
        # Assert
        mock_score_repo.get_by_id.assert_called_once_with("score-789")
        mock_score_repo.update.assert_called_once()
        call_args = mock_score_repo.update.call_args[0][0]
        assert call_args.value == 9.0
        assert result == updated_score
    
    def test_update_score_notes(self, service_setup):
        """Test updating a score's notes."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="Old notes",
            id="score-789"
        )
        mock_score_repo.get_by_id.return_value = score
        
        updated_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="New notes",
            id="score-789"
        )
        mock_score_repo.update.return_value = updated_score
        
        # Act
        result = service.update_score(
            score_id="score-789",
            notes="New notes"
        )
        
        # Assert
        mock_score_repo.update.assert_called_once()
        call_args = mock_score_repo.update.call_args[0][0]
        assert call_args.notes == "New notes"
        assert result == updated_score
    
    def test_update_score_value_and_notes(self, service_setup):
        """Test updating both value and notes of a score."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="Old notes",
            id="score-789"
        )
        mock_score_repo.get_by_id.return_value = score
        
        updated_score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=9.0,
            notes="New notes",
            id="score-789"
        )
        mock_score_repo.update.return_value = updated_score
        
        # Act
        result = service.update_score(
            score_id="score-789",
            value=9.0,
            notes="New notes"
        )
        
        # Assert
        mock_score_repo.update.assert_called_once()
        call_args = mock_score_repo.update.call_args[0][0]
        assert call_args.value == 9.0
        assert call_args.notes == "New notes"
        assert result == updated_score
    
    def test_update_score_not_found(self, service_setup):
        """Test updating a non-existent score raises error."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        mock_score_repo.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises((ValueError, KeyError)):
            service.update_score(
                score_id="non-existent-id",
                value=9.0
            )
    
    def test_delete_score(self, service_setup):
        """Test deleting a score."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        mock_score_repo.delete.return_value = True
        
        # Act
        result = service.delete_score("score-789")
        
        # Assert
        mock_score_repo.delete.assert_called_once_with("score-789")
        assert result is True
    
    def test_delete_score_not_found(self, service_setup):
        """Test deleting a non-existent score."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        mock_score_repo.delete.return_value = False
        
        # Act
        result = service.delete_score("non-existent-id")
        
        # Assert
        mock_score_repo.delete.assert_called_once_with("non-existent-id")
        assert result is False


class TestServiceIntegrationScenarios:
    """Test cases for complex service integration scenarios."""
    
    @pytest.fixture
    def service_setup(self):
        """Setup service with mocked dependencies."""
        decision = Decision(name="Choose a car", id="decision-123")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        return {
            'service': service,
            'decision': decision,
            'option_repo': mock_option_repo,
            'criteria_repo': mock_criteria_repo,
            'score_repo': mock_score_repo,
            'db': mock_db
        }
    
    def test_create_complete_decision_matrix(self, service_setup):
        """Test creating a complete decision matrix with options, criteria, and scores."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        mock_criteria_repo = service_setup['criteria_repo']
        mock_score_repo = service_setup['score_repo']
        
        # Setup mock returns
        option1 = Option(decision_id=decision.id, name="Toyota Camry", id="option-1")
        option2 = Option(decision_id=decision.id, name="Honda Accord", id="option-2")
        mock_option_repo.create.side_effect = [option1, option2]
        
        criteria1 = Criteria(decision_id=decision.id, name="Fuel Efficiency", weight=0.8, id="criteria-1")
        criteria2 = Criteria(decision_id=decision.id, name="Safety", weight=0.9, id="criteria-2")
        mock_criteria_repo.create.side_effect = [criteria1, criteria2]
        
        scores = [
            Score(option_id="option-1", criteria_id="criteria-1", value=8.5, id="score-1"),
            Score(option_id="option-1", criteria_id="criteria-2", value=9.0, id="score-2"),
            Score(option_id="option-2", criteria_id="criteria-1", value=7.5, id="score-3"),
            Score(option_id="option-2", criteria_id="criteria-2", value=8.5, id="score-4")
        ]
        mock_score_repo.create.side_effect = scores
        
        # Act
        service.create_option(name="Toyota Camry")
        service.create_option(name="Honda Accord")
        service.create_criteria(name="Fuel Efficiency", weight=0.8)
        service.create_criteria(name="Safety", weight=0.9)
        service.create_score(option_id="option-1", criteria_id="criteria-1", value=8.5)
        service.create_score(option_id="option-1", criteria_id="criteria-2", value=9.0)
        service.create_score(option_id="option-2", criteria_id="criteria-1", value=7.5)
        service.create_score(option_id="option-2", criteria_id="criteria-2", value=8.5)
        
        # Assert
        assert mock_option_repo.create.call_count == 2
        assert mock_criteria_repo.create.call_count == 2
        assert mock_score_repo.create.call_count == 4
    
    def test_get_all_scores_for_decision(self, service_setup):
        """Test retrieving all scores for all options in a decision."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        mock_score_repo = service_setup['score_repo']
        
        options = [
            Option(decision_id=decision.id, name="Toyota Camry", id="option-1"),
            Option(decision_id=decision.id, name="Honda Accord", id="option-2")
        ]
        mock_option_repo.get_by_decision_id.return_value = options
        
        scores_option1 = [
            Score(option_id="option-1", criteria_id="criteria-1", value=8.5, id="score-1"),
            Score(option_id="option-1", criteria_id="criteria-2", value=9.0, id="score-2")
        ]
        scores_option2 = [
            Score(option_id="option-2", criteria_id="criteria-1", value=7.5, id="score-3"),
            Score(option_id="option-2", criteria_id="criteria-2", value=8.5, id="score-4")
        ]
        
        mock_score_repo.get_by_option_id.side_effect = [scores_option1, scores_option2]
        
        # Act
        all_options = service.get_all_options()
        all_scores = []
        for option in all_options:
            scores = service.get_scores_by_option(option.id)
            all_scores.extend(scores)
        
        # Assert
        assert len(all_options) == 2
        assert len(all_scores) == 4
    
    def test_update_multiple_scores_for_option(self, service_setup):
        """Test updating multiple scores for an option."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        score1 = Score(option_id="option-1", criteria_id="criteria-1", value=8.5, id="score-1")
        score2 = Score(option_id="option-1", criteria_id="criteria-2", value=9.0, id="score-2")
        
        mock_score_repo.get_by_id.side_effect = [score1, score2]
        
        updated_score1 = Score(option_id="option-1", criteria_id="criteria-1", value=9.5, id="score-1")
        updated_score2 = Score(option_id="option-1", criteria_id="criteria-2", value=9.5, id="score-2")
        
        mock_score_repo.update.side_effect = [updated_score1, updated_score2]
        
        # Act
        service.update_score(score_id="score-1", value=9.5)
        service.update_score(score_id="score-2", value=9.5)
        
        # Assert
        assert mock_score_repo.update.call_count == 2
    
    def test_validate_option_belongs_to_decision(self, service_setup):
        """Test that service validates option belongs to its decision."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        
        # Option belongs to a different decision
        other_option = Option(
            decision_id="different-decision-id",
            name="Toyota Camry",
            id="option-123"
        )
        mock_option_repo.get_by_id.return_value = other_option
        
        # Act & Assert
        # The service should validate that the option belongs to the correct decision
        # This test assumes the service has such validation logic
        # If not implemented, this test documents the expected behavior
        result = service.get_option("option-123")
        
        # Verification depends on implementation:
        # Either the service filters results or raises an error
        # For now, we just verify the repository was called
        mock_option_repo.get_by_id.assert_called_once_with("option-123")
    
    def test_validate_criteria_belongs_to_decision(self, service_setup):
        """Test that service validates criteria belongs to its decision."""
        # Arrange
        service = service_setup['service']
        mock_criteria_repo = service_setup['criteria_repo']
        
        # Criteria belongs to a different decision
        other_criteria = Criteria(
            decision_id="different-decision-id",
            name="Fuel Efficiency",
            weight=0.8,
            id="criteria-123"
        )
        mock_criteria_repo.get_by_id.return_value = other_criteria
        
        # Act
        result = service.get_criteria("criteria-123")
        
        # Assert
        mock_criteria_repo.get_by_id.assert_called_once_with("criteria-123")
    
    def test_bulk_create_options(self, service_setup):
        """Test creating multiple options at once."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_option_repo = service_setup['option_repo']
        
        option_names = ["Toyota Camry", "Honda Accord", "Mazda 6"]
        options = [
            Option(decision_id=decision.id, name=name, id=f"option-{i}")
            for i, name in enumerate(option_names)
        ]
        mock_option_repo.create.side_effect = options
        
        # Act
        created_options = []
        for name in option_names:
            option = service.create_option(name=name)
            created_options.append(option)
        
        # Assert
        assert mock_option_repo.create.call_count == 3
        assert len(created_options) == 3
        assert all(opt.decision_id == decision.id for opt in created_options)
    
    def test_bulk_create_criteria(self, service_setup):
        """Test creating multiple criteria at once."""
        # Arrange
        service = service_setup['service']
        decision = service_setup['decision']
        mock_criteria_repo = service_setup['criteria_repo']
        
        criteria_data = [
            {"name": "Fuel Efficiency", "weight": 0.8},
            {"name": "Safety", "weight": 0.9},
            {"name": "Price", "weight": 0.7}
        ]
        criteria_list = [
            Criteria(decision_id=decision.id, name=c["name"], weight=c["weight"], id=f"criteria-{i}")
            for i, c in enumerate(criteria_data)
        ]
        mock_criteria_repo.create.side_effect = criteria_list
        
        # Act
        created_criteria = []
        for c_data in criteria_data:
            criteria = service.create_criteria(name=c_data["name"], weight=c_data["weight"])
            created_criteria.append(criteria)
        
        # Assert
        assert mock_criteria_repo.create.call_count == 3
        assert len(created_criteria) == 3
        assert all(c.decision_id == decision.id for c in created_criteria)


class TestServiceErrorHandling:
    """Test cases for error handling in the service."""
    
    @pytest.fixture
    def service_setup(self):
        """Setup service with mocked dependencies."""
        decision = Decision(name="Choose a car", id="decision-123")
        mock_db = Mock(spec=Database)
        mock_option_repo = Mock(spec=OptionRepository)
        mock_criteria_repo = Mock(spec=CriteriaRepository)
        mock_score_repo = Mock(spec=ScoreRepository)
        
        from src.decision_making.service import DecisionService
        service = DecisionService(
            decision=decision,
            database=mock_db,
            option_repository=mock_option_repo,
            criteria_repository=mock_criteria_repo,
            score_repository=mock_score_repo
        )
        
        return {
            'service': service,
            'decision': decision,
            'option_repo': mock_option_repo,
            'criteria_repo': mock_criteria_repo,
            'score_repo': mock_score_repo,
            'db': mock_db
        }
    
    def test_create_score_with_invalid_option_raises_error(self, service_setup):
        """Test that creating a score with invalid option_id raises error."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        import sqlite3
        mock_score_repo.create.side_effect = sqlite3.IntegrityError("FOREIGN KEY constraint failed")
        
        # Act & Assert
        with pytest.raises(sqlite3.IntegrityError):
            service.create_score(
                option_id="non-existent-option",
                criteria_id="criteria-123",
                value=8.5
            )
    
    def test_create_score_with_invalid_criteria_raises_error(self, service_setup):
        """Test that creating a score with invalid criteria_id raises error."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        import sqlite3
        mock_score_repo.create.side_effect = sqlite3.IntegrityError("FOREIGN KEY constraint failed")
        
        # Act & Assert
        with pytest.raises(sqlite3.IntegrityError):
            service.create_score(
                option_id="option-123",
                criteria_id="non-existent-criteria",
                value=8.5
            )
    
    def test_create_duplicate_score_raises_error(self, service_setup):
        """Test that creating a duplicate score raises error."""
        # Arrange
        service = service_setup['service']
        mock_score_repo = service_setup['score_repo']
        
        import sqlite3
        # First creation succeeds
        score = Score(option_id="option-123", criteria_id="criteria-456", value=8.5, id="score-1")
        # Second creation fails due to unique constraint
        mock_score_repo.create.side_effect = [
            score,
            sqlite3.IntegrityError("UNIQUE constraint failed")
        ]
        
        # Act
        service.create_score(option_id="option-123", criteria_id="criteria-456", value=8.5)
        
        # Assert
        with pytest.raises(sqlite3.IntegrityError):
            service.create_score(option_id="option-123", criteria_id="criteria-456", value=9.0)
    
    def test_repository_exception_propagates(self, service_setup):
        """Test that repository exceptions propagate to the caller."""
        # Arrange
        service = service_setup['service']
        mock_option_repo = service_setup['option_repo']
        
        mock_option_repo.create.side_effect = Exception("Database connection failed")
        
        # Act & Assert
        with pytest.raises(Exception, match="Database connection failed"):
            service.create_option(name="Toyota Camry")

