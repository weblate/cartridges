from abc import abstractmethod

from gi.repository import GObject

from src.game import Game


class Manager(GObject.Object):
    """Class in charge of handling a post creation action for games.

    * May connect to signals on the game to handle them.
    * May cancel its running tasks on critical error,
    in that case a new cancellable must be generated for new tasks to run.
    """

    run_after: set[type["Manager"]] = set()
    errors: list[Exception]
    blocking: bool = True

    def __init__(self) -> None:
        super().__init__()
        self.errors = []

    def report_error(self, error: Exception):
        """Report an error that happened in Manager.run"""
        self.errors.append(error)

    def collect_errors(self) -> list[Exception]:
        """Get the errors produced by the manager and remove them from self.errors"""
        errors = list(self.errors)
        self.errors.clear()
        return errors

    @abstractmethod
    def final_run(self, game: Game) -> None:
        """
        Abstract method overriden by final child classes, called by the run method.
        * May block its thread
        * May not raise exceptions, as they will be silently ignored
        """

    def run(self, game: Game) -> None:
        """Pass the game through the manager.
        In charge of calling the final_run method."""
        self.emit("started")
        self.final_run(game)
        self.emit("done")

    @GObject.Signal(name="started")
    def started(self) -> None:
        """Signal emitted when a manager is started"""
        pass

    @GObject.Signal(name="done")
    def done(self) -> None:
        """Signal emitted when a manager is done"""
        pass
