from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.app import App
from textual.widgets import ScrollView
from textual.scrollbar import ScrollTo

class UScrollView(ScrollView):
    async def handle_scroll_to(self, message: ScrollTo) -> None:
        if message.x is not None:
            self.target_x = message.x
        if message.y is not None:
            self.target_y = message.y
        self.animate("x", self.target_x, speed=1500, easing="out_cubic")
        self.animate("y", self.target_y, speed=1500, easing="out_cubic")
class CodeViewer(App):
    """An example of a very simple Textual App"""
    def __init__(self, screen: bool = True, driver_class: any = None, log: str = "", log_verbosity: int = 1, title: str = "Textual Application", **kwargs):
        
        self.content = kwargs['content']
        super().__init__(screen, driver_class, log, log_verbosity, title)
    
    async def on_load(self) -> None:

        await self.bind("q", "quit", "Quit")


    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""

        # Create our widgets
        # In this a scroll view for the code and a directory tree
        
        
        try:
            # Construct a Syntax object for the path in the message
            syntax = Syntax(
                self.content,
                lexer="HTML",
                line_numbers=True,
                word_wrap=True,
                indent_guides=True,
                theme="monokai",
            )
            self.body = UScrollView(syntax,fluid=False)
        except Exception:
            # Possibly a binary file
            # For demonstration purposes we will show the traceback
            syntax = Traceback(theme="monokai", width=None, show_locals=True)
        await self.view.dock(self.body)

# Run our app class
#CodeViewer.run(title="Code Viewer",content="123")