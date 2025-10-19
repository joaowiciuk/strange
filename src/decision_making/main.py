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
    # Initialize database and repositories
    db = Database()
    decision_repo = DecisionRepository(db)
    option_repo = OptionRepository(db)
    criteria_repo = CriteriaRepository(db)
    score_repo = ScoreRepository(db)
    
    # Create a decision
    decision = Decision(
        name="Choose a Programming Language for New Project",
        description="Need to select the best programming language for a web application"
    )
    decision_repo.create(decision)
    print(f"Created decision: {decision.name} (ID: {decision.id})")
    
    # Add options
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
        print(f"  Added option: {option.name}")
    
    # Add criteria
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
        print(f"  Added criteria: {criteria.name} (weight: {criteria.weight})")
    
    # Add scores for each option against each criteria
    print("\nScoring options against criteria:")
    
    # Define scores: Python
    scores_data = [
        # Python scores
        (options[0].id, criteria_list[0].id, 9.0, "Excellent productivity with clear syntax"),
        (options[0].id, criteria_list[1].id, 6.5, "Good performance but slower than compiled languages"),
        (options[0].id, criteria_list[2].id, 9.5, "Huge community and extensive libraries"),
        (options[0].id, criteria_list[3].id, 8.5, "Easy to learn for beginners"),
        
        # JavaScript/TypeScript scores
        (options[1].id, criteria_list[0].id, 8.0, "Good productivity with modern frameworks"),
        (options[1].id, criteria_list[1].id, 7.0, "Decent performance with V8 engine"),
        (options[1].id, criteria_list[2].id, 9.0, "Very large community, especially in web dev"),
        (options[1].id, criteria_list[3].id, 7.0, "Moderate learning curve with async patterns"),
        
        # Go scores
        (options[2].id, criteria_list[0].id, 7.0, "Simple but more verbose than Python"),
        (options[2].id, criteria_list[1].id, 9.5, "Excellent performance and efficiency"),
        (options[2].id, criteria_list[2].id, 7.5, "Growing community, great for cloud/backend"),
        (options[2].id, criteria_list[3].id, 7.5, "Simple to learn but concurrent patterns take time"),
    ]
    
    scores_created = 0
    scores_failed = 0
    
    for option_id, criteria_id, value, notes in scores_data:
        try:
            score = Score(
                option_id=option_id,
                criteria_id=criteria_id,
                value=value,
                notes=notes
            )
            score_repo.create(score)
            scores_created += 1
        except Exception as e:
            scores_failed += 1
            print(f"  WARNING: Failed to create score: {e}")
    
    print(f"  Scores added: {scores_created} successful, {scores_failed} failed")
    
    # Retrieve and display all decisions
    print("\n" + "="*50)
    print("All Decisions:")
    print("="*50)
    
    all_decisions = decision_repo.get_all()
    for dec in all_decisions:
        print(f"\nDecision: {dec.name}")
        print(f"  ID: {dec.id}")
        print(f"  Description: {dec.description}")
        
        # Get options for this decision
        dec_options = option_repo.get_by_decision_id(dec.id)
        print(f"\n  Options ({len(dec_options)}):")
        for opt in dec_options:
            print(f"    - {opt.name}: {opt.description}")
        
        # Get criteria for this decision
        dec_criteria = criteria_repo.get_by_decision_id(dec.id)
        print(f"\n  Criteria ({len(dec_criteria)}):")
        for crit in dec_criteria:
            print(f"    - {crit.name} (weight: {crit.weight}): {crit.description}")
        
        # Display scores for each option
        print(f"\n  Scores:")
        for opt in dec_options:
            print(f"\n    {opt.name}:")
            option_scores = score_repo.get_by_option_id(opt.id)
            
            if not option_scores:
                print(f"      (No scores recorded for this option)")
                continue
            
            # Create a mapping of criteria_id to criteria for easy lookup
            criteria_map = {c.id: c for c in dec_criteria}
            
            total_weighted_score = 0.0
            total_weight = 0.0
            
            for score in option_scores:
                criteria = criteria_map.get(score.criteria_id)
                if criteria:
                    weighted_value = score.value * criteria.weight
                    total_weighted_score += weighted_value
                    total_weight += criteria.weight
                    print(f"      {criteria.name}: {score.value}/10 (weighted: {weighted_value:.2f}) - {score.notes}")
                else:
                    print(f"      WARNING: Score references unknown criteria (ID: {score.criteria_id})")
            
            if total_weight > 0:
                final_score = total_weighted_score / total_weight
                print(f"      → Final weighted score: {final_score:.2f}/10")
            else:
                print(f"      WARNING: No valid scores with matching criteria")
    
    # Clean up
    db.close()
    print("\n" + "="*50)
    print("Example completed successfully!")
    print("="*50)


if __name__ == "__main__":
    example_usage()

