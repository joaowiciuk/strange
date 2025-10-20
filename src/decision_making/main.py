"""
Main entry point for the decision-making tool.

This module provides example usage of the decision-making tool.
"""

from .models import Decision, Option, Criteria, Score
from .persistence import Database
from .repositories import DecisionRepository, OptionRepository, CriteriaRepository, ScoreRepository


def example_usage():
    """
    Example usage of the decision-making tool.
    
    This function demonstrates how to:
    1. Create a decision
    2. Add options to the decision
    3. Add criteria for evaluating options
    4. Score each option against each criteria
    5. Store everything in the database
    """
    db = Database()
    decision_repo = DecisionRepository(db)
    option_repo = OptionRepository(db)
    criteria_repo = CriteriaRepository(db)
    score_repo = ScoreRepository(db)
    
    decision = Decision(
        name="Choose a Programming Language for New Project",
        description="Need to select the best programming language for a web application"
    )
    decision_repo.create(decision)
    
    options = [
        Option(
            decision_id=decision.id,
            name="Python",
            description="High-level, versatile language with great frameworks"
        ),
        Option(
            decision_id=decision.id,
            name="JavaScript/TypeScript",
            description="Full-stack capability with Node.js and modern frameworks"
        ),
        Option(
            decision_id=decision.id,
            name="Go",
            description="Fast, compiled language with excellent concurrency support"
        ),
    ]
    for option in options:
        option_repo.create(option)
    
    criteria_list = [
        Criteria(
            decision_id=decision.id,
            name="Developer Productivity",
            weight=0.9,
            description="How quickly can developers write and maintain code"
        ),
        Criteria(
            decision_id=decision.id,
            name="Performance",
            weight=0.7,
            description="Runtime performance and resource efficiency"
        ),
        Criteria(
            decision_id=decision.id,
            name="Community Support",
            weight=0.8,
            description="Size and activity of the developer community"
        ),
        Criteria(
            decision_id=decision.id,
            name="Learning Curve",
            weight=0.6,
            description="How easy it is for new developers to learn"
        ),
    ]
    for criteria in criteria_list:
        criteria_repo.create(criteria)
    
    scores_data = [
        (options[0].id, criteria_list[0].id, 9.0, "Excellent productivity with clear syntax"),
        (options[0].id, criteria_list[1].id, 6.5, "Good performance but slower than compiled languages"),
        (options[0].id, criteria_list[2].id, 9.5, "Huge community and extensive libraries"),
        (options[0].id, criteria_list[3].id, 8.5, "Easy to learn for beginners"),
        
        (options[1].id, criteria_list[0].id, 8.0, "Good productivity with modern frameworks"),
        (options[1].id, criteria_list[1].id, 7.0, "Decent performance with V8 engine"),
        (options[1].id, criteria_list[2].id, 9.0, "Very large community, especially in web dev"),
        (options[1].id, criteria_list[3].id, 7.0, "Moderate learning curve with async patterns"),
        
        (options[2].id, criteria_list[0].id, 7.0, "Simple but more verbose than Python"),
        (options[2].id, criteria_list[1].id, 9.5, "Excellent performance and efficiency"),
        (options[2].id, criteria_list[2].id, 7.5, "Growing community, great for cloud/backend"),
        (options[2].id, criteria_list[3].id, 7.5, "Simple to learn but concurrent patterns take time"),
    ]
    
    for option_id, criteria_id, value, notes in scores_data:
        score = Score(
            option_id=option_id,
            criteria_id=criteria_id,
            value=value,
            notes=notes
        )
        score_repo.create(score)
        
    db.close()


if __name__ == "__main__":
    example_usage()

