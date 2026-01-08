from loguru import logger as log

from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport

from .actions.DebugAction import DebugAction


class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__(use_legacy_locale=False)
        log.debug("Initializing Debug Tools Plugin")
        self.name = "Debug Tools"
        self.description = "A set of debugging tools"
        self.version = "1.0.0"
        self.author = "ImDevinc"
        self.lm = self.locale_manager
        self.lm.set_to_os_default()
        self._register_actions()
        self.register(
            plugin_name=self.plugin_name,
            github_repo="https://github.com/ImDevinC/StreamControllerDebugPlugin",
            plugin_version=self.version
        )

    def _register_actions(self):
        log.debug("Registering Debug Actions")
        profile = ActionHolder(
            plugin_base=self,
            action_base=DebugAction,
            action_id_suffix="Profile",
            action_name="Profiler"
        )
        self.add_action_holder(profile)
        log.debug("Debug Actions registered successfully")
