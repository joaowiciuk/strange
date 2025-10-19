"""
Unit tests for data models.
"""

import pytest
from datetime import datetime
from src.decision_making.models import Decision, Option, Criteria, Score


class TestDecision:
    """Test cases for the Decision model."""
    
    def test_create_decision_with_required_fields(self):
        """Test creating a decision with only required fields."""
        decision = Decision(name="Choose a car")
        
        assert decision.name == "Choose a car"
        assert decision.description == ""
        assert decision.id is not None
        assert isinstance(decision.created_at, datetime)
        assert isinstance(decision.updated_at, datetime)
    
    def test_create_decision_with_all_fields(self):
        """Test creating a decision with all fields."""
        decision = Decision(
            name="Choose a car",
            description="Need to decide which car to buy"
        )
        
        assert decision.name == "Choose a car"
        assert decision.description == "Need to decide which car to buy"
    
    def test_decision_name_cannot_be_empty(self):
        """Test that decision name cannot be empty."""
        with pytest.raises(ValueError, match="Decision name cannot be empty"):
            Decision(name="")
        
        with pytest.raises(ValueError, match="Decision name cannot be empty"):
            Decision(name="   ")
    
    def test_decision_to_dict(self):
        """Test converting decision to dictionary."""
        decision = Decision(
            name="Choose a car",
            description="Need to decide which car to buy"
        )
        
        data = decision.to_dict()
        
        assert data['name'] == "Choose a car"
        assert data['description'] == "Need to decide which car to buy"
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_decision_from_dict(self):
        """Test creating decision from dictionary."""
        data = {
            'id': 'test-id',
            'name': 'Choose a car',
            'description': 'Need to decide which car to buy',
            'created_at': '2025-01-01T12:00:00',
            'updated_at': '2025-01-01T12:00:00'
        }
        
        decision = Decision.from_dict(data)
        
        assert decision.id == 'test-id'
        assert decision.name == 'Choose a car'
        assert decision.description == 'Need to decide which car to buy'
        assert decision.created_at == datetime(2025, 1, 1, 12, 0, 0)
        assert decision.updated_at == datetime(2025, 1, 1, 12, 0, 0)


class TestOption:
    """Test cases for the Option model."""
    
    def test_create_option_with_required_fields(self):
        """Test creating an option with only required fields."""
        option = Option(
            decision_id="decision-123",
            name="Toyota Camry"
        )
        
        assert option.decision_id == "decision-123"
        assert option.name == "Toyota Camry"
        assert option.description == ""
        assert option.id is not None
        assert isinstance(option.created_at, datetime)
        assert isinstance(option.updated_at, datetime)
    
    def test_create_option_with_all_fields(self):
        """Test creating an option with all fields."""
        option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            description="Reliable and fuel-efficient sedan"
        )
        
        assert option.decision_id == "decision-123"
        assert option.name == "Toyota Camry"
        assert option.description == "Reliable and fuel-efficient sedan"
    
    def test_option_name_cannot_be_empty(self):
        """Test that option name cannot be empty."""
        with pytest.raises(ValueError, match="Option name cannot be empty"):
            Option(decision_id="decision-123", name="")
        
        with pytest.raises(ValueError, match="Option name cannot be empty"):
            Option(decision_id="decision-123", name="   ")
    
    def test_option_must_have_decision_id(self):
        """Test that option must be associated with a decision."""
        with pytest.raises(ValueError, match="Option must be associated with a decision"):
            Option(decision_id="", name="Toyota Camry")
        
        with pytest.raises(ValueError, match="Option must be associated with a decision"):
            Option(decision_id="   ", name="Toyota Camry")
    
    def test_option_to_dict(self):
        """Test converting option to dictionary."""
        option = Option(
            decision_id="decision-123",
            name="Toyota Camry",
            description="Reliable and fuel-efficient sedan"
        )
        
        data = option.to_dict()
        
        assert data['decision_id'] == "decision-123"
        assert data['name'] == "Toyota Camry"
        assert data['description'] == "Reliable and fuel-efficient sedan"
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_option_from_dict(self):
        """Test creating option from dictionary."""
        data = {
            'id': 'option-id',
            'decision_id': 'decision-123',
            'name': 'Toyota Camry',
            'description': 'Reliable and fuel-efficient sedan',
            'created_at': '2025-01-01T12:00:00',
            'updated_at': '2025-01-01T12:00:00'
        }
        
        option = Option.from_dict(data)
        
        assert option.id == 'option-id'
        assert option.decision_id == 'decision-123'
        assert option.name == 'Toyota Camry'
        assert option.description == 'Reliable and fuel-efficient sedan'
        assert option.created_at == datetime(2025, 1, 1, 12, 0, 0)
        assert option.updated_at == datetime(2025, 1, 1, 12, 0, 0)


