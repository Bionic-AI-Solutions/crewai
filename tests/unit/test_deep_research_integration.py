"""Unit tests for Deep Research Tool integration."""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import the tool to test
from comprehensive_curriculum_creator.tools.deep_research_tool import (
    DeepResearchTool,
    ResearchQuery,
    ResearchResult
)


class TestResearchQuery:
    """Test cases for ResearchQuery data structure."""

    def test_research_query_creation_with_string(self):
        """Test creating ResearchQuery from string input."""
        query = ResearchQuery(
            query="What is machine learning?",
            research_mode="deep",
            max_sources=20
        )

        assert query.query == "What is machine learning?"
        assert query.research_mode == "deep"
        assert query.max_sources == 20
        assert query.include_citations is True

    def test_research_query_creation_with_dict(self):
        """Test creating ResearchQuery from dictionary input."""
        query_dict = {
            "query": "Artificial Intelligence basics",
            "research_mode": "academic",
            "max_sources": 30,
            "target_audience": "students"
        }

        query = ResearchQuery(**query_dict)

        assert query.query == "Artificial Intelligence basics"
        assert query.research_mode == "academic"
        assert query.max_sources == 30
        assert query.target_audience == "students"

    def test_research_query_validation(self):
        """Test ResearchQuery validation."""
        # Valid query
        query = ResearchQuery(query="Test query")
        assert query.research_mode == "deep"  # default

        # Invalid research mode should trigger warning but not fail
        with patch('comprehensive_curriculum_creator.tools.deep_research_tool.logger') as mock_logger:
            query = ResearchQuery(query="Test", research_mode="invalid")
            mock_logger.warning.assert_called_once()


class TestResearchResult:
    """Test cases for ResearchResult data structure."""

    def test_research_result_creation(self):
        """Test creating ResearchResult with all fields."""
        result = ResearchResult(
            summary="Comprehensive analysis of AI",
            key_findings=["Finding 1", "Finding 2"],
            sources=[{"title": "Source 1", "url": "http://example.com"}],
            methodology="Multi-source analysis",
            confidence_score=0.85
        )

        assert result.summary == "Comprehensive analysis of AI"
        assert len(result.key_findings) == 2
        assert len(result.sources) == 1
        assert result.confidence_score == 0.85

    def test_research_result_with_optional_fields(self):
        """Test ResearchResult with optional fields."""
        result = ResearchResult(
            summary="Test summary",
            key_findings=["Test finding"],
            sources=[],
            methodology="Test method",
            confidence_score=0.9,
            raw_output="Raw test output"
        )

        assert result.raw_output == "Raw test output"


