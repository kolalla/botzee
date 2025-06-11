from typing import List, Set, Dict, Tuple
from random import randint
from collections import Counter
from dataclasses import dataclass


@dataclass
class DiceRoll:
    values: List[int]
    
    def __post_init__(self):
        if len(self.values) != 5:
            raise ValueError("Dice roll must contain exactly 5 dice")
        if not all(1 <= die <= 6 for die in self.values):
            raise ValueError("All dice values must be between 1 and 6")
    
    def get_counts(self) -> Dict[int, int]:
        return dict(Counter(self.values))
    
    def get_unique_values(self) -> Set[int]:
        return set(self.values)
    
    def has_n_of_a_kind(self, n: int) -> bool:
        return any(count >= n for count in self.get_counts().values())
    
    def get_highest_count(self) -> int:
        counts = self.get_counts()
        return max(counts.values()) if counts else 0
    
    def is_full_house(self) -> bool:
        counts = sorted(self.get_counts().values(), reverse=True)
        return len(counts) == 2 and counts == [3, 2]
    
    def is_small_straight(self) -> bool:
        unique_values = self.get_unique_values()
        straights = [
            {1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}
        ]
        return any(straight.issubset(unique_values) for straight in straights)
    
    def is_large_straight(self) -> bool:
        unique_values = self.get_unique_values()
        return unique_values in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
    
    def is_yahtzee(self) -> bool:
        return self.has_n_of_a_kind(5)
    
    def sum_all(self) -> int:
        return sum(self.values)
    
    def sum_of_value(self, value: int) -> int:
        return sum(die for die in self.values if die == value)


class DiceManager:
    def __init__(self):
        self.current_roll: List[int] = []
    
    def roll_all_dice(self) -> DiceRoll:
        self.current_roll = [randint(1, 6) for _ in range(5)]
        return DiceRoll(self.current_roll.copy())
    
    def reroll_dice(self, keep_indices: List[int]) -> DiceRoll:
        if not self.current_roll:
            raise ValueError("No initial roll to reroll from")
        
        if not all(0 <= idx < 5 for idx in keep_indices):
            raise ValueError("Keep indices must be between 0 and 4")
        
        new_roll = self.current_roll.copy()
        for i in range(5):
            if i not in keep_indices:
                new_roll[i] = randint(1, 6)
        
        self.current_roll = new_roll
        return DiceRoll(self.current_roll.copy())
    
    def reroll_by_value(self, keep_values: List[int]) -> DiceRoll:
        if not self.current_roll:
            raise ValueError("No initial roll to reroll from")
        
        keep_indices = []
        available_dice = self.current_roll.copy()
        
        for value in keep_values:
            try:
                idx = available_dice.index(value)
                keep_indices.append(self.current_roll.index(value, len(keep_indices)))
                available_dice[idx] = -1
            except ValueError:
                raise ValueError(f"Value {value} not found in current roll")
        
        return self.reroll_dice(keep_indices)
    
    def get_current_roll(self) -> DiceRoll:
        if not self.current_roll:
            raise ValueError("No dice have been rolled")
        return DiceRoll(self.current_roll.copy())
    
    def analyze_roll(self) -> Dict[str, any]:
        if not self.current_roll:
            return {}
        
        roll = DiceRoll(self.current_roll)
        counts = roll.get_counts()
        
        return {
            "values": self.current_roll.copy(),
            "counts": counts,
            "unique_count": len(roll.get_unique_values()),
            "highest_count": roll.get_highest_count(),
            "has_pair": roll.has_n_of_a_kind(2),
            "has_three_kind": roll.has_n_of_a_kind(3),
            "has_four_kind": roll.has_n_of_a_kind(4),
            "has_yahtzee": roll.is_yahtzee(),
            "has_full_house": roll.is_full_house(),
            "has_small_straight": roll.is_small_straight(),
            "has_large_straight": roll.is_large_straight(),
            "sum": roll.sum_all()
        }


def get_optimal_keeps_for_category(dice_roll: DiceRoll, target_category: str) -> List[int]:
    values = dice_roll.values
    counts = dice_roll.get_counts()
    
    if target_category in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
        target_value = {"ones": 1, "twos": 2, "threes": 3, "fours": 4, "fives": 5, "sixes": 6}[target_category]
        return [i for i, val in enumerate(values) if val == target_value]
    
    elif target_category == "three_of_a_kind":
        for value, count in counts.items():
            if count >= 3:
                return [i for i, val in enumerate(values) if val == value]
        for value, count in counts.items():
            if count == 2:
                return [i for i, val in enumerate(values) if val == value]
        return []
    
    elif target_category == "four_of_a_kind":
        for value, count in counts.items():
            if count >= 4:
                return [i for i, val in enumerate(values) if val == value]
        for value, count in counts.items():
            if count >= 3:
                return [i for i, val in enumerate(values) if val == value]
        for value, count in counts.items():
            if count == 2:
                return [i for i, val in enumerate(values) if val == value]
        return []
    
    elif target_category == "full_house":
        if dice_roll.is_full_house():
            return list(range(5))
        
        three_kind_value = None
        pair_value = None
        for value, count in counts.items():
            if count == 3:
                three_kind_value = value
            elif count == 2:
                pair_value = value
        
        if three_kind_value:
            return [i for i, val in enumerate(values) if val == three_kind_value]
        elif pair_value:
            return [i for i, val in enumerate(values) if val == pair_value]
        return []
    
    elif target_category == "small_straight":
        if dice_roll.is_small_straight():
            return list(range(5))
        
        target_sequences = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        unique_values = dice_roll.get_unique_values()
        
        for seq in target_sequences:
            overlap = seq.intersection(unique_values)
            if len(overlap) >= 3:
                return [i for i, val in enumerate(values) if val in overlap]
        return []
    
    elif target_category == "large_straight":
        if dice_roll.is_large_straight():
            return list(range(5))
        
        target_sequences = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
        unique_values = dice_roll.get_unique_values()
        
        for seq in target_sequences:
            overlap = seq.intersection(unique_values)
            if len(overlap) >= 4:
                return [i for i, val in enumerate(values) if val in overlap]
        return []
    
    elif target_category == "yahtzee":
        for value, count in counts.items():
            if count >= 2:
                return [i for i, val in enumerate(values) if val == value]
        return []
    
    elif target_category == "chance":
        return list(range(5))
    
    return []