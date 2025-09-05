#!/usr/bin/env python
import sys
import json
from pathlib import Path
from crewai import Crew
from comprehensive_curriculum_creator.crew import ComprehensiveCurriculumCreatorCrew

def get_user_input():
    """Collect curriculum creation parameters from user with validation"""
    print("\n=== Curriculum Creator - Stage 1: Parameter Collection ===")
    print("Please provide the following information for your curriculum:\n")

    inputs = {}
    max_retries = 3

    # Topic validation
    for attempt in range(max_retries):
        try:
            topic = input("Topic of education: ").strip()
            if not topic:
                raise ValueError("Topic cannot be empty")
            if len(topic) > 200:
                raise ValueError("Topic is too long (max 200 characters)")
            inputs['topic'] = topic
            break
        except ValueError as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise ValueError("Maximum retries exceeded for topic input")

    # Duration validation
    for attempt in range(max_retries):
        try:
            duration = input("Duration of course (e.g., '8 weeks', '3 months'): ").strip()
            if not duration:
                raise ValueError("Duration cannot be empty")
            inputs['duration'] = duration
            break
        except ValueError as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise ValueError("Maximum retries exceeded for duration input")

    # Sessions validation
    for attempt in range(max_retries):
        try:
            sessions_input = input("Number of sessions: ").strip()
            try:
                sessions_num = int(sessions_input)
                if sessions_num <= 0:
                    raise ValueError("Number of sessions must be positive")
                if sessions_num > 100:
                    raise ValueError("Number of sessions cannot exceed 100")
                inputs['sessions'] = str(sessions_num)
                break
            except ValueError:
                raise ValueError("Please enter a valid number for sessions")
        except ValueError as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise ValueError("Maximum retries exceeded for sessions input")

    # Session duration validation
    for attempt in range(max_retries):
        try:
            session_duration = input("Duration of each session (e.g., '2 hours', '90 minutes'): ").strip()
            if not session_duration:
                raise ValueError("Session duration cannot be empty")
            inputs['session_duration'] = session_duration
            break
        except ValueError as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise ValueError("Maximum retries exceeded for session duration input")

    # Project based validation
    for attempt in range(max_retries):
        try:
            project_based = input("Project Based (yes/no): ").strip().lower()
            if project_based not in ['yes', 'no']:
                raise ValueError("Please enter 'yes' or 'no'")
            inputs['project_based'] = project_based
            break
        except ValueError as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise ValueError("Maximum retries exceeded for project based input")

    # Audience level validation
    for attempt in range(max_retries):
        try:
            audience_level = input("Audience level description (e.g., 'Computer Engineers', 'Non-tech', 'Corporate Real estate'): ").strip()
            if not audience_level:
                raise ValueError("Audience level cannot be empty")
            if len(audience_level) > 200:
                raise ValueError("Audience level description is too long (max 200 characters)")
            inputs['audience_level'] = audience_level
            break
        except ValueError as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise ValueError("Maximum retries exceeded for audience level input")

    return inputs

def run_stage1_outline_creation(inputs):
    """Run Stage 1: Create curriculum outline"""
    print("\n=== Stage 1: Creating Curriculum Outline ===")

    # Create crew instance
    crew_instance = ComprehensiveCurriculumCreatorCrew()

    # Create a partial crew that only runs the outline creation task
    partial_crew = Crew(
        agents=[crew_instance.curriculum_architect()],
        tasks=[crew_instance.create_curriculum_outline()],
        verbose=True
    )

    # Run the outline creation
    result = partial_crew.kickoff(inputs=inputs)

    print("\n" + "="*60)
    print("CURRICULUM OUTLINE CREATED - STAGE 1 COMPLETE")
    print("="*60)
    print("\nOutline Result:")
    print(result)

    return result

def get_user_approval():
    """Get user approval to proceed to Stage 2"""
    print("\n" + "="*60)
    print("REVIEW CHECKPOINT - YOUR APPROVAL NEEDED")
    print("="*60)
    print("\nPlease review the curriculum outline above.")
    print("\nDo you approve this outline and want to proceed to Stage 2?")
    print("Stage 2 will include:")
    print("- Deep research on each lesson")
    print("- Creation of detailed learning materials")
    print("- Project development (if applicable)")
    print("- Complete course package generation")

    while True:
        response = input("\nEnter 'yes' to proceed, 'no' to stop, or 'revise' to make changes: ").strip().lower()
        if response in ['yes', 'no', 'revise']:
            return response
        print("Please enter 'yes', 'no', or 'revise'")

def run_full_curriculum_creation(inputs):
    """Run the complete curriculum creation process"""
    print("\n=== Stage 2: Complete Curriculum Development ===")

    crew_instance = ComprehensiveCurriculumCreatorCrew()
    result = crew_instance.crew().kickoff(inputs=inputs)

    print("\n" + "="*60)
    print("CURRICULUM CREATION COMPLETE")
    print("="*60)
    print("\nFinal Result:")
    print(result)

    return result

def run():
    """
    Run the curriculum creator with two-stage process and user feedback.
    """
    try:
        # Stage 1: Collect parameters and create outline
        inputs = get_user_input()

        # Create output directory
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)

        # Save inputs for reference
        with open(output_dir / "curriculum_inputs.json", 'w') as f:
            json.dump(inputs, f, indent=2)

        # Run Stage 1: Outline creation
        outline_result = run_stage1_outline_creation(inputs)

        # Get user approval
        approval = get_user_approval()

        if approval == 'no':
            print("\nCurriculum creation stopped by user request.")
            print("You can restart the process anytime.")
            return

        elif approval == 'revise':
            print("\nPlease provide your revision requests:")
            revisions = input("What changes would you like to make to the outline? ").strip()

            # Update inputs with revision notes
            inputs['revision_notes'] = revisions
            print(f"\nRevision notes recorded: {revisions}")
            print("Please restart the curriculum creator with updated parameters.")
            return

        else:  # approval == 'yes'
            print("\nProceeding to Stage 2: Complete curriculum development...")
            final_result = run_full_curriculum_creation(inputs)

            print("\n" + "="*60)
            print("🎉 CURRICULUM CREATION SUCCESSFULLY COMPLETED!")
            print("="*60)
            print("\nYour curriculum package has been created in the ./output/ directory.")
            print("Check for the zip file containing your complete course materials.")

    except KeyboardInterrupt:
        print("\n\nCurriculum creation interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred during curriculum creation: {str(e)}")
        print("Please check your inputs and try again.")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'topic': 'sample_value',
        'duration': 'sample_value',
        'sessions': 'sample_value',
        'project_based': 'sample_value',
        'audience_level': 'sample_value',
        'session_duration': 'sample_value'
    }
    try:
        ComprehensiveCurriculumCreatorCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ComprehensiveCurriculumCreatorCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'topic': 'sample_value',
        'duration': 'sample_value',
        'sessions': 'sample_value',
        'project_based': 'sample_value',
        'audience_level': 'sample_value',
        'session_duration': 'sample_value'
    }
    try:
        ComprehensiveCurriculumCreatorCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
