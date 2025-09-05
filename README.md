# 🎓 Comprehensive Curriculum Creator

An AI-powered curriculum creation system that generates complete, professional course materials using CrewAI multi-agent collaboration. This system creates structured, engaging curricula with deep research, project-based learning integration, and professional formatting.

## ✨ Features

- **Two-Stage Creation Process**: Outline creation with user approval, followed by detailed development
- **Multi-Agent Collaboration**: Specialized agents for research, content development, and organization
- **Deep Research Integration**: Multiple research tools for comprehensive content gathering
- **Project-Based Learning**: Real-world use cases and hands-on projects when requested
- **Professional Folder Structure**: Organized delivery in Topic/Module/Week/Session format
- **Complete Course Packages**: Slides, materials, homework, and answer keys for every session
- **Zip File Delivery**: Easy distribution of complete curriculum packages

## 🚀 Quick Start

### Prerequisites
- Python >=3.10 <3.14
- OpenAI API Key (required)
- Optional: Additional API keys for enhanced research capabilities

### Installation

1. **Install UV** (if not already installed):
```bash
pip install uv
```

2. **Clone and setup**:
```bash
cd /workspace/curriculum
uv sync
```

3. **Configure API Keys**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the Curriculum Creator**:
```bash
python -m comprehensive_curriculum_creator.main
```

## 📋 Usage

The curriculum creator follows a two-stage process:

### Stage 1: Outline Creation
1. Enter your curriculum parameters:
   - Topic of education
   - Course duration
   - Number of sessions
   - Session duration
   - Project-based learning (yes/no)
   - Target audience level

2. The system creates a comprehensive curriculum outline
3. **Review Checkpoint**: You can approve, reject, or request revisions

### Stage 2: Complete Development (After Approval)
1. Deep research on each topic using multiple sources
2. Project design (if project-based=yes)
3. Content development for all sessions
4. Professional formatting and organization
5. Zip file creation for easy distribution

## 📁 Output Structure

The system creates a complete curriculum package:

```
{Topic}_Curriculum_Package.zip
├── {Topic}/
│   ├── Course_Overview_and_Guide/
│   │   ├── course_overview.md
│   │   ├── instructor_guide.md
│   │   ├── assessment_rubrics.md
│   │   └── implementation_schedule.md
│   ├── Module_{Name}/
│   │   ├── Week_{Number}/
│   │   │   ├── Session_{Number}/
│   │   │   │   ├── Classwork/
│   │   │   │   │   ├── slides_presentation.md
│   │   │   │   │   └── course_material.md
│   │   │   │   └── Homework/
│   │   │   │       ├── homework_questions.md
│   │   │   │       └── homework_keys.md
```

## 🤖 AI Agents

### Curriculum Architect
- Creates comprehensive course outlines and learning progressions
- Aligns content with educational objectives and audience needs

### Subject Matter Researcher
- Conducts deep research using multiple sources
- Gathers current trends, best practices, and authoritative references

### Learning Content Developer
- Transforms research into engaging learning materials
- Creates slides with detailed talking points and professional formatting

### Project Specialist
- Designs hands-on, real-world projects (when project_based=yes)
- Identifies practical use cases and implementation scenarios

### Course Structure Organizer
- Organizes all materials into the specified folder hierarchy
- Creates downloadable zip packages

## 🔧 Configuration

### Required API Keys
- `OPENAI_API_KEY`: Required for CrewAI and GPT models

### Optional API Keys (Enhance Research)
- `SERPER_API_KEY`: Web search capabilities
- `TAVILY_API_KEY`: Advanced web search and content extraction
- `GITHUB_TOKEN`: Code repository research

## 🛠️ Customization

### Modifying Agent Behavior
Edit `src/comprehensive_curriculum_creator/config/agents.yaml` to customize:
- Agent roles and goals
- Backstories and expertise areas
- Tool configurations

### Adjusting Task Definitions
Edit `src/comprehensive_curriculum_creator/config/tasks.yaml` to modify:
- Task descriptions and requirements
- Expected outputs and formats
- Context dependencies between tasks

### Adding Custom Tools
Extend `src/comprehensive_curriculum_creator/tools/custom_tool.py` with:
- New research capabilities
- Content processing tools
- File organization utilities

## 📊 Example Usage

```bash
$ python -m comprehensive_curriculum_creator.main

=== Curriculum Creator - Stage 1: Parameter Collection ===
Please provide the following information for your curriculum:

Topic of education: Machine Learning Fundamentals
Duration of course (e.g., '8 weeks', '3 months'): 8 weeks
Number of sessions: 16
Duration of each session (e.g., '2 hours', '90 minutes'): 2 hours
Project Based (yes/no): yes
Audience level description: Computer Science Students

=== Stage 1: Creating Curriculum Outline ===
[Processing...]

REVIEW CHECKPOINT - YOUR APPROVAL NEEDED
[Outline displayed]

Do you approve this outline? (yes/no/revise): yes

=== Stage 2: Complete Curriculum Development ===
[Creating complete course materials...]

🎉 CURRICULUM CREATION SUCCESSFULLY COMPLETED!
Your curriculum package has been created in the ./output/ directory.
```

## 🔍 Research Capabilities

The system uses multiple research tools for comprehensive content:

- **SerperDevTool**: General web search
- **WebsiteSearchTool**: Targeted website content extraction
- **TavilySearchTool**: Advanced search with content summaries
- **GitHubSearchTool**: Code and repository research
- **ScrapeWebsiteTool**: Direct website content scraping

## 🎯 Project-Based Learning

When `project_based=yes`, the system creates:

- Real-world use cases and scenarios
- Hands-on implementation projects
- Industry-relevant applications
- Practical assessment criteria
- Step-by-step implementation guides

## 📈 Best Practices

1. **API Keys**: Set up all available API keys for best research results
2. **Review Process**: Always review Stage 1 outline before proceeding
3. **Audience Alignment**: Clearly define audience level for appropriate content
4. **Project Scope**: Ensure project-based requests align with course duration
5. **Content Validation**: Review generated materials for accuracy and completeness

## 🐛 Troubleshooting

### Common Issues

**Missing API Keys**
```bash
# Ensure OPENAI_API_KEY is set in .env
echo "OPENAI_API_KEY=your_key_here" >> .env
```

**Permission Errors**
```bash
# Ensure write permissions for output directory
chmod 755 ./output/
```

**Research Tool Failures**
- Some tools require specific API keys
- Check network connectivity for web scraping tools
- Verify API key validity and quotas

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

- 📖 [CrewAI Documentation](https://docs.crewai.com)
- 💬 [Discord Community](https://discord.com/invite/X4JWnZnxPb)
- 🐛 [GitHub Issues](https://github.com/joaomdmoura/crewai/issues)
- 📧 [CrewAI Support](https://chatg.pt/DWjSBZn)

---

**Built with ❤️ using CrewAI**
