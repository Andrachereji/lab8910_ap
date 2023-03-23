from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class UpdateOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 updated_entity: Entity,
                 entity: Entity):
        self.repository = repository
        self.updated_entity = updated_entity
        self.entity = entity

    def undo(self):
        self.repository.delete(self.updated_entity.id_entity)
        self.repository.create(self.entity)

    def redo(self):
        self.repository.delete(self.entity.id_entity)
        self.repository.create(self.updated_entity)
