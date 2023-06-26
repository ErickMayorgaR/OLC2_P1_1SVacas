class NodeCst():
    def __init__(self, value):
        self.children = []
        self.value = value

    def setChildren(self, children):
        self.children = children

    def setValue(self, value):
        self.value = value

    def addChild(self, childValue):
        self.children.append(NodeCst(childValue))

    def addChildren(self, children):
        for child in children:
            self.children.append(child)

    def addChildNode(self, childNode):
        self.children.append(childNode)

    def addFirstChild(self, childValue):
        self.children.insert(0, NodeCst(childValue))

    def addFirstChildNode(self, child):
        self.children.insert(0, child)

    def getValue(self):
        return str(self.value)

    def getChildren(self):
        return self.children