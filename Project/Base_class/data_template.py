from dataclasses import dataclass
from dataclasses_json import dataclass_json
#from typing import Optional


@dataclass
class Data:
    uuid_list: list
    id_list: list


@dataclass
class LegoData(Data):
    link_list: list
    img_list: list
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