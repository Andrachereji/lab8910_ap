from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class UpdateGarantieOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 update_entities: List[Entity],
                 entities: List[Entity]):
        self.repository = repository
        self.updated_entities = update_entities
        self.entities = entities

    def undo(self):
        for update_entity in self.updated_entities:
            self.repository.delete(update_entity.id_entity)
        for entity in self.entities:
            self.repository.create(entity)

    def redo(self):
        for entity in self.entities:
            self.repository.delete(entity.id_entity)
        for update_entity in self.updated_entities:
            self.repository.create(update_entity)
