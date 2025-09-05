"""Integration tests for curriculum creation with deep research integration."""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import curriculum components
from comprehensive_curriculum_creator.crew import ComprehensiveCurriculumCreatorCrew
from comprehensive_curriculum_creator.tools.deep_research_tool import DeepResearchTool


class TestCurriculumWithDeepResearch:
    """Integration tests for full curriculum workflow with deep research."""

    @pytest.fixture
    def sample_curriculum_inputs(self):
        """Sample curriculum creation inputs."""
        return {
            'topic': 'Introduction to Machine Learning',
            'duration': '8 weeks',
            'sessions': '16',
            'session_duration': '2 hours',
            'project_based': 'yes',
            'audience_level': 'Computer Science students with basic programming knowledge'
        }

    @pytest.fixture
    def mock_research_result(self):
        """Mock research result for testing."""
        return {
            "summary": "Machine Learning is a subset of artificial intelligence...",
            "key_findings": [
                "ML algorithms learn patterns from data",
                "Supervised learning requires labeled data",
                "Neural networks mimic brain structure"
            ],
            "sources": [
                {
                    "title": "Machine Learning Fundamentals",
                    "url": "https://example.com/ml-fundamentals",
                    "type": "academic"
                }
            ],
            "methodology": "Comprehensive analysis of ML literature",
            "confidence_score": 0.88
        }

    def test_curriculum_creation_with_deep_research_enabled(self, sample_curriculum_inputs, mock_research_result):
        """Test full curriculum creation workflow with deep research enabled."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'TAVILY_API_KEY': 'test-key'
        }):
            with patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._execute_research') as mock_research:
                mock_research.return_value = Mock(**mock_research_result)

                # Create crew instance
                crew_instance = ComprehensiveCurriculumCreatorCrew()

                # Test that deep research tool is included
                researcher_agent = crew_instance.subject_matter_researcher()

                # Check if DeepResearchTool is in the tools list
                tool_names = [tool.__class__.__name__ for tool in researcher_agent.tools]
                assert 'DeepResearchTool' in tool_names

    def test_research_task_execution(self, sample_curriculum_inputs, mock_research_result):
        """Test that research tasks are executed with deep research."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'TAVILY_API_KEY': 'test-key'
        }):
            with patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._run') as mock_run:
                mock_run.return_value = """
                # Research Report

                ## Executive Summary
                Comprehensive analysis of Machine Learning fundamentals...

                ## Key Findings
                - ML algorithms learn from data patterns
                - Neural networks provide powerful modeling capabilities
                """

                crew_instance = ComprehensiveCurriculumCreatorCrew()

                # Create research task
                research_task = crew_instance.research_course_content()

                # Verify task configuration
                assert research_task is not None
                assert 'research' in research_task.description.lower()

    def test_research_tool_fallback_behavior(self, sample_curriculum_inputs):
        """Test fallback behavior when deep research is not available."""
        # Test without API keys
        with patch.dict(os.environ, {}, clear=True):
            crew_instance = ComprehensiveCurriculumCreatorCrew()
            researcher_agent = crew_instance.subject_matter_researcher()

            # Should still have basic research tools
            tool_names = [tool.__class__.__name__ for tool in researcher_agent.tools]

            # Should have basic tools but not deep research
            assert 'SerperDevTool' in tool_names
            assert 'WebsiteSearchTool' in tool_names

            # Deep research tool should not be present without API keys
            assert 'DeepResearchTool' not in tool_names

    def test_research_quality_integration(self, mock_research_result):
        """Test that research quality metrics are integrated."""
        tool = DeepResearchTool()

        with patch.object(tool, '_execute_research') as mock_execute:
            mock_execute.return_value = Mock(**mock_research_result)

            result = tool._run("Test research query")

            # Check that confidence score is included
            assert "88%" in result or "0.88" in result

            # Check that sources are included
            assert "sources" in result.lower() or "references" in result.lower()

    def test_curriculum_workflow_with_research_phases(self, sample_curriculum_inputs):
        """Test the complete curriculum workflow with research phases."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'TAVILY_API_KEY': 'test-key'
        }):
            with patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._run') as mock_research:

                # Mock research response
                mock_research.return_value = """
                # Deep Research Report: Machine Learning Fundamentals

                ## Executive Summary
                Machine Learning represents a paradigm shift in computing...

                ## Key Findings
                1. ML algorithms automatically learn patterns from data
                2. Supervised learning uses labeled training data
                3. Deep learning uses neural networks with multiple layers

                ## Sources
                - Russell, S. & Norvig, P. (2020). Artificial Intelligence: A Modern Approach
                - Goodfellow, I. et al. (2016). Deep Learning
                """

                crew_instance = ComprehensiveCurriculumCreatorCrew()

                # Verify crew has all required agents
                assert len(crew_instance.agents) == 5  # All 5 agents should be present

                # Verify crew has all required tasks
                assert len(crew_instance.tasks) == 6  # All 6 tasks should be present

                # Test crew creation
                crew = crew_instance.crew()
                assert crew is not None
                assert crew.process == "sequential"

    def test_research_caching_behavior(self, sample_curriculum_inputs):
        """Test that research results are cached appropriately."""
        tool = DeepResearchTool(cache_enabled=True)

        with patch.object(tool, '_execute_research') as mock_execute:
            mock_result = Mock(
                summary="Test summary",
                key_findings=["Finding 1"],
                sources=[],
                methodology="Test method",
                confidence_score=0.8
            )
            mock_execute.return_value = mock_result

            # First research call
            result1 = tool._run("Machine Learning basics")
            assert mock_execute.call_count == 1

            # Second identical call should use cache
            result2 = tool._run("Machine Learning basics")
            assert mock_execute.call_count == 1  # Should not increase

            # Results should be identical
            assert result1 == result2

    def test_error_handling_in_curriculum_workflow(self, sample_curriculum_inputs):
        """Test error handling throughout the curriculum workflow."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key'
        }):
            with patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._run') as mock_research:

                # Mock research failure
                mock_research.side_effect = Exception("API rate limit exceeded")

                crew_instance = ComprehensiveCurriculumCreatorCrew()
                researcher_agent = crew_instance.subject_matter_researcher()

                # Agent should still be created despite research tool failure
                assert researcher_agent is not None

                # Should have fallback tools available
                tool_names = [tool.__class__.__name__ for tool in researcher_agent.tools]
                assert len(tool_names) >= 2  # At least basic tools should be available

    def test_research_modes_in_curriculum_context(self):
        """Test different research modes work in curriculum context."""
        tool = DeepResearchTool()

        test_cases = [
            ("quick", "Basic ML concepts"),
            ("deep", "Advanced ML algorithms"),
            ("academic", "ML research papers")
        ]

        for mode, query in test_cases:
            with patch.object(tool, '_execute_research') as mock_execute:
                mock_result = Mock(
                    summary=f"{mode.title()} research on {query}",
                    key_findings=[f"Key finding for {mode} mode"],
                    sources=[],
                    methodology=f"{mode} methodology",
                    confidence_score=0.8
                )
                mock_execute.return_value = mock_result

                result = tool._run(query, research_mode=mode)

                assert mode in result.lower() or mode.title() in result
                assert query in result

    def test_parallel_research_execution_simulation(self, sample_curriculum_inputs):
        """Test simulation of parallel research execution."""
        tool = DeepResearchTool()

        # Simulate multiple research queries
        queries = [
            "Supervised Learning",
            "Unsupervised Learning",
            "Deep Learning",
            "Reinforcement Learning"
        ]

        results = []
        with patch.object(tool, '_execute_research') as mock_execute:
            mock_execute.return_value = Mock(
                summary="ML algorithm research",
                key_findings=["Key findings"],
                sources=[],
                methodology="Comprehensive analysis",
                confidence_score=0.85
            )

            for query in queries:
                result = tool._run(query)
                results.append(result)

            # Should have called execute for each query
            assert mock_execute.call_count == len(queries)

            # All results should be similar in structure
            for result in results:
                assert "Research Report" in result
                assert "Executive Summary" in result
                assert "Key Findings" in result

    def test_curriculum_specific_research_scenarios(self):
        """Test research scenarios specific to curriculum development."""
        tool = DeepResearchTool()

        curriculum_scenarios = [
            {
                "query": "Best practices for teaching machine learning to beginners",
                "audience": "students",
                "expected_elements": ["teaching methods", "learning objectives"]
            },
            {
                "query": "Industry applications of deep learning",
                "audience": "professionals",
                "expected_elements": ["use cases", "business applications"]
            },
            {
                "query": "Assessment methods for ML courses",
                "audience": "educators",
                "expected_elements": ["evaluation", "rubrics"]
            }
        ]

        for scenario in curriculum_scenarios:
            with patch.object(tool, '_execute_research') as mock_execute:
                mock_result = Mock(
                    summary=f"Research on {scenario['query']}",
                    key_findings=[f"Finding relevant to {scenario['audience']}"],
                    sources=[],
                    methodology="Curriculum-focused research",
                    confidence_score=0.82
                )
                mock_execute.return_value = mock_result

                result = tool._run(
                    scenario["query"],
                    target_audience=scenario["audience"]
                )

                assert scenario["query"] in result
                # Check for curriculum-relevant content structure
                assert any(element in result.lower() for element in scenario["expected_elements"])

    def test_research_performance_metrics(self):
        """Test that research performance is tracked and reported."""
        tool = DeepResearchTool()

        with patch.object(tool, '_execute_research') as mock_execute:
            import time
            start_time = time.time()

            mock_result = Mock(
                summary="Performance test research",
                key_findings=["Performance finding"],
                sources=[],
                methodology="Performance methodology",
                confidence_score=0.9
            )
            mock_execute.return_value = mock_result

            result = tool._run("Performance test query")

            execution_time = time.time() - start_time

            # Should complete within reasonable time
            assert execution_time < 5.0  # Less than 5 seconds for mock

            # Result should contain performance-relevant information
            assert "research report" in result.lower()
            assert "methodology" in result.lower()

    def test_research_output_formatting_for_curriculum(self):
        """Test that research output is properly formatted for curriculum use."""
        tool = DeepResearchTool()

        with patch.object(tool, '_execute_research') as mock_execute:
            mock_result = Mock(
                summary="Curriculum-ready research summary",
                key_findings=[
                    "Finding 1: Important for learning objectives",
                    "Finding 2: Useful for course content",
                    "Finding 3: Relevant for assessments"
                ],
                sources=[
                    {"title": "Academic Source", "url": "http://example.com", "type": "academic"},
                    {"title": "Industry Report", "url": "http://example.com/report", "type": "industry"}
                ],
                methodology="Structured curriculum research",
                confidence_score=0.87
            )
            mock_execute.return_value = mock_result

            result = tool._run("Curriculum research query")

            # Check formatting elements
            assert "# Research Report" in result
            assert "## Executive Summary" in result
            assert "## Key Findings" in result
            assert "## Sources" in result
            assert "## Methodology" in result
            assert "87%" in result  # Formatted confidence score

            # Check that findings are numbered
            assert "1." in result
            assert "2." in result
            assert "3." in result


