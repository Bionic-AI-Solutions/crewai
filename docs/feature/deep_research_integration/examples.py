#!/usr/bin/env python3
"""
Deep Research Integration Examples

This file contains practical examples of how to use the Deep Research
integration with the curriculum development system.
"""

import os
import sys
from pathlib import Path

# Add the source directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "src"))

from comprehensive_curriculum_creator.tools.deep_research_tool import DeepResearchTool
from comprehensive_curriculum_creator.crew import ComprehensiveCurriculumCreatorCrew


def setup_environment():
    """Set up environment variables for examples."""
    # Check if required API keys are available
    required_keys = ['OPENAI_API_KEY', 'TAVILY_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print("⚠️  Missing required API keys:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease set these environment variables before running examples.")
        print("Example:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("   export TAVILY_API_KEY='your-key-here'")
        return False

    print("✅ Environment setup complete")
    return True


def example_basic_research():
    """Example 1: Basic research query."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Research Query")
    print("="*60)

    tool = DeepResearchTool()

    query = "What are the fundamental concepts of machine learning?"
    print(f"Research Query: {query}")

    try:
        result = tool._run(query)
        print("\nResearch Result (first 500 characters):")
        print(result[:500] + "..." if len(result) > 500 else result)
        print("✅ Basic research example completed")
    except Exception as e:
        print(f"❌ Error in basic research: {e}")


def example_research_modes():
    """Example 2: Different research modes."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Research Modes Comparison")
    print("="*60)

    tool = DeepResearchTool()

    query = "Applications of artificial intelligence in healthcare"
    modes = ['quick', 'deep', 'academic']

    for mode in modes:
        print(f"\n--- {mode.upper()} MODE ---")
        try:
            result = tool._run(query, research_mode=mode)
            # Extract key metrics from result
            lines = result.split('\n')
            summary_line = next((line for line in lines if 'Executive Summary' in line), None)
            confidence_line = next((line for line in lines if 'Confidence Score' in line), None)

            print(f"Mode: {mode}")
            print(f"Summary: {summary_line}")
            print(f"Confidence: {confidence_line}")
            print("✅ Mode test completed")

        except Exception as e:
            print(f"❌ Error in {mode} mode: {e}")


def example_curriculum_research():
    """Example 3: Curriculum-specific research."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Curriculum-Specific Research")
    print("="*60)

    tool = DeepResearchTool()

    curriculum_scenarios = [
        {
            "query": "Best practices for teaching data structures and algorithms",
            "audience": "computer science students",
            "research_mode": "academic"
        },
        {
            "query": "Real-world applications of cloud computing",
            "audience": "IT professionals",
            "research_mode": "deep"
        },
        {
            "query": "Introduction to cybersecurity fundamentals",
            "audience": "beginners",
            "research_mode": "quick"
        }
    ]

    for i, scenario in enumerate(curriculum_scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['query'][:50]}... ---")
        try:
            result = tool._run(
                scenario["query"],
                research_mode=scenario["research_mode"],
                target_audience=scenario["audience"]
            )

            # Analyze result structure
            has_sources = "## Sources" in result
            has_findings = "## Key Findings" in result
            has_methodology = "## Methodology" in result

            print(f"Query: {scenario['query']}")
            print(f"Mode: {scenario['research_mode']}")
            print(f"Audience: {scenario['audience']}")
            print(f"Has Sources: {'✅' if has_sources else '❌'}")
            print(f"Has Key Findings: {'✅' if has_findings else '❌'}")
            print(f"Has Methodology: {'✅' if has_methodology else '❌'}")

            print("✅ Curriculum research example completed")

        except Exception as e:
            print(f"❌ Error in curriculum research: {e}")


def example_error_handling():
    """Example 4: Error handling and fallbacks."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Error Handling and Fallbacks")
    print("="*60)

    tool = DeepResearchTool()

    # Test with invalid query
    print("\n--- Testing Invalid Query ---")
    try:
        result = tool._run("")
        print("❌ Should have failed with empty query")
    except Exception as e:
        print(f"✅ Correctly handled invalid query: {e}")

    # Test with very long query
    print("\n--- Testing Long Query ---")
    long_query = "What are the implications of " * 100  # Very long query
    try:
        result = tool._run(long_query[:500])  # Truncate for safety
        print("✅ Handled long query successfully")
    except Exception as e:
        print(f"Error with long query: {e}")

    # Test timeout scenario (simulated)
    print("\n--- Testing Timeout Handling ---")
    tool_long = DeepResearchTool(research_timeout=1)  # Very short timeout
    try:
        result = tool_long._run("Complex research topic requiring deep analysis")
        print("Result received (may have been truncated)")
    except Exception as e:
        print(f"✅ Handled timeout scenario: {e}")


