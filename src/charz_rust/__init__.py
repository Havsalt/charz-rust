from charz_rust._core import (
    __doc__,
    render_all as _render_all,
)


from colex import RESET as _ANSI_RESET_CODE
from charz import (
    Vec2 as _Vec2,
    Screen as _Screen,
    Scene as _Scene,
    Group as _Group,
    Camera as _Camera,
    TextureComponent as _TextureComponent,
)
from charz._screen import CursorCode as _CursorCode


__all__ = ["RustScreen"]


class RustScreen(_Screen):
    """`RustScreen` class, partially implemented in `Rust`.

    This is useful for speeding up rendering,
    since rendering many nodes can be slow.

    Note:
        - Attribute `.buffer` is **unused** (not updated),
          and cannot be properly read.

    Example:
    ```python
    from charz import Engine
    from charz_rust import RustScreen

    class MyGame(Engine):
        screen = RustScreen()  # This will use faster rendering!
    ```
    """

    #: Have `Rust` skip rendering to #Screen.buffer,
    #: and instead compute and render the frame.
    _single_line_buffer: str = ""

    def refresh(self) -> None:
        centering = _Vec2.ZERO
        if _Camera.current.mode & _Camera.MODE_CENTERED:
            centering = self.get_actual_size() // 2
        camera_parent = _Camera.current.parent
        if _Camera.current.mode & _Camera.MODE_INCLUDE_SIZE:
            if isinstance(camera_parent, _TextureComponent):
                centering -= camera_parent.get_texture_size() / 2
        # Have Rust compute screen buffer and concatinate output into a single line
        self._single_line_buffer = _render_all(
            self,
            tuple(_Scene.current.groups[_Group.TEXTURE]),
            _Camera.current,
            centering.x,
            centering.y,
        )
        self.show()

    def show(self) -> None:
        actual_size = self.get_actual_size()
        # Construct frame
        out = self._single_line_buffer
        if self.is_using_ansi():
            out += _ANSI_RESET_CODE
            cursor_move_code = f"\x1b[{actual_size.y - 1}A" + "\r"
            out += cursor_move_code
        # Write and flush
        self.stream.write(out)
        self.stream.flush()

    def on_cleanup(self) -> None:
        if self.hide_cursor and self.is_using_ansi():
            self.stream.write(_CursorCode.SHOW)
            self.stream.flush()
        if self.final_clear:
            old_fill = self.transparency_fill
            self.transparency_fill = " "
            self.reset_buffer()
            self._single_line_buffer = _render_all(
                self,
                [],
                _Camera.current,
                0,
                0,
            )
            self.show()
            self.transparency_fill = old_fill
