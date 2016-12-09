from girder.models.item import Item
from girder.models.model_base import ValidationException

from .meta import TCGAModel


class Aperio(TCGAModel, Item):

    TCGAType = 'aperio'

    def importDocument(self, doc, **kwargs):
        recurse = kwargs.get('recurse', False)

        if doc.get('_modelType', 'item') == 'item':
            name = doc['name']
            tcga = self.parseAperio(name)
            self.setTCGA(doc, **tcga)

            doc = super(Aperio, self).importDocument(doc, **kwargs)
            return doc
        elif recurse:
            for item in self.iterateItems(doc):
                try:
                    self.importDocument(item, **kwargs)
                except ValidationException:
                    pass
        else:
            raise ValidationException('Invalid model type')