class TestCriteria:
    """Test cases for the Criteria model."""
    
    def test_create_criteria_with_required_fields(self):
        """Test creating a criteria with only required fields."""
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency"
        )
        
        assert criteria.decision_id == "decision-123"
        assert criteria.name == "Fuel Efficiency"
        assert criteria.weight == 1.0
        assert criteria.description == ""
        assert criteria.id is not None
        assert isinstance(criteria.created_at, datetime)
        assert isinstance(criteria.updated_at, datetime)
    
    def test_create_criteria_with_all_fields(self):
        """Test creating a criteria with all fields."""
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            description="Miles per gallon rating"
        )
        
        assert criteria.decision_id == "decision-123"
        assert criteria.name == "Fuel Efficiency"
        assert criteria.weight == 0.8
        assert criteria.description == "Miles per gallon rating"
    
    def test_criteria_name_cannot_be_empty(self):
        """Test that criteria name cannot be empty."""
        with pytest.raises(ValueError, match="Criteria name cannot be empty"):
            Criteria(decision_id="decision-123", name="")
        
        with pytest.raises(ValueError, match="Criteria name cannot be empty"):
            Criteria(decision_id="decision-123", name="   ")
    
    def test_criteria_must_have_decision_id(self):
        """Test that criteria must be associated with a decision."""
        with pytest.raises(ValueError, match="Criteria must be associated with a decision"):
            Criteria(decision_id="", name="Fuel Efficiency")
        
        with pytest.raises(ValueError, match="Criteria must be associated with a decision"):
            Criteria(decision_id="   ", name="Fuel Efficiency")
    
    def test_criteria_weight_must_be_numeric(self):
        """Test that criteria weight must be numeric."""
        with pytest.raises(ValueError, match="Weight must be a numeric value"):
            Criteria(decision_id="decision-123", name="Fuel Efficiency", weight="high")
    
    def test_criteria_weight_cannot_be_negative(self):
        """Test that criteria weight cannot be negative."""
        with pytest.raises(ValueError, match="Weight cannot be negative"):
            Criteria(decision_id="decision-123", name="Fuel Efficiency", weight=-1.0)
    
    def test_criteria_weight_can_be_zero(self):
        """Test that criteria weight can be zero."""
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.0
        )
        assert criteria.weight == 0.0
    
    def test_criteria_to_dict(self):
        """Test converting criteria to dictionary."""
        criteria = Criteria(
            decision_id="decision-123",
            name="Fuel Efficiency",
            weight=0.8,
            description="Miles per gallon rating"
        )
        
        data = criteria.to_dict()
        
        assert data['decision_id'] == "decision-123"
        assert data['name'] == "Fuel Efficiency"
        assert data['weight'] == 0.8
        assert data['description'] == "Miles per gallon rating"
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_criteria_from_dict(self):
        """Test creating criteria from dictionary."""
        data = {
            'id': 'criteria-id',
            'decision_id': 'decision-123',
            'name': 'Fuel Efficiency',
            'description': 'Miles per gallon rating',
            'weight': 0.8,
            'created_at': '2025-01-01T12:00:00',
            'updated_at': '2025-01-01T12:00:00'
        }
        
        criteria = Criteria.from_dict(data)
        
        assert criteria.id == 'criteria-id'
        assert criteria.decision_id == 'decision-123'
        assert criteria.name == 'Fuel Efficiency'
        assert criteria.description == 'Miles per gallon rating'
        assert criteria.weight == 0.8
        assert criteria.created_at == datetime(2025, 1, 1, 12, 0, 0)
        assert criteria.updated_at == datetime(2025, 1, 1, 12, 0, 0)


