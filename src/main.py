import os
import argparse

from logging_wrapper import LoggingWrapper
from whats_new_parser import WhatsNewParser
from hsp_configs import HspConfigs
from file_system import FileSystem
from svn_commands import SvnCommands


snv_file_props = {
    "etas:confidentiality": "internal",
    "etas:owner": "XXXXXXXX",
    "etas:pm_project_nr": "10688",
    "etas:project_title": "ES820",
    "etas:review_state": "draft",
}


log = LoggingWrapper().get_logger(__name__)


# TODO - most of the argument should be exposed into a config file
def get_arguments():
    """
    Parses command line arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Metrics Collector for the Drive Recorder PAT"
    )
    parser.add_argument(
        "--sp-version",
        type=str,
        required=False,
        help="Drive Recorder Service Pack version, e.g., SP7.5.5.0.1",
    )
    parser.add_argument(
        "--metrics-destination-path",
        type=str,
        required=True,
        help="Path to the destination directory of the metrics.",
    )
    parser.add_argument(
        "--whats-new-path",
        type=str,
        default=r"\\fe00fs70.de.bosch.com\\ES715_20\\ES820\\GENESIS\\v7.5.5\\SP\\WhatsNew.html",
        help="Path to the Drive Recorder's 'What's New' HTML file.",
    )
    parser.add_argument(
        "--hsp-configs-path",
        type=str,
        default=r"C:\\ETASData\\HSP\\Configs",
        help="Path to the HSP configurations directory.",
    )
    parser.add_argument(
        "--metrics-source-path",
        type=str,
        default=r"D:\\Workspace\\TestMetrics",
        help="Path to the source directory of the metrics.",
    )
    return parser.parse_args()


def main(args):
    # Service Pack and Configurator Version
    whats_new = WhatsNewParser(args.whats_new_path, args.sp_version)
    sp_version, cfg_version = whats_new.get_service_pack_and_configurator_version()
    log.info(f"Service Pack Version: {sp_version}")
    log.info(f"Configurator Version: {cfg_version}")

    # HSP Update Tool Version
    configs = HspConfigs(args.hsp_configs_path)
    hsp_version = configs.get_hsp_version()
    log.info(f"HSP Version: {hsp_version}")

    # Metrics source
    if not os.path.exists(args.metrics_source_path):
        log.error(f"Metrics source path does not exist: {args.metrics_source_path}")
        return
    source_path = FileSystem.get_directory(args.metrics_source_path, sp_version)
    if not os.path.exists(source_path):
        log.error(f"Metrics source directory does not exist: {source_path}")
        return
    else:
        log.info(f"Metrics source directory: {source_path}")

    # Metrics destination
    # TODO expose naming format into a config file
    destination_name = "_".join(["DRVR", cfg_version, sp_version, hsp_version])
    destination_path = os.path.join(args.metrics_destination_path, destination_name)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        log.info(f"Created destination directory: {destination_path}")
    else:
        log.info(f"Destination directory already exists: {destination_path}")

    # Copy metrics
    log.info("Copying metrics...")
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
    for root, _, files in os.walk(destination_path):
        for file in files:
            file_path = os.path.join(root, file)
            SvnCommands.propset2(file_path, snv_file_props)

    # Commit SVN changes
    log.info("Committing changes to SVN repo...")
    commit_message = f"PAT metrics collected: {cfg_version} {sp_version} {hsp_version}"
    if SvnCommands.commit(destination_path, commit_message) is None:
        log.error(f"Failed to commit changes to SVN repo for {destination_path}")


if __name__ == "__main__":
    try:
        log.info("Started.")
        main(get_arguments())
        log.info("Finished.")
    except Exception as e:
        log.exception(e)
