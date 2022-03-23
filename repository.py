class Repository:
    def __init__(self, key, description, packageType, rclass):
        self.key = key
        self.description = description
        self.packageType = packageType
        self.rclass = rclass  #local virtual or remote