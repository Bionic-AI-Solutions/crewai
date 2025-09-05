import os
import zipfile
from pathlib import Path
from typing import Type, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class FileOrganizerInput(BaseModel):
    """Input schema for FileOrganizerTool."""
    topic: str = Field(..., description="The main topic of the curriculum")
    content_structure: dict = Field(..., description="Dictionary containing the curriculum structure with modules, weeks, and sessions")


class FileOrganizerTool(BaseTool):
    name: str = "Curriculum File Organizer"
    description: str = "Organizes curriculum files into the specified folder structure: Topic/Module/Week/Session/Classwork & Homework folders"
    args_schema: Type[BaseModel] = FileOrganizerInput

    def _run(self, topic: str, content_structure: dict) -> str:
        """Creates the complete folder structure for the curriculum"""
        try:
            if not topic or not isinstance(topic, str):
                raise ValueError("Topic must be a non-empty string")

            if not content_structure or not isinstance(content_structure, dict):
                raise ValueError("Content structure must be a non-empty dictionary")

            # Sanitize topic name for filesystem
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_topic:
                safe_topic = "Curriculum"

            base_path = Path(f"./output/{safe_topic.replace(' ', '_')}")

            # Create base directory with error handling
            try:
                base_path.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                return f"Permission denied: Cannot create directory at {base_path}"
            except OSError as e:
                return f"OS error creating base directory: {str(e)}"

            # Create course overview folder
            overview_path = base_path / "Course_Overview_and_Guide"
            try:
                overview_path.mkdir(exist_ok=True)
            except OSError as e:
                return f"Error creating overview directory: {str(e)}"

            # Process each module
            for module_name, module_data in content_structure.items():
                try:
                    safe_module_name = "".join(c for c in str(module_name) if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    if not safe_module_name:
                        safe_module_name = f"Module_{list(content_structure.keys()).index(module_name) + 1}"

                    module_path = base_path / f"Module_{safe_module_name.replace(' ', '_')}"
                    module_path.mkdir(exist_ok=True)

                    # Validate module_data structure
                    if not isinstance(module_data, dict):
                        continue

                    # Process each week
                    for week_num, week_data in module_data.items():
                        try:
                            week_path = module_path / f"Week_{week_num}"
                            week_path.mkdir(exist_ok=True)

                            # Validate week_data structure
                            if not isinstance(week_data, dict):
                                continue

                            # Process each session
                            for session_num, session_data in week_data.items():
                                try:
                                    session_path = week_path / f"Session_{session_num}"
                                    session_path.mkdir(exist_ok=True)

                                    # Create Classwork and Homework folders
                                    classwork_path = session_path / "Classwork"
                                    homework_path = session_path / "Homework"

                                    classwork_path.mkdir(exist_ok=True)
                                    homework_path.mkdir(exist_ok=True)

                                except OSError as e:
                                    return f"Error creating session {session_num} in week {week_num}: {str(e)}"

                        except OSError as e:
                            return f"Error creating week {week_num} in module {module_name}: {str(e)}"

                except OSError as e:
                    return f"Error creating module {module_name}: {str(e)}"

            return f"Successfully created curriculum folder structure for '{topic}' at {base_path}"

        except ValueError as e:
            return f"Validation error: {str(e)}"
        except Exception as e:
            return f"Unexpected error creating folder structure: {str(e)}"


class ZipCreatorInput(BaseModel):
    """Input schema for ZipCreatorTool."""
    source_path: str = Field(..., description="Path to the folder to be zipped")
    zip_name: str = Field(..., description="Name for the output zip file (without .zip extension)")


class ZipCreatorTool(BaseTool):
    name: str = "Curriculum Zip Creator"
    description: str = "Creates a zip file from the specified curriculum folder for easy distribution"
    args_schema: Type[BaseModel] = ZipCreatorInput

    def _run(self, source_path: str, zip_name: str) -> str:
        """Creates a zip file from the source directory"""
        try:
            if not source_path or not isinstance(source_path, str):
                raise ValueError("Source path must be a non-empty string")

            if not zip_name or not isinstance(zip_name, str):
                raise ValueError("Zip name must be a non-empty string")

            source_path = Path(source_path)
            if not source_path.exists():
                return f"Source path {source_path} does not exist"

            if not source_path.is_dir():
                return f"Source path {source_path} is not a directory"

            # Sanitize zip name
            safe_zip_name = "".join(c for c in zip_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_zip_name:
                safe_zip_name = "curriculum_package"

            zip_path = Path(f"./output/{safe_zip_name}.zip")

            # Ensure output directory exists
            try:
                zip_path.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                return f"Permission denied: Cannot create output directory at {zip_path.parent}"
            except OSError as e:
                return f"Error creating output directory: {str(e)}"

            # Create zip file
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    file_count = 0
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            try:
                                # Add file to zip with relative path
                                arcname = file_path.relative_to(source_path.parent)
                                zipf.write(file_path, arcname)
                                file_count += 1
                            except OSError as e:
                                return f"Error adding file {file_path} to zip: {str(e)}"

                    if file_count == 0:
                        return f"Warning: No files found in source directory {source_path}"

            except PermissionError:
                return f"Permission denied: Cannot create zip file at {zip_path}"
            except OSError as e:
                return f"OS error creating zip file: {str(e)}"

            return f"Successfully created zip file with {file_count} files: {zip_path}"

        except ValueError as e:
            return f"Validation error: {str(e)}"
        except Exception as e:
            return f"Unexpected error creating zip file: {str(e)}"


class ContentWriterInput(BaseModel):
    """Input schema for ContentWriterTool."""
    file_path: str = Field(..., description="Path where the file should be created")
    content: str = Field(..., description="Content to write to the file")
    file_type: str = Field("md", description="File extension/type (md, txt, etc.)")


class ContentWriterTool(BaseTool):
    name: str = "Curriculum Content Writer"
    description: str = "Writes curriculum content to specific files in the organized folder structure"
    args_schema: Type[BaseModel] = ContentWriterInput

    def _run(self, file_path: str, content: str, file_type: str = "md") -> str:
        """Writes content to a file, creating directories if needed"""
        try:
            if not file_path or not isinstance(file_path, str):
                raise ValueError("File path must be a non-empty string")

            if content is None:
                raise ValueError("Content cannot be None")

            if not file_type or not isinstance(file_type, str):
                file_type = "md"

            # Validate file_type
            allowed_types = ['md', 'txt', 'html', 'json', 'yaml', 'yml']
            if file_type not in allowed_types:
                file_type = "md"

            file_path = Path(file_path)

            # Create parent directories if they don't exist
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                return f"Permission denied: Cannot create directory {file_path.parent}"
            except OSError as e:
                return f"Error creating directory {file_path.parent}: {str(e)}"

            # Add extension if not present
            if not file_path.suffix:
                file_path = file_path.with_suffix(f".{file_type}")

            # Validate file path is safe
            if ".." in str(file_path):
                return "Error: File path contains unsafe '..' components"

            # Write content to file
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(content))
            except PermissionError:
                return f"Permission denied: Cannot write to {file_path}"
            except OSError as e:
                return f"OS error writing to file: {str(e)}"
            except UnicodeEncodeError:
                # Fallback to ascii encoding if unicode fails
                try:
                    with open(file_path, 'w', encoding='ascii', errors='replace') as f:
                        f.write(str(content))
                except OSError as e:
                    return f"Error writing file with fallback encoding: {str(e)}"

            return f"Successfully wrote {len(str(content))} characters to {file_path}"

        except ValueError as e:
            return f"Validation error: {str(e)}"
        except Exception as e:
            return f"Unexpected error writing content to file: {str(e)}"