class TestScore:
    """Test cases for the Score model."""
    
    def test_create_score_with_required_fields(self):
        """Test creating a score with only required fields."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5
        )
        
        assert score.option_id == "option-123"
        assert score.criteria_id == "criteria-456"
        assert score.value == 8.5
        assert score.notes == ""
        assert score.id is not None
        assert isinstance(score.created_at, datetime)
        assert isinstance(score.updated_at, datetime)
    
    def test_create_score_with_all_fields(self):
        """Test creating a score with all fields."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="Great fuel economy, verified by consumer reports"
        )
        
        assert score.option_id == "option-123"
        assert score.criteria_id == "criteria-456"
        assert score.value == 8.5
        assert score.notes == "Great fuel economy, verified by consumer reports"
    
    def test_score_value_int_converted_to_float(self):
        """Test that integer score values are converted to float."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8
        )
        
        assert score.value == 8.0
        assert isinstance(score.value, float)
    
    def test_score_value_can_be_negative(self):
        """Test that score values can be negative."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=-5.5
        )
        
        assert score.value == -5.5
    
    def test_score_value_can_be_zero(self):
        """Test that score values can be zero."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=0.0
        )
        
        assert score.value == 0.0
    
    def test_score_value_can_be_very_large(self):
        """Test that score values can be very large."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=1000000.5
        )
        
        assert score.value == 1000000.5
    
    def test_score_must_have_option_id(self):
        """Test that score must be associated with an option."""
        with pytest.raises(ValueError, match="Score must be associated with an option"):
            Score(option_id="", criteria_id="criteria-456", value=8.5)
        
        with pytest.raises(ValueError, match="Score must be associated with an option"):
            Score(option_id="   ", criteria_id="criteria-456", value=8.5)
    
    def test_score_must_have_criteria_id(self):
        """Test that score must be associated with a criteria."""
        with pytest.raises(ValueError, match="Score must be associated with a criteria"):
            Score(option_id="option-123", criteria_id="", value=8.5)
        
        with pytest.raises(ValueError, match="Score must be associated with a criteria"):
            Score(option_id="option-123", criteria_id="   ", value=8.5)
    
    def test_score_value_must_be_numeric(self):
        """Test that score value must be numeric."""
        with pytest.raises(ValueError, match="Score value must be a numeric value"):
            Score(option_id="option-123", criteria_id="criteria-456", value="high")
        
        with pytest.raises(ValueError, match="Score value must be a numeric value"):
            Score(option_id="option-123", criteria_id="criteria-456", value=None)
        
        with pytest.raises(ValueError, match="Score value must be a numeric value"):
            Score(option_id="option-123", criteria_id="criteria-456", value=[8.5])
    
    def test_score_to_dict(self):
        """Test converting score to dictionary."""
        score = Score(
            option_id="option-123",
            criteria_id="criteria-456",
            value=8.5,
            notes="Great fuel economy"
        )
        
        data = score.to_dict()
        
        assert data['option_id'] == "option-123"
        assert data['criteria_id'] == "criteria-456"
        assert data['value'] == 8.5
        assert data['notes'] == "Great fuel economy"
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_score_from_dict(self):
        """Test creating score from dictionary."""
        data = {
            'id': 'score-id',
            'option_id': 'option-123',
            'criteria_id': 'criteria-456',
            'value': 8.5,
            'notes': 'Great fuel economy',
            'created_at': '2025-01-01T12:00:00',
            'updated_at': '2025-01-01T12:00:00'
        }
        
        score = Score.from_dict(data)
        
        assert score.id == 'score-id'
        assert score.option_id == 'option-123'
        assert score.criteria_id == 'criteria-456'
        assert score.value == 8.5
        assert score.notes == 'Great fuel economy'
        assert score.created_at == datetime(2025, 1, 1, 12, 0, 0)
        assert score.updated_at == datetime(2025, 1, 1, 12, 0, 0)
    
    def test_score_from_dict_with_missing_notes(self):
        """Test creating score from dictionary with missing notes field."""
        data = {
            'id': 'score-id',
            'option_id': 'option-123',
            'criteria_id': 'criteria-456',
            'value': 8.5,
            'created_at': '2025-01-01T12:00:00',
            'updated_at': '2025-01-01T12:00:00'
        }
        
        score = Score.from_dict(data)
        
        assert score.notes == ""

