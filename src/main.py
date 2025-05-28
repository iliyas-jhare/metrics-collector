import os
import argparse

import logging_wrapper
import whats_new_reader
import hsp_configs
import file_system

log = logging_wrapper.LoggingWrapper().get_logger(__name__)


# TODO - most of the argument should be exposed into a config file
def get_arguments():
    """
    Parses command line arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Metrics Collector for the Drive Recorder"
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
    parser.add_argument(
        "--metrics-destination-path",
        type=str,
        required=True,
        help="Path to the destination directory of the metrics.",
    )
    return parser.parse_args()


def main(args):
    log.info("Started.")

    # Service Pack and Configurator Version
    whats_new = whats_new_reader.WhatsNewReader(args.whats_new_path)
    sp_version, cfg_version = whats_new.get_service_pack_and_configurator_version()
    log.info(f"Service Pack Version: {sp_version}")
    log.info(f"Configurator Version: {cfg_version}")

    # HSP Update Tool Version
    configs = hsp_configs.HspConfigs(args.hsp_configs_path)
    hsp_version = configs.get_hsp_version()
    log.info(f"HSP Version: {hsp_version}")

    # Metrics source
    if not os.path.exists(args.metrics_source_path):
        log.error(f"Metrics source path does not exist: {args.metrics_source_path}")
        return
    source_path = file_system.FileSystem.get_directory(
        args.metrics_source_path, sp_version
    )
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
    file_system.FileSystem.copytree(
        src=source_path, dst=destination_path, dirs_exist_ok=True
    )

    # TODO add to SVN
    # TODO import SVN props for all the metrics
    # TODO commit to SVN

    log.info("Finshed.")


if __name__ == "__main__":
    try:
        main(get_arguments())
    except Exception as e:
        log.exception(e)
