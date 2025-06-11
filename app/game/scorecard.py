from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from .dice import DiceRoll


class ScoreCategory(Enum):
    ONES = "ones"
    TWOS = "twos"
    THREES = "threes"
    FOURS = "fours"
    FIVES = "fives"
    SIXES = "sixes"
    THREE_OF_A_KIND = "three_of_a_kind"
    FOUR_OF_A_KIND = "four_of_a_kind"
    FULL_HOUSE = "full_house"
    SMALL_STRAIGHT = "small_straight"
    LARGE_STRAIGHT = "large_straight"
    YAHTZEE = "yahtzee"
    CHANCE = "chance"

    @classmethod
    def upper_section(cls) -> List['ScoreCategory']:
        return [cls.ONES, cls.TWOS, cls.THREES, cls.FOURS, cls.FIVES, cls.SIXES]
    
    @classmethod
    def lower_section(cls) -> List['ScoreCategory']:
        return [cls.THREE_OF_A_KIND, cls.FOUR_OF_A_KIND, cls.FULL_HOUSE,
                cls.SMALL_STRAIGHT, cls.LARGE_STRAIGHT, cls.YAHTZEE, cls.CHANCE]


@dataclass
class ScoreEntry:
    category: ScoreCategory
    score: int
    dice_used: List[int]
    is_bonus: bool = False


class ScoreCalculator:
    @staticmethod
    def calculate_score(category: ScoreCategory, dice_roll: DiceRoll) -> int:
        dice = dice_roll.values
        counts = dice_roll.get_counts()
        
        if category in ScoreCategory.upper_section():
            target_value = {
                ScoreCategory.ONES: 1, ScoreCategory.TWOS: 2, ScoreCategory.THREES: 3,
                ScoreCategory.FOURS: 4, ScoreCategory.FIVES: 5, ScoreCategory.SIXES: 6
            }[category]
            return dice_roll.sum_of_value(target_value)
        
        elif category == ScoreCategory.THREE_OF_A_KIND:
            return dice_roll.sum_all() if dice_roll.has_n_of_a_kind(3) else 0
        
        elif category == ScoreCategory.FOUR_OF_A_KIND:
            return dice_roll.sum_all() if dice_roll.has_n_of_a_kind(4) else 0
        
        elif category == ScoreCategory.FULL_HOUSE:
            return 25 if dice_roll.is_full_house() else 0
        
        elif category == ScoreCategory.SMALL_STRAIGHT:
            return 30 if dice_roll.is_small_straight() else 0
        
        elif category == ScoreCategory.LARGE_STRAIGHT:
            return 40 if dice_roll.is_large_straight() else 0
        
        elif category == ScoreCategory.YAHTZEE:
            return 50 if dice_roll.is_yahtzee() else 0
        
        elif category == ScoreCategory.CHANCE:
            return dice_roll.sum_all()
        
        return 0
    
    @staticmethod
    def get_all_possible_scores(dice_roll: DiceRoll) -> Dict[ScoreCategory, int]:
        return {
            category: ScoreCalculator.calculate_score(category, dice_roll)
            for category in ScoreCategory
        }


