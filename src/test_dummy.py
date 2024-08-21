# pyre-strict
from typing import List, Any

def unannotated() -> List:        # Error: missing return annotation
    return b"" + ""       # Error: function body *is* checked

def annotated() -> List[Any]:  # Error: implicit `Any` for generic parameter to `List`
    any = unannotated()
    any.attribute         # Note: the type of `any` is still any.
    return None              # Error: returning `int` but expecting `List`