class TestDeepResearchTool:
    """Test cases for DeepResearchTool functionality."""

    @pytest.fixture
    def tool(self):
        """Create a DeepResearchTool instance for testing."""
        return DeepResearchTool()

    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            "research_timeout": 300,
            "cache_enabled": True,
            "max_retries": 2
        }

    def test_tool_initialization(self, tool):
        """Test tool initialization with default parameters."""
        assert tool.name == "deep_research_tool"
        assert "deep research" in tool.description.lower()
        assert tool.cache_enabled is True
        assert tool.max_retries == 3

    def test_tool_initialization_with_custom_params(self):
        """Test tool initialization with custom parameters."""
        custom_tool = DeepResearchTool(
            research_timeout=600,
            cache_enabled=False,
            max_retries=5
        )

        assert custom_tool.research_timeout == 600
        assert custom_tool.cache_enabled is False
        assert custom_tool.max_retries == 5

    def test_parse_query_with_string(self, tool):
        """Test parsing string query input."""
        result = tool._parse_query(
            "What is Python?",
            "deep",
            20,
            True,
            "developers"
        )

        assert result.query == "What is Python?"
        assert result.research_mode == "deep"
        assert result.max_sources == 20
        assert result.target_audience == "developers"

    def test_parse_query_with_dict(self, tool):
        """Test parsing dictionary query input."""
        query_dict = {
            "query": "Machine Learning",
            "research_mode": "academic",
            "max_sources": 30
        }

        result = tool._parse_query(
            query_dict,
            "quick",  # These should be overridden by dict
            10,
            False,
            None
        )

        assert result.query == "Machine Learning"
        assert result.research_mode == "academic"
        assert result.max_sources == 30

    def test_parse_query_invalid_mode(self, tool):
        """Test parsing query with invalid research mode."""
        with patch('comprehensive_curriculum_creator.tools.deep_research_tool.logger') as mock_logger:
            result = tool._parse_query(
                "Test query",
                "invalid_mode",
                10,
                True,
                None
            )

            # Should default to 'deep' and log warning
            assert result.research_mode == "deep"
            mock_logger.warning.assert_called_once()

    @patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._execute_research')
    def test_run_method_success(self, mock_execute, tool):
        """Test successful execution of research."""
        # Mock the research execution
        mock_result = ResearchResult(
            summary="Test summary",
            key_findings=["Finding 1"],
            sources=[],
            methodology="Test method",
            confidence_score=0.8
        )
        mock_execute.return_value = mock_result

        # Execute the tool
        result = tool._run("Test research query")

        # Verify the result
        assert "Test summary" in result
        assert "Finding 1" in result
        mock_execute.assert_called_once()

    @patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._execute_research')
    def test_run_method_with_caching(self, mock_execute, tool):
        """Test research execution with caching enabled."""
        # Setup cache
        tool._cache = {}

        # First call
        mock_result = ResearchResult(
            summary="Cached summary",
            key_findings=["Cached finding"],
            sources=[],
            methodology="Test method",
            confidence_score=0.8
        )
        mock_execute.return_value = mock_result

        # Execute first time
        result1 = tool._run("Test query")
        assert mock_execute.call_count == 1

        # Execute second time (should use cache)
        result2 = tool._run("Test query")
        assert mock_execute.call_count == 1  # Should not call again

        # Results should be identical
        assert result1 == result2

    def test_cache_key_generation(self, tool):
        """Test cache key generation."""
        query = ResearchQuery(
            query="Test query",
            research_mode="deep",
            max_sources=20,
            target_audience="students"
        )

        key1 = tool._generate_cache_key(query)
        key2 = tool._generate_cache_key(query)

        # Same query should generate same key
        assert key1 == key2
        assert isinstance(key1, str)
        assert len(key1) > 0

    def test_format_research_output(self, tool):
        """Test formatting of research output."""
        result = ResearchResult(
            summary="Test research summary",
            key_findings=["Key finding 1", "Key finding 2"],
            sources=[
                {
                    "title": "Source 1",
                    "url": "http://example.com",
                    "type": "academic",
                    "relevance_score": 0.95
                }
            ],
            methodology="Comprehensive analysis",
            confidence_score=0.85,
            raw_output="Raw research data"
        )

        formatted = tool._format_research_output(result)

        # Check that all sections are present
        assert "# Research Report" in formatted
        assert "## Executive Summary" in formatted
        assert "## Key Findings" in formatted
        assert "## Sources" in formatted
        assert "## Methodology" in formatted
        assert "## Confidence Score" in formatted
        assert "85%" in formatted  # Formatted confidence score

    def test_error_handling(self, tool):
        """Test error handling in research execution."""
        with patch.object(tool, '_execute_research', side_effect=Exception("API Error")):
            result = tool._run("Test query")

            # Should return error message with troubleshooting info
            assert "Deep research failed" in result
            assert "API Error" in result
            assert "Troubleshooting" in result

    def test_error_handling_api_key_error(self, tool):
        """Test error handling for API key issues."""
        api_error = Exception("API key not found")
        with patch.object(tool, '_execute_research', side_effect=api_error):
            result = tool._run("Test query")

            assert "API keys" in result
            assert "environment variables" in result

    def test_error_handling_timeout_error(self, tool):
        """Test error handling for timeout issues."""
        timeout_error = Exception("Research timeout exceeded")
        with patch.object(tool, '_execute_research', side_effect=timeout_error):
            result = tool._run("Test query")

            assert "timeout" in result.lower()
            assert "quick" in result

    @patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._execute_research')
    def test_different_research_modes(self, mock_execute, tool):
        """Test different research modes."""
        mock_result = ResearchResult(
            summary="Mode-specific summary",
            key_findings=["Finding"],
            sources=[],
            methodology="Test",
            confidence_score=0.8
        )
        mock_execute.return_value = mock_result

        # Test quick mode
        result_quick = tool._run("Test", research_mode="quick")
        assert mock_execute.called

        # Test academic mode
        mock_execute.reset_mock()
        result_academic = tool._run("Test", research_mode="academic")
        assert mock_execute.called

    def test_tool_without_cache(self):
        """Test tool with caching disabled."""
        tool = DeepResearchTool(cache_enabled=False)
        assert tool._cache is None

        # Should not attempt caching
        with patch.object(tool, '_execute_research') as mock_execute:
            mock_result = ResearchResult(
                summary="Test",
                key_findings=[],
                sources=[],
                methodology="Test",
                confidence_score=0.8
            )
            mock_execute.return_value = mock_result

            result = tool._run("Test query")
            assert "Test" in result


class TestAsyncFunctionality:
    """Test async functionality of the research tool."""

    @pytest.fixture
    def tool(self):
        """Create tool instance for async testing."""
        return DeepResearchTool()

    @patch('comprehensive_curriculum_creator.tools.deep_research_tool.DeepResearchTool._run')
    async def test_arun_method(self, mock_run, tool):
        """Test async run method."""
        mock_run.return_value = "Test result"

        result = await tool._arun("Test query")

        assert result == "Test result"
        mock_run.assert_called_once_with("Test query")


class TestIntegrationPoints:
    """Test integration points with CrewAI."""

    def test_tool_interface_compatibility(self):
        """Test that tool implements required CrewAI interface."""
        tool = DeepResearchTool()

        # Required attributes
        assert hasattr(tool, 'name')
        assert hasattr(tool, 'description')
        assert hasattr(tool, '_run')

        # Name should be string
        assert isinstance(tool.name, str)

        # Description should be descriptive
        assert len(tool.description) > 50
        assert "research" in tool.description.lower()

    def test_tool_with_different_parameters(self):
        """Test tool with various parameter combinations."""
        tool = DeepResearchTool()

        test_cases = [
            {
                "query": "Simple query",
                "research_mode": "quick",
                "max_sources": 5
            },
            {
                "query": "Complex research topic",
                "research_mode": "deep",
                "max_sources": 25,
                "target_audience": "experts"
            },
            {
                "query": "Academic topic",
                "research_mode": "academic",
                "max_sources": 50,
                "include_citations": True
            }
        ]

        for case in test_cases:
            with patch.object(tool, '_execute_research') as mock_execute:
                mock_result = ResearchResult(
                    summary=f"Summary for {case['query']}",
                    key_findings=["Finding"],
                    sources=[],
                    methodology="Test",
                    confidence_score=0.8
                )
                mock_execute.return_value = mock_result

                result = tool._run(**case)

                assert case['query'] in result
                mock_execute.assert_called()


# Test configuration for pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
