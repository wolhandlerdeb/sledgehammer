from allennlp.data.fields import ArrayField, TextField, LabelField, MetadataField
from allennlp.data.dataset_readers import DatasetReader
from typing import *
from allennlp.data.token_indexers import TokenIndexer
from overrides import overrides
from allennlp.data.tokenizers import Token
import numpy as np
from allennlp.data import Instance
import torch

label_cols = ['accuracy']

@DatasetReader.register("classification_dataset_reader")
class ClassificationDatasetReader(DatasetReader):
    """
    Text classification dataset reader.
    """
    def __init__(self, tokenizer: Callable[[str], List[str]]=lambda x: x.split(),
                         token_indexers: Dict[str, TokenIndexer] = None,
                         max_seq_len: Optional[int]=100, testing=False) -> None:
        super().__init__(lazy=False)
        self.tokenizer = tokenizer
        self.token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}
        self.max_seq_len = max_seq_len
        self.testing=testing,
        self.label_cols = label_cols

    @overrides
    def text_to_instance(self, tokens: List[Token],
                         instance_id: int=-1,
                         labels: int=0) -> Instance:
        sentence_field = TextField(tokens, self.token_indexers)

        label_field = LabelField(labels)
        id_field = MetadataField(instance_id)

        fields = {"tokens": sentence_field, 'label': label_field, "instance_id": id_field}

        return Instance(fields)
                                                                                                            
    @overrides
    def _read(self, file_path: str) -> Iterator[Instance]:
        with open(file_path, encoding='ISO-8859-1') as ifh:
            for (i, l) in enumerate(ifh):
                fields = l.rstrip().split("\t")
                if len(fields) < 2:
                    continue
                yield self.text_to_instance(
                    [Token(x) for x in self.tokenizer(fields[1])],
                    i,
                    fields[0]
                )

