# Deep Research Integration

## Overview

The Deep Research Integration enhances the curriculum development system by adding advanced research capabilities powered by Open Deep Research. This integration allows curriculum developers to conduct comprehensive, AI-powered research that goes beyond traditional web searches.

## Features

- **Advanced Research Capabilities**: Access to Open Deep Research with proven performance (ranked #6 on Deep Research Bench)
- **Multiple Research Modes**: Quick, deep, and academic research modes for different needs
- **Seamless Integration**: Works transparently with existing curriculum development workflow
- **Quality Assurance**: Built-in quality metrics and source validation
- **Caching System**: Intelligent result caching to improve performance and reduce costs
- **Error Handling**: Robust error handling with graceful fallbacks

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CrewAI Agent  │────│  Research Tool   │────│  LangGraph App  │
│                 │    │    Wrapper       │    │                 │
│ subject_matter_ │    │                  │    │ Open Deep       │
│ researcher      │    │ - Query Parser   │    │ Research        │
└─────────────────┘    │ - Result Proc    │    │                 │
                       │ - Error Handler  │    └─────────────────┘
                       └──────────────────┘            │
┌─────────────────┐    ┌──────────────────┐           │
│ Research Cache  │    │ Quality          │           │
│                 │    │ Evaluator        │           │
│ - Redis/Cache   │    │                  │           │
│ - TTL Management│    │ - Completeness   │           │
└─────────────────┘    │ - Authority      │           │
                       └──────────────────┘           │
                                                      │
                                               ┌──────┴─────┐
                                               │ Search APIs │
                                               │             │
                                               │ - Tavily    │
                                               │ - OpenAI    │
                                               │ - Anthropic │
                                               │ - MCP Tools │
                                               └────────────┘
```

## Quick Start

### Prerequisites

1. **API Keys**: Set up the following environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export TAVILY_API_KEY="your-tavily-key"
   # Optional:
   export ANTHROPIC_API_KEY="your-anthropic-key"
   export GITHUB_TOKEN="your-github-token"
   ```

2. **Docker Environment**: Ensure Docker is running for the research service.

### Basic Usage

The deep research tool integrates automatically with the curriculum development system. Simply run your curriculum creation as usual:

```python
from comprehensive_curriculum_creator.crew import ComprehensiveCurriculumCreatorCrew

# Create curriculum with enhanced research capabilities
inputs = {
    'topic': 'Machine Learning Fundamentals',
    'duration': '8 weeks',
    'sessions': '16',
    'project_based': 'yes',
    'audience_level': 'Computer Science students'
}

crew_instance = ComprehensiveCurriculumCreatorCrew()
result = crew_instance.crew().kickoff(inputs=inputs)
```

The system will automatically use deep research capabilities when appropriate.

## Research Modes

### Quick Mode
- **Duration**: 5-10 minutes
- **Use Case**: Basic information gathering, fact-checking
- **Sources**: 5-10 sources
- **Best For**: Simple queries, preliminary research

```python
# Automatically selected for basic queries
result = deep_research_tool._run(
    "What is supervised learning?",
    research_mode="quick"
)
```

### Deep Mode
- **Duration**: 15-30 minutes
- **Use Case**: Comprehensive analysis, multi-perspective research
- **Sources**: 15-25 sources
- **Best For**: Detailed topic analysis, industry trends

```python
# Default mode for most research tasks
result = deep_research_tool._run(
    "Latest developments in neural networks",
    research_mode="deep"
)
```

### Academic Mode
- **Duration**: 20-45 minutes
- **Use Case**: Scholarly research, rigorous analysis
- **Sources**: 25-40 sources
- **Best For**: Academic papers, evidence-based research

```python
# For academic and scholarly research
result = deep_research_tool._run(
    "Current research on AI ethics",
    research_mode="academic"
)
```

## Configuration

### Research Configuration

The system uses a comprehensive configuration file located at:
`src/comprehensive_curriculum_creator/config/research_config.yaml`

Key configuration sections:

```yaml
research_modes:
  quick:
    model: "gpt-4o-mini"
    max_iterations: 3
    max_sources: 10
  deep:
    model: "gpt-4o"
    max_iterations: 6
    max_sources: 20
  academic:
    model: "gpt-4o"
    max_iterations: 8
    max_sources: 30

api_config:
  tavily:
    priority: 1
    rate_limit: 1000
  openai:
    priority: 2
    rate_limit: 10000

quality_assurance:
  min_confidence_score: 0.7
  require_citations: true
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for research | Yes |
| `TAVILY_API_KEY` | Tavily search API key | Yes |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional) | No |
| `GITHUB_TOKEN` | GitHub token for repository access | No |

## Docker Setup

### Development Environment

1. **Build the research service**:
   ```bash
   cd research/
   docker-compose build
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Check service health**:
   ```bash
   docker-compose ps
   curl http://localhost:8000/health  # Monitoring service
   ```

### Production Deployment

For production deployment, use the provided docker-compose configuration with appropriate environment variables and resource limits.

## API Reference

### DeepResearchTool

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `research_timeout` | int | 1800 | Research timeout in seconds |
| `max_retries` | int | 3 | Maximum retry attempts |
| `cache_enabled` | bool | True | Enable result caching |
| `docker_compose_path` | str | None | Path to docker-compose.yml |

#### Methods

##### `_run(research_query, **kwargs)`

Execute deep research on a given query.

**Parameters:**
- `research_query` (str or dict): Research topic or structured query
- `research_mode` (str): Research mode ('quick', 'deep', 'academic')
- `max_sources` (int): Maximum sources to analyze
- `include_citations` (bool): Include citations in results
- `target_audience` (str): Target audience for research

**Returns:** Formatted research report as string

##### `_arun(*args, **kwargs)`

Async version of `_run` method.

## Examples

### Basic Research Query

```python
from comprehensive_curriculum_creator.tools.deep_research_tool import DeepResearchTool

tool = DeepResearchTool()
result = tool._run("What are the main types of machine learning algorithms?")
print(result)
```

### Advanced Research with Parameters

```python
result = tool._run(
    research_query="Recent advances in natural language processing",
    research_mode="deep",
    max_sources=25,
    target_audience="data scientists",
    include_citations=True
)
```

### Curriculum-Specific Research

```python
# Research for learning objectives
objectives_research = tool._run(
    "Best practices for teaching machine learning to beginners",
    research_mode="academic",
    target_audience="instructors"
)

# Research for project ideas
project_research = tool._run(
    "Real-world applications of computer vision",
    research_mode="deep",
    target_audience="students"
)
```

### Integration with Curriculum Tasks

```python
from comprehensive_curriculum_creator.crew import ComprehensiveCurriculumCreatorCrew

# The deep research tool is automatically integrated
crew = ComprehensiveCurriculumCreatorCrew()

# Research task will use deep research capabilities
research_task = crew.research_course_content()
# Task description includes deep research guidance
```

## Testing

### Running Unit Tests

```bash
# Run all unit tests
python -m pytest tests/unit/test_deep_research_integration.py -v

# Run specific test
python -m pytest tests/unit/test_deep_research_integration.py::TestDeepResearchTool::test_run_method_success -v
```

### Running Integration Tests

```bash
# Run integration tests
python -m pytest tests/integration/test_curriculum_with_deep_research.py -v

# Run performance tests
python -m pytest tests/integration/test_curriculum_with_deep_research.py::TestResearchPerformance -v
```

### Manual Testing

```python
# Test basic functionality
from comprehensive_curriculum_creator.tools.deep_research_tool import DeepResearchTool

tool = DeepResearchTool()
result = tool._run("Test research query")
print("✅ Basic research test passed")

# Test different modes
for mode in ['quick', 'deep', 'academic']:
    result = tool._run(f"Machine learning {mode} test", research_mode=mode)
    print(f"✅ {mode.capitalize()} mode test passed")
```

## Monitoring and Troubleshooting

### Monitoring Dashboard

Access the monitoring service at `http://localhost:8000` when running with Docker.

### Common Issues

#### API Key Issues
```
Error: API key not found
Solution: Set environment variables OPENAI_API_KEY and TAVILY_API_KEY
```

#### Docker Connection Issues
```
Error: Docker service not available
Solution: Ensure docker-compose is running: docker-compose ps
```

#### Rate Limit Issues
```
Error: Rate limit exceeded
Solution: Reduce concurrent requests or upgrade API plan
```

#### Timeout Issues
```
Error: Research timeout
Solution: Use 'quick' mode for complex queries or increase timeout
```

### Performance Optimization

1. **Enable Caching**: Keep `cache_enabled=True` for repeated queries
2. **Choose Appropriate Mode**: Use 'quick' for simple queries, 'deep' for comprehensive research
3. **Monitor Usage**: Track API usage to optimize costs
4. **Resource Limits**: Configure Docker resource limits based on usage patterns

## Contributing

### Development Setup

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd curriculum/research
   uv sync
   ```

2. **Run tests**:
   ```bash
   uv run pytest tests/
   ```

3. **Start development server**:
   ```bash
   uv run langgraph dev
   ```

### Code Standards

- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

## License

This integration uses the Open Deep Research tool, which is licensed under MIT.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the Open Deep Research documentation
3. Create an issue in the project repository
4. Contact the development team

## Changelog

### Version 1.0.0
- Initial release with basic integration
- Support for all three research modes
- Docker environment setup
- Comprehensive test suite
- Monitoring and logging capabilities

### Future Enhancements
- Enhanced caching strategies
- Additional search APIs support
- Real-time research progress tracking
- Advanced quality metrics
- Multi-language support