def example_curriculum_integration():
    """Example 5: Full curriculum integration."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Full Curriculum Integration")
    print("="*60)

    try:
        # Create curriculum instance
        crew_instance = ComprehensiveCurriculumCreatorCrew()

        # Check if deep research tool is integrated
        researcher_agent = crew_instance.subject_matter_researcher()
        tool_names = [tool.__class__.__name__ for tool in researcher_agent.tools]

        print("Research Agent Tools:")
        for tool_name in tool_names:
            status = "✅" if tool_name == 'DeepResearchTool' else "📄"
            print(f"  {status} {tool_name}")

        # Check crew configuration
        crew = crew_instance.crew()
        print("
Crew Configuration:")
        print(f"  Agents: {len(crew.agents)}")
        print(f"  Tasks: {len(crew.tasks)}")
        print(f"  Process: {crew.process}")

        print("✅ Curriculum integration example completed")

    except Exception as e:
        print(f"❌ Error in curriculum integration: {e}")


def example_performance_comparison():
    """Example 6: Performance comparison."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Performance Comparison")
    print("="*60)

    import time

    tool = DeepResearchTool()
    query = "Overview of software development methodologies"

    modes = ['quick', 'deep', 'academic']

    print("Performance Comparison:")
    print("Mode      | Time (s) | Status")
    print("-" * 30)

    for mode in modes:
        try:
            start_time = time.time()
            result = tool._run(query, research_mode=mode)
            execution_time = time.time() - start_time

            status = "✅"
            print("8")

        except Exception as e:
            execution_time = 0
            status = "❌"
            print("8")

    print("\nNote: Actual performance may vary based on API response times and query complexity")


def example_caching_behavior():
    """Example 7: Caching behavior demonstration."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Caching Behavior")
    print("="*60)

    tool = DeepResearchTool(cache_enabled=True)
    query = "Basic concepts of object-oriented programming"

    print("Testing caching behavior...")
    print("First request (should execute research):")

    try:
        start_time = time.time()
        result1 = tool._run(query)
        time1 = time.time() - start_time
        print(".2f"
        print("Second request (should use cache):")
        start_time = time.time()
        result2 = tool._run(query)
        time2 = time.time() - start_time
        print(".2f"
        # Check if results are identical (indicating cache usage)
        if result1 == result2:
            print("✅ Results identical - cache working correctly")
            if time2 < time1 * 0.5:  # Second request much faster
                print("✅ Second request significantly faster - cache hit confirmed")
        else:
            print("⚠️  Results differ - possible cache miss")

    except Exception as e:
        print(f"❌ Error in caching test: {e}")


def run_all_examples():
    """Run all examples in sequence."""
    print("🔬 Deep Research Integration Examples")
    print("="*60)

    if not setup_environment():
        return

    examples = [
        example_basic_research,
        example_research_modes,
        example_curriculum_research,
        example_error_handling,
        example_curriculum_integration,
        example_performance_comparison,
        example_caching_behavior
    ]

    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\n⏹️  Examples interrupted by user")
            break
        except Exception as e:
            print(f"❌ Example {example.__name__} failed: {e}")
            continue

    print("\n" + "="*60)
    print("🎉 All examples completed!")
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific example
        example_name = sys.argv[1]
        example_functions = {
            'basic': example_basic_research,
            'modes': example_research_modes,
            'curriculum': example_curriculum_research,
            'errors': example_error_handling,
            'integration': example_curriculum_integration,
            'performance': example_performance_comparison,
            'caching': example_caching_behavior
        }

        if example_name in example_functions:
            if setup_environment():
                example_functions[example_name]()
        else:
            print(f"Available examples: {', '.join(example_functions.keys())}")
    else:
        # Run all examples
        run_all_examples()
