from PySide6.QtWidgets import QListWidgetItem


class BoxQListWidgetItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(BoxQListWidgetItem, self).__init__(*args, **kwargs)

    def __hash__(self):
        return hash(id(self))
