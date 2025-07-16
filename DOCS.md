# Documentation for `charz-rust`

## Table of Contents

* [charz\_rust](#charz_rust)
  * [RustScreen](#charz_rust.RustScreen)

<a id="charz_rust"></a>

# `charz_rust`

<a id="charz_rust.RustScreen"></a>

## Class `RustScreen`

```python
class RustScreen(_Screen)
```

`RustScreen` class, partially implemented in `Rust`.

This is useful for speeding up rendering,
since rendering many nodes can be slow.

**Notes**:

  - Attribute `.buffer` is **unused** (not updated),
  and cannot be properly read.
  

**Example**:

```python
from charz import Engine
from charz_rust import RustScreen

class MyGame(Engine):
    screen = RustScreen()  # This will use faster rendering!
```

