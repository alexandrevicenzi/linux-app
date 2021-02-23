import os
import sys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gio, Gtk
from proton.constants import VERSION as proton_version
from protonvpn_nm_lib.constants import APP_VERSION as lib_version

from .constants import APP_VERSION
from .logger import logger
# from .view_model.dashboard import DashboardPresenter
from .view_model.login import LoginViewModel
# from .service.dashboard import DashboardService
# from .view.dashboard import DashboardView
from .view.login import LoginView
from protonvpn_nm_lib import protonvpn


class ProtonVPN(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id='com.protonvpn.www',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.protonvpn = protonvpn

    def do_startup(self):
        logger.info(
            "\n"
            + "---------------------"
            + "----------------"
            + "------------\n\n"
            + "-----------\t"
            + "Initialized protonvpn"
            + "\t-----------\n\n"
            + "---------------------"
            + "----------------"
            + "------------"
        )
        logger.info(
            "ProtonVPN v{} "
            "(protonvpn-nm-lib v{}; proton-client v{})".format(
                APP_VERSION, lib_version, proton_version
            )
        )
        if "SUDO_UID" in os.environ:
            logger.info("Initialized app with sudo")
            print(
                "\nRunning ProtonVPN as root is not supported and "
                "is highly discouraged, as it might introduce "
                "undesirable side-effects."
            )
            user_input = input("Are you sure that you want to proceed (y/N): ")
            user_input = user_input.lower()
            if not user_input == "y":
                logger.info("Quit app as sudo")
                self.on_quit()

        Gtk.Application.do_startup(self)

        quit_app = Gio.SimpleAction.new("quit", None)
        display_preferences = Gio.SimpleAction.new("display_preferences", None)

        quit_app.connect("activate", self.on_quit)
        display_preferences.connect("activate", self.on_display_preferences)

        self.add_action(quit_app)
        self.add_action(display_preferences)
        logger.info("Startup successful")

    def on_quit(self, *args):
        logger.info("Quit app")
        self.quit()

    def on_display_preferences(self, *args):
        logger.info("Display preferences")
        print("To-do")

    def do_activate(self):
        win = self.props.active_window

        if not win:
            if not self.protonvpn._check_session_exists():
                win = self.get_login_window
            # else:
                # win = self.get_dashboard_window

        logger.info("Default window: {}".format(win))

        win().present()

    def get_login_window(self):
        login_view_model = LoginViewModel(self.protonvpn)
        return LoginView(
            application=self,
            view_model=login_view_model,
            # dashboard_window=self.get_dashboard_window
        )

    # def get_dashboard_window(self):
    # #     dasboard_service = DashboardService(
    # #         self.reconector_manager,
    # #         self.user_conf_manager,
    # #         self.ks_manager,
    # #         self.connection_manager,
    # #         self.user_manager,
    # #         self.server_manager,
    # #         self.ipv6_lp_manager,
    # #         CertificateManager
    # #     )
    #     dashboard_presenter = DashboardPresenter(self.protonvpn)
    #     return DashboardView(
    #         application=self,
    #         presenter=dashboard_presenter
    #     )


def main():
    app = ProtonVPN()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
