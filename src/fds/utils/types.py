from pathlib import Path
from typing import Dict, List, Optional, Union

from ape.types import ABI

AbiType = Optional[Union[List[ABI], Dict, str, Path]]
