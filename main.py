from importlib import metadata

import click
from iso639 import Language, LanguageNotFoundError
from loguru import logger
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
)

from repo_agent.chat_with_repo import main as run_chat_with_repo
from repo_agent.config_manager import write_config
from repo_agent.doc_meta_info import DocItem, MetaInfo
from repo_agent.log import logger, set_logger_level_from_config
from repo_agent.runner import Runner, delete_fake_files
from repo_agent.settings import (
    ChatCompletionSettings,
    LogLevel,
    ProjectSettings,
    Setting,
    setting,
)
from repo_agent.utils.meta_info_utils import delete_fake_files, make_fake_files

# 尝试获取版本号，如果失败，则使用默认版本号。
try:
    version_number = metadata.version("repoagent")
except metadata.PackageNotFoundError:
    version_number = "0.0.0"

project_settings_default_instance = ProjectSettings()
chat_completion_default_instance = ChatCompletionSettings()


def run(
    model,
    temperature,
    request_timeout,
    base_url,
    target_repo_path,
    hierarchy_path,
    markdown_docs_path,
    ignore_list,
    language,
    log_level,
):
    """Run the program with the specified parameters."""

    project_settings = ProjectSettings(
        target_repo=target_repo_path,
        hierarchy_name=hierarchy_path,
        markdown_docs_name=markdown_docs_path,
        ignore_list=list(ignore_list),  # convert tuple from 'multiple' option to list
        language=language,
        log_level=log_level,
    )

    chat_completion_settings = ChatCompletionSettings(
        model=model,
        temperature=temperature,
        request_timeout=request_timeout,
        base_url=base_url,
    )

    settings = Setting(project=project_settings, chat_completion=chat_completion_settings)
    write_config(settings.model_dump())
    set_logger_level_from_config(log_level=setting.project.log_level)

    runner = Runner()
    runner.run()
    logger.success("Documentation task completed.")


run(
    "gpt-3.5-turbo",
    0.2,
    60.0,
    "http://142.171.49.217:8660/v1",
    "D:\\Code\\LLM-EAE",
    ".project_doc_record",
    "markdown_docs",
    [],
    "Chinese",
    "INFO",
)
