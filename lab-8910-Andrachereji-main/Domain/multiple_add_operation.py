from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class MultipleAddOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 added_entities: List[Entity]):
        self.repository = repository
        self.added_entities = added_entities

    def undo(self):
        for entity in self.added_entities:
            self.repository.delete(entity.id_entity)

    def redo(self):
        for entity in self.added_entities:
            self.repository.create(entity)
