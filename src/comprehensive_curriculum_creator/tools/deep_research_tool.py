"""CrewAI-compatible wrapper for Open Deep Research tool."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import tempfile
import os

from crewai_tools.tools import BaseTool
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchQuery(BaseModel):
    """Structure for research query parameters."""
    query: str = Field(..., description="The research question or topic")
    research_mode: str = Field(default="deep", description="Research mode: 'quick', 'deep', or 'academic'")
    max_sources: int = Field(default=20, description="Maximum number of sources to analyze")
    include_citations: bool = Field(default=True, description="Include citations in the response")
    target_audience: Optional[str] = Field(default=None, description="Target audience for the research")


class ResearchResult(BaseModel):
    """Structure for research results."""
    summary: str = Field(..., description="Executive summary of the research")
    key_findings: List[str] = Field(..., description="Key findings and insights")
    sources: List[Dict[str, Any]] = Field(..., description="Source citations and references")
    methodology: str = Field(..., description="Research methodology used")
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    raw_output: Optional[str] = Field(default=None, description="Raw research output")


class DeepResearchTool(BaseTool):
    """CrewAI-compatible wrapper for Open Deep Research.

    This tool integrates the Open Deep Research agent with CrewAI,
    allowing curriculum developers to conduct comprehensive research
    on any topic using advanced AI-powered research capabilities.
    """

    name: str = "deep_research_tool"
    description: str = """
    Conduct comprehensive deep research on any topic using advanced AI research capabilities.

    This tool provides access to Open Deep Research, which can:
    - Search across multiple academic and web sources
    - Synthesize information from diverse perspectives
    - Generate structured research reports
    - Provide citations and source validation
    - Adapt research depth based on requirements

    Use this tool when you need:
    - Comprehensive research on complex topics
    - Academic or scholarly research
    - Multi-perspective analysis
    - Well-cited and authoritative information
    - Research that goes beyond simple web searches

    Research modes available:
    - 'quick': Fast research for basic information (5-10 min)
    - 'deep': Comprehensive research with multiple sources (15-30 min)
    - 'academic': Scholarly research with rigorous methodology (20-45 min)
    """

    # Tool configuration
    research_timeout: int = Field(default=1800, description="Research timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    cache_enabled: bool = Field(default=True, description="Enable result caching")
    docker_compose_path: Optional[str] = Field(default=None, description="Path to docker-compose.yml")

    def __init__(self, **kwargs):
        """Initialize the Deep Research Tool."""
        super().__init__(**kwargs)

        # Set default docker compose path if not provided
        if self.docker_compose_path is None:
            self.docker_compose_path = str(Path(__file__).parent.parent.parent.parent / "research" / "docker-compose.yml")

        # Validate docker compose file exists
        if not Path(self.docker_compose_path).exists():
            logger.warning(f"Docker compose file not found at {self.docker_compose_path}")
            logger.warning("Make sure the research service is properly set up")

        # Initialize cache if enabled
        self._cache = {} if self.cache_enabled else None

    def _run(
        self,
        research_query: Union[str, Dict[str, Any]],
        research_mode: str = "deep",
        max_sources: int = 20,
        include_citations: bool = True,
        target_audience: Optional[str] = None,
        **kwargs
    ) -> str:
        """Execute deep research using the Open Deep Research tool.

        Args:
            research_query: The research topic or structured query
            research_mode: Research mode ('quick', 'deep', 'academic')
            max_sources: Maximum number of sources to analyze
            include_citations: Whether to include citations
            target_audience: Target audience for the research
            **kwargs: Additional parameters

        Returns:
            Comprehensive research report as a formatted string
        """
        try:
            # Parse and validate input
            query_obj = self._parse_query(research_query, research_mode, max_sources, include_citations, target_audience)

            # Check cache first
            if self.cache_enabled:
                cached_result = self._get_cached_result(query_obj)
                if cached_result:
                    logger.info("Returning cached research result")
                    return cached_result

            # Execute research
            logger.info(f"Starting deep research on: {query_obj.query}")
            result = self._execute_research(query_obj)

            # Cache result
            if self.cache_enabled:
                self._cache_result(query_obj, result)

            # Format and return result
            return self._format_research_output(result)

        except Exception as e:
            logger.error(f"Deep research failed: {str(e)}")
            return self._handle_error(e)

    def _parse_query(
        self,
        research_query: Union[str, Dict[str, Any]],
        research_mode: str,
        max_sources: int,
        include_citations: bool,
        target_audience: Optional[str]
    ) -> ResearchQuery:
        """Parse and validate the research query."""
        if isinstance(research_query, str):
            query_obj = ResearchQuery(
                query=research_query,
                research_mode=research_mode,
                max_sources=max_sources,
                include_citations=include_citations,
                target_audience=target_audience
            )
        elif isinstance(research_query, dict):
            query_obj = ResearchQuery(**research_query)
        else:
            raise ValueError("Research query must be a string or dictionary")

        # Validate research mode
        if query_obj.research_mode not in ['quick', 'deep', 'academic']:
            logger.warning(f"Invalid research mode '{query_obj.research_mode}', defaulting to 'deep'")
            query_obj.research_mode = 'deep'

        return query_obj

    def _execute_research(self, query: ResearchQuery) -> ResearchResult:
        """Execute the research using Open Deep Research."""
        try:
            # For now, return a mock result until the full integration is complete
            # TODO: Implement actual Docker container execution

            logger.info(f"Executing research with mode: {query.research_mode}")

            # Simulate research execution time based on mode
            execution_time = {
                'quick': 5,
                'deep': 15,
                'academic': 30
            }.get(query.research_mode, 15)

            # Create mock result for development/testing
            result = ResearchResult(
                summary=f"Comprehensive research analysis of: {query.query}",
                key_findings=[
                    f"Key finding 1 related to {query.query}",
                    f"Key finding 2 with supporting evidence",
                    f"Key finding 3 with practical implications"
                ],
                sources=[
                    {
                        "title": "Academic Source 1",
                        "url": "https://example.com/source1",
                        "type": "academic",
                        "relevance_score": 0.95
                    },
                    {
                        "title": "Industry Report",
                        "url": "https://example.com/source2",
                        "type": "industry",
                        "relevance_score": 0.88
                    }
                ],
                methodology=f"Multi-source analysis using {query.research_mode} methodology",
                confidence_score=0.85,
                raw_output=f"Raw research output for: {query.query}"
            )

            logger.info(f"Research completed in {execution_time} seconds")
            return result

        except Exception as e:
            logger.error(f"Research execution failed: {str(e)}")
            raise

    def _get_cached_result(self, query: ResearchQuery) -> Optional[str]:
        """Get cached research result if available."""
        if not self.cache_enabled or not self._cache:
            return None

        cache_key = self._generate_cache_key(query)
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            # TODO: Implement TTL check
            return cached_data
        return None

    def _cache_result(self, query: ResearchQuery, result: ResearchResult):
        """Cache the research result."""
        if not self.cache_enabled:
            return

        cache_key = self._generate_cache_key(query)
        self._cache[cache_key] = self._format_research_output(result)
        logger.debug(f"Cached research result for key: {cache_key}")

    def _generate_cache_key(self, query: ResearchQuery) -> str:
        """Generate a cache key for the research query."""
        import hashlib
        key_data = f"{query.query}_{query.research_mode}_{query.max_sources}_{query.target_audience}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _format_research_output(self, result: ResearchResult) -> str:
        """Format the research result as a comprehensive report."""
        output = []

        # Executive Summary
        output.append("# Research Report\n")
        output.append(f"## Executive Summary\n{result.summary}\n")

        # Key Findings
        output.append("## Key Findings\n")
        for i, finding in enumerate(result.key_findings, 1):
            output.append(f"{i}. {finding}")
        output.append("")

        # Methodology
        output.append(f"## Methodology\n{result.methodology}\n")

        # Sources
        if result.sources:
            output.append("## Sources\n")
            for source in result.sources:
                output.append(f"- **{source['title']}**")
                output.append(f"  - URL: {source['url']}")
                output.append(f"  - Type: {source['type']}")
                output.append(f"  - Relevance: {source.get('relevance_score', 'N/A')}")
            output.append("")

        # Confidence Score
        output.append(f"## Confidence Score\n{result.confidence_score:.2%}\n")

        # Raw Output (if requested)
        if result.raw_output:
            output.append("## Raw Research Output\n")
            output.append(f"```\n{result.raw_output}\n```\n")

        return "\n".join(output)

    def _handle_error(self, error: Exception) -> str:
        """Handle and format error responses."""
        error_msg = f"Deep research failed: {str(error)}"

        # Provide helpful guidance based on error type
        if "API key" in str(error).lower():
            error_msg += "\n\nTroubleshooting:\n" + \
                        "- Ensure API keys are properly configured\n" + \
                        "- Check environment variables\n" + \
                        "- Verify API key permissions"
        elif "timeout" in str(error).lower():
            error_msg += "\n\nTroubleshooting:\n" + \
                        "- Research query might be too complex\n" + \
                        "- Try using 'quick' research mode\n" + \
                        "- Consider breaking down the query"
        elif "docker" in str(error).lower():
            error_msg += "\n\nTroubleshooting:\n" + \
                        "- Ensure Docker is running\n" + \
                        "- Check docker-compose configuration\n" + \
                        "- Verify research service is healthy"

        return error_msg

    async def _arun(self, *args, **kwargs) -> str:
        """Async version of the research tool."""
        # For now, delegate to sync version
        # TODO: Implement true async execution
        return self._run(*args, **kwargs)
