from dataclasses import dataclass, field
from typing import Dict, Optional, Any

@dataclass
class AppState:
    rag_system: Optional[Any] = None
    doc_processor: Optional[Any] = None
    document_store: Dict[str, Dict] = field(default_factory = dict)
