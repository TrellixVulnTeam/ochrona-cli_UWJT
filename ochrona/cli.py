#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ochrona-cli
:author: ascott
"""

import sys
import click

from ochrona.config import OchronaConfig
from ochrona.exceptions import OchronaException, OchronaAPIException
from ochrona.file_handler import rfind_all_dependencies_files, parse_to_payload
from ochrona.logger import OchronaLogger
from ochrona.reporter import OchronaReporter
from ochrona.rest_client import OchronaAPIClient


@click.command()
@click.option("--api_key", help="Ochrona API Key (https://ochrona.dev).")
@click.option(
    "--dir",
    help="Directory to recursively search for dependencies files.",
    type=click.Path(exists=True),
)
@click.option("--file", "-r", help="Dependency file to use.", type=click.File("r"))
@click.option("--debug", help="Enable debug logging.", default=False, is_flag=True)
@click.option("--silent", help="Silent mode.", default=False, is_flag=True)
@click.option(
    "--report_type",
    help=f"The report type that's desired. Options ({OchronaConfig.REPORT_OPTIONS}",
    default="BASIC",
)
@click.option(
    "--output", help=f"Location for report output", type=click.Path(exists=True)
)
@click.option(
    "--exit",
    help="Exit with Code 0 regardless of vulnerability findings.",
    default=False,
    is_flag=True,
)
@click.option("--ignore", help="Ignore vulnerabilities by CVE or package name.")
def run(api_key, dir, file, debug, silent, report_type, output, exit, ignore):
    config = OchronaConfig(
        api_key=api_key,
        dir=dir,
        file=file,
        debug=debug,
        silent=silent,
        report_type=report_type,
        report_location=output,
        exit=exit,
        ignore=ignore,
    )
    log = OchronaLogger(config)
    client = OchronaAPIClient(log, config)
    reporter = OchronaReporter(log, config)
    if not config.silent:
        log.header()

    files = rfind_all_dependencies_files(log, config.dir, config.file)

    try:
        reporter.report_collector(
            files, [client.analyze(parse_to_payload(log, file)) for file in files]
        )
    except OchronaAPIException as ex:
        OchronaLogger.error(ex)
        sys.exit(-1)


if __name__ == "__main__":
    try:
        run()
    except OchronaException as ex:
        OchronaLogger.error(ex)
        sys.exit(1)
