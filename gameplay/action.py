class Action(object):
    """An action to perfom on board."""

    def __init__(self, name, *args, **kwargs):
        """Create an action."""
        self._name = name       # Name of action
        self._args = args       # Arguments to perfom action
        self._kwargs = kwargs   # Key arguments to perfom action
        self._ukwargs = None    # Key arguments to undo action

    def apply(self, board):
        """Apply action on board.

        It catch board._rev_<action_name> method and call it with
        <action_kwargs>.
        """
        method = getattr(board, "_rev_" + self._name)
        self._ukwargs = method(*self._args, **self._kwargs)

    def unapply(self, board):
        """Unapply action on board.

        It catch board._undo_<action_name> method and call it with
        <action_ukwargs>.
        """
        method = getattr(board, "_undo_" + self._name)
        method(**self._ukwargs)
        self._ukwargs = None


class ActionBatch(list):
    """A batch of actions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def apply(self, board):
        """Apply all actions in list order."""
        for action in self:
            action.apply(board)

    def unapply(self, board):
        """Unapply all action in reversed list order."""
        for action in reversed(self):
            action.unapply(board)
