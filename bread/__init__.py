from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BreadRecipe:
    """A sourdough bread recipe."""
    sourdough: Optional[int] = None
    wheat: Optional[int] = None
    full_wheat: Optional[int] = None
    water: Optional[int] = None
    salt: Optional[int] = None
    total_wheat: int = field(init=False)
    total_water: int = field(init=False)
    full_wheat_percentage: float = field(init=False)
    total_weight: float = field(init=False)
    water_bp: Optional[float] = None
    salt_bp: Optional[float] = None
    
    def __post_init__(self):
        # do some sanity checks on data
        if not ((self.water is not None) ^ (self.water_bp is not None)):
            raise ValueError("Either water or water_bp needs to be set.")
        if not ((self.salt is not None) ^ (self.salt_bp is not None)):
            raise ValueError("Either salt or salt_ba needs to be set.")
        # get total wheat (for bp calc)
        self.total_wheat = self.wheat + self.full_wheat + self.sourdough * .5
        # infer bp or actual amounts
        self.full_wheat_percentage = (self.full_wheat + self.sourdough * .5) / self.total_wheat
        if self.salt is None:
            self.salt = self.total_wheat * self.salt_bp - self.total_wheat
        else:
            self.salt_bp = self.salt / self.total_wheat
        if self.water is None:
            total_water = self.total_wheat * self.water_bp - self.total_wheat
            self.water = total_water - self.sourdough * .5
        else:
            self.water_bp = (self.water + self.sourdough * .5) / self.total_wheat
        self.total_water = self.sourdough * .5 + self.water
        
        self.total_weight = self.total_water + self.total_wheat + self.salt
