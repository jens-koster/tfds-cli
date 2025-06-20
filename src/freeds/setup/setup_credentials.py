from pathlib import Path
from typing import Any

import freeds.setup.utils as utils
import freeds.utils.log as log

logger = log.setup_logging(__name__)


def merge_config(config_name: str, new_cfg: dict[str, Any]) -> None:
    """Load old config if exists, update with new values and save it, otherwise save the new_cfg as is."""
    old_cfg = utils.read_local_config(config_name=config_name, root_dir=Path.cwd())
    if old_cfg:
        old_cfg.update(new_cfg)
        new_cfg = old_cfg
    utils.write_local_config(config_name=config_name, data=new_cfg, root_dir=Path.cwd())
    logger.info(f"✅ Updated local config {config_name}.yaml with new credentials.")


def setup_credentials() -> bool:
    """Prompt user for credentials and save them in locals."""
    utils.log_header(title="Create credentials for airflow, S3 etc", char="-")
    utils.prompt_press_any(
        "You'll be prompted for credentials, just press enter to use default user name and an autogenerated 8 char password.\n"
        "The credentials will be readable in the config files in the 'config/locals' folder.\n"
        "Nothing in FreeDS should be exposed outside your computer, so security is not a huge concern. On the other hand, you never know. I'm human, bugs happen...\n"
    )

    airflow_cfg = utils.prompt_credential(service_desc="Airflow", default_user="freeds")
    merge_config(config_name="airflow", new_cfg=airflow_cfg)

    s3_cfg = utils.prompt_credential(service_desc="minio S3", default_user="freeds")
    merge_config(config_name="s3", new_cfg=s3_cfg)
    merge_config(config_name="minio", new_cfg=s3_cfg)

    postgres_cfg = utils.prompt_credential(service_desc="PostgreSQL", default_user="freeds")
    merge_config(config_name="postgres", new_cfg=postgres_cfg)
    utils.log_header(title="🟢 Credentials setup completed successfully 🌟", char=" ")
    return True


# if __name__ == '__main__':

#     setup_credentials()