# Performance test configuration
@pytest.mark.performance
class TestResearchPerformance:
    """Performance tests for research integration."""

    def test_research_response_time(self):
        """Test that research responses are within acceptable time limits."""
        tool = DeepResearchTool()

        with patch.object(tool, '_execute_research') as mock_execute:
            import time

            mock_result = Mock(
                summary="Quick response test",
                key_findings=["Fast finding"],
                sources=[],
                methodology="Quick method",
                confidence_score=0.8
            )
            mock_execute.return_value = mock_result

            start_time = time.time()
            result = tool._run("Quick test query")
            execution_time = time.time() - start_time

            # Should complete quickly
            assert execution_time < 2.0
            assert len(result) > 100  # Should have substantial content

    def test_concurrent_research_simulation(self):
        """Test simulation of concurrent research requests."""
        tool = DeepResearchTool()

        queries = [f"Research topic {i}" for i in range(5)]

        with patch.object(tool, '_execute_research') as mock_execute:
            mock_result = Mock(
                summary="Concurrent test",
                key_findings=["Concurrent finding"],
                sources=[],
                methodology="Concurrent method",
                confidence_score=0.8
            )
            mock_execute.return_value = mock_result

            import time
            start_time = time.time()

            results = []
            for query in queries:
                result = tool._run(query)
                results.append(result)

            total_time = time.time() - start_time

            # All queries should complete
            assert len(results) == len(queries)

            # Should complete within reasonable total time
            assert total_time < 10.0

            # All results should be valid
            for result in results:
                assert "Research Report" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
