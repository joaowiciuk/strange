"""
Main entry point for the decision-making tool.

This module provides example usage of the decision-making tool.
"""

from .models import Decision, Option, Criteria, Score
from .persistence import Database
from .repositories import DecisionRepository, OptionRepository, CriteriaRepository, ScoreRepository
from .service import DecisionService


def example_usage():
    """Example usage demonstrating decision creation, scoring, and weighted calculation."""
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
    
    service = DecisionService(decision, option_repo, criteria_repo, score_repo)
    
    service.create_option("Python", "High-level, versatile language with great frameworks")
    service.create_option("JavaScript/TypeScript", "Full-stack capability with Node.js and modern frameworks")
    service.create_option("Go", "Fast, compiled language with excellent concurrency support")
    
    service.create_criteria("Developer Productivity", "How quickly can developers write and maintain code", 0.9)
    service.create_criteria("Performance", "Runtime performance and resource efficiency", 0.7)
    service.create_criteria("Community Support", "Size and activity of the developer community", 0.8)
    service.create_criteria("Learning Curve", "How easy it is for new developers to learn", 0.6)
    
    options = service.get_all_options()
    criteria = service.get_all_criteria()
    
    scores_data = [
        (0, 0, 9.0, "Excellent productivity with clear syntax"),
        (0, 1, 6.5, "Good performance but slower than compiled languages"),
        (0, 2, 9.5, "Huge community and extensive libraries"),
        (0, 3, 8.5, "Easy to learn for beginners"),
        (1, 0, 8.0, "Good productivity with modern frameworks"),
        (1, 1, 7.0, "Decent performance with V8 engine"),
        (1, 2, 9.0, "Very large community, especially in web dev"),
        (1, 3, 7.0, "Moderate learning curve with async patterns"),
        (2, 0, 7.0, "Simple but more verbose than Python"),
        (2, 1, 9.5, "Excellent performance and efficiency"),
        (2, 2, 7.5, "Growing community, great for cloud/backend"),
        (2, 3, 7.5, "Simple to learn but concurrent patterns take time"),
    ]
    
    for opt_idx, crit_idx, value, notes in scores_data:
        service.create_score(options[opt_idx].id, criteria[crit_idx].id, value, notes)
    
    results = service.calculate_weighted_scores()
    
    print(f"\nDecision: {decision.name}")
    print("=" * 60)
    for rank, result in enumerate(results, 1):
        print(f"{rank}. {result['option'].name}: {result['weighted_score']:.2f}")
    
    db.close()


if __name__ == "__main__":
    example_usage()

