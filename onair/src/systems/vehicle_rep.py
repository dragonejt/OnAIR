# GSC-19165-1, "The On-Board Artificial Intelligence Research (OnAIR) Platform"
#
# Copyright © 2023 United States Government as represented by the Administrator of
# the National Aeronautics and Space Administration. No copyright is claimed in the
# United States under Title 17, U.S. Code. All Other Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19165-1 OnAIR.pdf"

"""
VehicleRepresentation Class
Handles retrieval and storage of vehicle subsystem information
"""

from .status import Status
from .telemetry_test_suite import TelemetryTestSuite

from ..util.print_io import *
from ..util.plugin_import import import_plugins

# from ..util.data_conversion import *


class VehicleRepresentation:
    def __init__(self, headers, tests, _knowledge_rep_plugins={}):
        assert len(headers) == len(tests)
        self.headers = headers
        self.knowledge_synthesis_constructs = import_plugins(
            self.headers, _knowledge_rep_plugins
        )

        self.status = Status("MISSION")
        self.test_suite = TelemetryTestSuite(headers, tests)

        self.curr_data = ["-"] * len(self.headers)  # stale data

    ##### UPDATERS #################################
    def update(self, frame):
        # Update constructs
        self.update_curr_data(frame)
        self.test_suite.execute_suite(self.curr_data)
        self.status.set_status(*self.test_suite.get_suite_status())
        self.update_constructs(self.curr_data)

    def update_constructs(self, frame):
        for construct in self.knowledge_synthesis_constructs:
            construct.update(frame)

    def update_curr_data(self, frame):
        for i in range(len(frame)):
            if frame[i] != "-":
                self.curr_data[i] = frame[i]

    ##### GETTERS AND SETTERS #####
    def get_headers(self):
        return self.headers

    def get_current_faulting_mnemonics(self):
        return self.test_suite.get_status_specific_mnemonics()

    def get_current_data(self):
        return self.curr_data

    def get_current_time(self):
        return self.curr_data[0]

    def get_status(self):
        return self.status.get_status()

    def get_bayesian_status(self):
        return self.status.get_bayesian_status()

    def get_batch_status_reports(self, batch_data):
        return

    def get_state_information(self, scope=["status"]):
        state_info = {}
        for construct in self.knowledge_synthesis_constructs:
            state_info[construct.component_name] = construct.render_reasoning()
        return state_info
