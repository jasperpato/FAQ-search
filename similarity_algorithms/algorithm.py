from abc import ABC, abstractmethod
from typing import Dict
from project_types import Tokens

class SimilarityAlgorithm(ABC):
    
    @abstractmethod
    def similarity(self, in_tok : Tokens, toks_dict : Dict[int, Tokens]) -> Dict[int, float]:
        '''
        in_toks is list of tokens of the incoming query
        toks_dict is a dictionary mapping post id to its text (can be subject or payload)
        returns a dictionary mapping each post id to a similarity score between 0-1
        '''
        pass 



    