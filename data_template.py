from dataclasses import dataclass
from typing import Optional

@dataclass
class Data:
    uuid_list: list
    id_list: list
    link_list: Optional[list]
    img_list: Optional[list]

@dataclass
class LegoData(Data):
    name_list: list
    date_list: list
    creator_list: list
    num_supporters_list: list
    num_days_remaining_list: list

@dataclass
class CollocationsData(Data):
    adj_rank_word_frequency: list
    adj_phrases: list
    verb_rank_word_frequency: list
    infinitive_verb: list
    verb_phrases: list