class Scorecard:
    def __init__(self):
        self.scores: Dict[ScoreCategory, Optional[int]] = {
            category: None for category in ScoreCategory
        }
        self.score_entries: List[ScoreEntry] = []
        self.yahtzee_bonuses: int = 0
        self.upper_section_bonus_earned: bool = False
    
    def is_category_available(self, category: ScoreCategory) -> bool:
        return self.scores[category] is None
    
    def get_available_categories(self) -> List[ScoreCategory]:
        return [cat for cat, score in self.scores.items() if score is None]
    
    def score_category(self, category: ScoreCategory, dice_roll: DiceRoll) -> int:
        if not self.is_category_available(category):
            raise ValueError(f"Category {category.value} is already scored")
        
        base_score = ScoreCalculator.calculate_score(category, dice_roll)
        
        if category == ScoreCategory.YAHTZEE and dice_roll.is_yahtzee():
            if self.scores[ScoreCategory.YAHTZEE] is not None:
                self.yahtzee_bonuses += 1
                bonus_entry = ScoreEntry(
                    category=ScoreCategory.YAHTZEE,
                    score=100,
                    dice_used=dice_roll.values.copy(),
                    is_bonus=True
                )
                self.score_entries.append(bonus_entry)
                return 100
        
        self.scores[category] = base_score
        entry = ScoreEntry(
            category=category,
            score=base_score,
            dice_used=dice_roll.values.copy()
        )
        self.score_entries.append(entry)
        
        return base_score
    
    def get_upper_section_total(self) -> int:
        return sum(
            self.scores[cat] or 0 
            for cat in ScoreCategory.upper_section()
        )
    
    def get_upper_section_bonus(self) -> int:
        upper_total = self.get_upper_section_total()
        if upper_total >= 63:
            self.upper_section_bonus_earned = True
            return 35
        return 0
    
    def get_lower_section_total(self) -> int:
        return sum(
            self.scores[cat] or 0 
            for cat in ScoreCategory.lower_section()
        )
    
    def get_yahtzee_bonus_total(self) -> int:
        return self.yahtzee_bonuses * 100
    
    def get_grand_total(self) -> int:
        upper_total = self.get_upper_section_total()
        upper_bonus = self.get_upper_section_bonus()
        lower_total = self.get_lower_section_total()
        yahtzee_bonus_total = self.get_yahtzee_bonus_total()
        
        return upper_total + upper_bonus + lower_total + yahtzee_bonus_total
    
    def is_complete(self) -> bool:
        return all(score is not None for score in self.scores.values())
    
    def get_score_breakdown(self) -> Dict[str, int]:
        return {
            "upper_section": self.get_upper_section_total(),
            "upper_bonus": self.get_upper_section_bonus(),
            "lower_section": self.get_lower_section_total(),
            "yahtzee_bonuses": self.get_yahtzee_bonus_total(),
            "grand_total": self.get_grand_total()
        }
    
    def get_category_score(self, category: ScoreCategory) -> Optional[int]:
        return self.scores[category]
    
    def get_expected_value_analysis(self, dice_roll: DiceRoll) -> Dict[ScoreCategory, Dict[str, any]]:
        analysis = {}
        possible_scores = ScoreCalculator.get_all_possible_scores(dice_roll)
        
        for category in self.get_available_categories():
            current_score = possible_scores[category]
            
            if category in ScoreCategory.upper_section():
                target_value = {
                    ScoreCategory.ONES: 1, ScoreCategory.TWOS: 2, ScoreCategory.THREES: 3,
                    ScoreCategory.FOURS: 4, ScoreCategory.FIVES: 5, ScoreCategory.SIXES: 6
                }[category]
                max_possible = target_value * 5
                efficiency = (current_score / max_possible) * 100 if max_possible > 0 else 0
            else:
                max_possible = {
                    ScoreCategory.THREE_OF_A_KIND: 30, ScoreCategory.FOUR_OF_A_KIND: 30,
                    ScoreCategory.FULL_HOUSE: 25, ScoreCategory.SMALL_STRAIGHT: 30,
                    ScoreCategory.LARGE_STRAIGHT: 40, ScoreCategory.YAHTZEE: 50,
                    ScoreCategory.CHANCE: 30
                }[category]
                efficiency = (current_score / max_possible) * 100 if max_possible > 0 else 0
            
            analysis[category] = {
                "score": current_score,
                "max_possible": max_possible,
                "efficiency_percent": round(efficiency, 1),
                "is_optimal": current_score == max_possible
            }
        
        return analysis
    
    def get_upper_section_progress(self) -> Dict[str, any]:
        current_total = self.get_upper_section_total()
        needed_for_bonus = max(0, 63 - current_total)
        available_categories = [cat for cat in ScoreCategory.upper_section() 
                              if self.is_category_available(cat)]
        
        return {
            "current_total": current_total,
            "needed_for_bonus": needed_for_bonus,
            "bonus_achievable": len(available_categories) > 0 and needed_for_bonus <= len(available_categories) * 5,
            "available_categories": available_categories,
            "progress_percent": round((current_total / 63) * 100, 1)
        }
    
    def to_dict(self) -> Dict[str, any]:
        return {
            "scores": {cat.value: score for cat, score in self.scores.items()},
            "yahtzee_bonuses": self.yahtzee_bonuses,
            "upper_section_bonus_earned": self.upper_section_bonus_earned,
            "breakdown": self.get_score_breakdown(),
            "is_complete": self.is_complete(),
            "entries": [
                {
                    "category": entry.category.value,
                    "score": entry.score,
                    "dice": entry.dice_used,
                    "is_bonus": entry.is_bonus
                }
                for entry in self.score_entries
            ]
        }