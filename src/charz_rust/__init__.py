from colex import RESET as _RESET
from charz import (
    Screen as _Screen,
    Scene as _Scene,
    Camera as _Camera,
    Texture as _Texture,
)
from charz._screen import CursorCode as _CursorCode
from charz._scene import Group as _Group

from .charz_rust import (
    __doc__,
    render_all as _render_all,
)


__all__ = ["RustScreen"]


class RustScreen(_Screen):
    def refresh(self) -> None:
        centering_x = 0
        centering_y = 0
        if _Camera.current.mode & _Camera.MODE_CENTERED:
            (centering_x, centering_y) = self.get_actual_size() // 2
        camera_parent = _Camera.current.parent
        if _Camera.current.mode & _Camera.MODE_INCLUDE_SIZE:
            if isinstance(camera_parent, _Texture):
                (texture_size_x, texture_size_y) = camera_parent.texture_size
                centering_x -= texture_size_x / 2
                centering_y -= texture_size_y / 2

        out = _render_all(
            self,
            tuple(_Scene.current.groups[_Group.TEXTURE]),
            _Camera.current,
            centering_x,
            centering_y,
        )
        self.show(out)

    def show(self, out: str) -> None:
        actual_size = self.get_actual_size()
        # construct frame
        if self.is_using_ansi():
            out += _RESET
            cursor_move_code = f"\x1b[{actual_size.y - 1}A" + "\r"
            out += cursor_move_code
        # write and flush
        self.stream.write(out)
        self.stream.flush()

    def on_cleanup(self) -> None:
        if self.hide_cursor and self.is_using_ansi():
            self.stream.write(_CursorCode.SHOW)
            self.stream.flush()
        if self.final_clear:
            old_fill = self.transparency_fill
            self.transparency_fill = " "
            self.clear()
            out = _render_all(
                self,
                [],
                _Camera.current,
                0,
                0,
            )
            self.show(out)
            self.transparency_fill = old_fill
