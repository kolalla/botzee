from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


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


@dataclass
class RollResult:
    dice: List[int]
    roll_number: int
    can_reroll: bool


class GameState:
    def __init__(self):
        self.scorecard: Dict[ScoreCategory, Optional[int]] = {
            category: None for category in ScoreCategory
        }
        self.current_dice: List[int] = []
        self.current_roll: int = 0
        self.max_rolls_per_turn: int = 3
        self.yahtzee_bonuses: int = 0
        self.game_complete: bool = False
        self.turn_complete: bool = True
    
    def start_turn(self) -> None:
        self.current_dice = []
        self.current_roll = 0
        self.turn_complete = False
    
    def roll_dice(self, keep_dice: Optional[List[int]] = None) -> RollResult:
        if self.turn_complete:
            raise ValueError("Cannot roll dice - turn is complete")
        if self.current_roll >= self.max_rolls_per_turn:
            raise ValueError("Maximum rolls per turn exceeded")
        
        from random import randint
        
        if keep_dice is None:
            keep_dice = []
        
        if self.current_roll == 0:
            self.current_dice = [randint(1, 6) for _ in range(5)]
        else:
            if len(keep_dice) > 5:
                raise ValueError("Cannot keep more than 5 dice")
            
            new_dice = self.current_dice.copy()
            dice_to_reroll = 5 - len(keep_dice)
            
            keep_positions = set()
            for die_value in keep_dice:
                for i, current_die in enumerate(new_dice):
                    if current_die == die_value and i not in keep_positions:
                        keep_positions.add(i)
                        break
            
            positions_to_reroll = [i for i in range(5) if i not in keep_positions][:dice_to_reroll]
            
            for pos in positions_to_reroll:
                new_dice[pos] = randint(1, 6)
            
            self.current_dice = new_dice
        
        self.current_roll += 1
        can_reroll = self.current_roll < self.max_rolls_per_turn
        
        return RollResult(
            dice=self.current_dice.copy(),
            roll_number=self.current_roll,
            can_reroll=can_reroll
        )
    
    def score_turn(self, category: ScoreCategory) -> int:
        if self.turn_complete:
            raise ValueError("Turn is already complete")
        if self.scorecard[category] is not None:
            raise ValueError(f"Category {category.value} already scored")
        if not self.current_dice:
            raise ValueError("No dice rolled")
        
        score = self._calculate_score(category, self.current_dice)
        
        if category == ScoreCategory.YAHTZEE and score == 50 and self.scorecard[ScoreCategory.YAHTZEE] is not None:
            self.yahtzee_bonuses += 1
            score = 100
        
        self.scorecard[category] = score
        self.turn_complete = True
        
        if all(score is not None for score in self.scorecard.values()):
            self.game_complete = True
        
        return score
    
    def get_possible_scores(self) -> Dict[ScoreCategory, int]:
        if not self.current_dice:
            return {}
        
        possible_scores = {}
        for category in ScoreCategory:
            if self.scorecard[category] is None:
                possible_scores[category] = self._calculate_score(category, self.current_dice)
        
        return possible_scores
    
    def _calculate_score(self, category: ScoreCategory, dice: List[int]) -> int:
        if len(dice) != 5:
            return 0
        
        dice_counts = {i: dice.count(i) for i in range(1, 7)}
        
        if category in [ScoreCategory.ONES, ScoreCategory.TWOS, ScoreCategory.THREES,
                       ScoreCategory.FOURS, ScoreCategory.FIVES, ScoreCategory.SIXES]:
            target_num = {
                ScoreCategory.ONES: 1, ScoreCategory.TWOS: 2, ScoreCategory.THREES: 3,
                ScoreCategory.FOURS: 4, ScoreCategory.FIVES: 5, ScoreCategory.SIXES: 6
            }[category]
            return dice_counts[target_num] * target_num
        
        elif category == ScoreCategory.THREE_OF_A_KIND:
            if any(count >= 3 for count in dice_counts.values()):
                return sum(dice)
            return 0
        
        elif category == ScoreCategory.FOUR_OF_A_KIND:
            if any(count >= 4 for count in dice_counts.values()):
                return sum(dice)
            return 0
        
        elif category == ScoreCategory.FULL_HOUSE:
            counts = sorted(dice_counts.values(), reverse=True)
            if counts[0] == 3 and counts[1] == 2:
                return 25
            return 0
        
        elif category == ScoreCategory.SMALL_STRAIGHT:
            straights = [
                {1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}
            ]
            dice_set = set(dice)
            if any(straight.issubset(dice_set) for straight in straights):
                return 30
            return 0
        
        elif category == ScoreCategory.LARGE_STRAIGHT:
            dice_set = set(dice)
            if dice_set in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
                return 40
            return 0
        
        elif category == ScoreCategory.YAHTZEE:
            if any(count == 5 for count in dice_counts.values()):
                return 50
            return 0
        
        elif category == ScoreCategory.CHANCE:
            return sum(dice)
        
        return 0
    
    def get_upper_section_total(self) -> int:
        upper_categories = [
            ScoreCategory.ONES, ScoreCategory.TWOS, ScoreCategory.THREES,
            ScoreCategory.FOURS, ScoreCategory.FIVES, ScoreCategory.SIXES
        ]
        total = sum(self.scorecard[cat] or 0 for cat in upper_categories)
        return total
    
    def get_upper_section_bonus(self) -> int:
        return 35 if self.get_upper_section_total() >= 63 else 0
    
    def get_lower_section_total(self) -> int:
        lower_categories = [
            ScoreCategory.THREE_OF_A_KIND, ScoreCategory.FOUR_OF_A_KIND,
            ScoreCategory.FULL_HOUSE, ScoreCategory.SMALL_STRAIGHT,
            ScoreCategory.LARGE_STRAIGHT, ScoreCategory.YAHTZEE, ScoreCategory.CHANCE
        ]
        return sum(self.scorecard[cat] or 0 for cat in lower_categories)
    
    def get_total_score(self) -> int:
        upper_total = self.get_upper_section_total()
        upper_bonus = self.get_upper_section_bonus()
        lower_total = self.get_lower_section_total()
        yahtzee_bonus_total = self.yahtzee_bonuses * 100
        
        return upper_total + upper_bonus + lower_total + yahtzee_bonus_total
    
    def get_available_categories(self) -> List[ScoreCategory]:
        return [cat for cat, score in self.scorecard.items() if score is None]
    
    def is_game_complete(self) -> bool:
        return self.game_complete
    
    def can_roll(self) -> bool:
        return not self.turn_complete and self.current_roll < self.max_rolls_per_turn