from typing import TYPE_CHECKING
import sentry_sdk

from sentry_sdk.integrations import DidNotEnable, Integration

try:
    from openfeature import api
    from openfeature.hook import Hook

    if TYPE_CHECKING:
        from openfeature.flag_evaluation import FlagEvaluationDetails
        from openfeature.hook import HookContext, HookHints
except ImportError:
    raise DidNotEnable("OpenFeature is not installed")


class OpenFeatureIntegration(Integration):
    identifier = "openfeature"

    @staticmethod
    def setup_once():
        # type: () -> None
        # Register the hook within the global openfeature hooks list.
        api.add_hooks(hooks=[OpenFeatureHook()])


class OpenFeatureHook(Hook):

    def after(self, hook_context, details, hints):
        # type: (HookContext, FlagEvaluationDetails[bool], HookHints) -> None
        if isinstance(details.value, bool):
            flags = sentry_sdk.get_current_scope().flags
            flags.set(details.flag_key, details.value)

    def error(self, hook_context, exception, hints):
        # type: (HookContext, Exception, HookHints) -> None
        if isinstance(hook_context.default_value, bool):
            flags = sentry_sdk.get_current_scope().flags
            flags.set(hook_context.flag_key, hook_context.default_value)