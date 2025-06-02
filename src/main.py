import os
import argparse

from anyio import run

from logging_wrapper import LoggingWrapper
from config import Config
from whats_new_parser import WhatsNewParser
from hsp_configs import HspConfigs
from file_system import FileSystem
from svn_commands import SvnCommands


log = LoggingWrapper().get_logger(__name__)


def get_arguments():
    """
    Parses command line arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Metrics Collector for the Drive Recorder PAT"
    )
    parser.add_argument(
        "--config-path",
        type=str,
        default="config.json",
        help="Path to the tool configuration file.",
    )
    parser.add_argument(
        "--sp-version",
        type=str,
        help="Drive Recorder Service Pack version. If not provided, it will be the latest from the 'What's New' file.",
    )
    parser.add_argument(
        "--commit-msg",
        type=str,
        default="Add test metrics",
        help="Commit message for the SVN repo.",
    )
    return parser.parse_args()


async def main(args):
    # Load configuration
    config = await Config.load_json(args.config_path)

    # Service Pack and Configurator Version
    whats_new = WhatsNewParser(
        config.DriveRecorderWhatsNewPath,
        args.sp_version,
        config.ServicePackNamingStyle,
        config.ConfiguratorNamingStyle,
    )
    (
        sp_version,
        cfg_version,
    ) = await whats_new.get_service_pack_and_configurator_version()
    log.info(f"Service Pack Version: {sp_version}")
    log.info(f"Configurator Version: {cfg_version}")

    # HSP Update Tool Version
    configs = HspConfigs(config.HspConfigsPath, config.HSPNamingStyle)
    hsp_version = configs.get_hsp_version()
    log.info(f"HSP Version: {hsp_version}")

    # Metrics source
    if not os.path.exists(config.TestMetricsSourcePath):
        log.error(
            f"Test metrics source path does not exist: {config.TestMetricsSourcePath}"
        )
        return
    source_path = FileSystem.get_directory(config.TestMetricsSourcePath, sp_version)
    if not os.path.exists(source_path):
        log.error(f"Test metrics source directory does not exist: {source_path}")
        return
    else:
        log.info(f"Test metrics source directory: {source_path}")

    # Metrics destination
    destination_name = (
        config.MetricsDirectoryNamingStyle.replace("${CFG_VERSION}", cfg_version)
        .replace("${SP_VERSION}", sp_version)
        .replace("${HSP_VERSION}", hsp_version)
    )
    destination_path = os.path.join(config.TestMetricsDestinationPath, destination_name)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        log.info(f"Created destination directory: {destination_path}")
    else:
        log.info(f"Destination directory already exists: {destination_path}")

    # Copy metrics
    log.info("Copying test metrics...")
    if (
        FileSystem.copytree(src=source_path, dst=destination_path, dirs_exist_ok=True)
        is None
    ):
        log.error(f"Failed to copy metrics from {source_path} to {destination_path}")
        return

    # Add metrics to SVN repo
    log.info("Adding metrics to SVN repo...")
    if SvnCommands.add(destination_path) is None:
        log.error(f"Failed to add {destination_path} to SVN repo")
        return

    # Set SVN file properties
    log.info("Setting SVN file properties...")
    file_props = Config.get_svn_file_properties(config)
    for root, _, files in os.walk(destination_path):
        for file in files:
            file_path = os.path.join(root, file)
            SvnCommands.propset2(file_path, file_props)

    # Commit SVN changes
    log.info("Committing changes to SVN repo...")
    msg = (
        args.commit_msg
        if args.commit_msg
        else f"{args.commit_msg}: {cfg_version} {sp_version} {hsp_version}"
    )
    if SvnCommands.commit(destination_path, msg) is None:
        log.error(f"Failed to commit changes to SVN repo for {destination_path}")


if __name__ == "__main__":
    try:
        log.info("Started.")
        run(main, get_arguments())
        log.info("Finished.")
    except Exception as e:
        log.exception(e)
