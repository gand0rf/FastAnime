import importlib

import click


# TODO: since command structure is pretty obvious default to only requiring  mapping of command names to their function name(cause some have special names like import)
class LazyGroup(click.Group):
    def __init__(self, root: str, *args, lazy_subcommands=None, **kwargs):
        super().__init__(*args, **kwargs)
        # lazy_subcommands is a map of the form:
        #
        #   {command-name} -> {module-name}.{command-object-name}
        #
        self.root = root
        self.lazy_subcommands = lazy_subcommands or {}

    def list_commands(self, ctx):
        base = super().list_commands(ctx)
        lazy = sorted(self.lazy_subcommands.keys())
        return base + lazy

    def get_command(self, ctx, cmd_name):  # pyright:ignore
        if cmd_name in self.lazy_subcommands:
            return self._lazy_load(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _lazy_load(self, cmd_name: str):
        # lazily loading a command, first get the module name and attribute name
        import_path: str = self.lazy_subcommands[cmd_name]
        modname, cmd_object_name = import_path.rsplit(".", 1)
        # do the import
        mod = importlib.import_module(f".{modname}", package=self.root)
        # get the Command object from that module
        cmd_object = getattr(mod, cmd_object_name)
        # check the result to make debugging easier
        if not isinstance(cmd_object, click.Command):
            raise ValueError(
                f"Lazy loading of {import_path} failed by returning "
                "a non-command object"
            )
        return cmd_object
