MAX_OBJECTS_PER_CUBE = 10

DIRLOOKUP = {"3":0, "2":1, "-2":2, "-1":3, "1":4, "0":5, "-4":6, "-3":7}

try:
    import psyco
    psyco.full()
except:
    print ("Could not import psyco, speed may suffer :)")

class OctNode:
    def _init_(self, position, size, data):
        self.position = position
        self.size = size
        self.isLeafNode = True
        self.data = data
        self.ldb = (position[0] - (size / 2), position[1] - (size / 2), position[2] - (size / 2))
        self.ruf = (position[0] + (size / 2), position[1] + (size / 2), position[2] + (size / 2))
        

class Octree:
    def _init_(self, worldSize):
        self.root = self.addNode((0,0,0), worldSize, [])
        self.worldSize = worldSize

    def addNode(self, position, size, objects):
        return OctNode(position, size, objects)

    def insertNode(self, root, size, parent, objData):
        if root == None:
            pos = parent.position
            offset = size / 2
            branch = self.findBranch(parent, objData.position)
            newCenter = (0,0,0)
            if branch == 0:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
                
            elif branch == 1:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
                
            elif branch == 2:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
                
            elif branch == 3:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )

            elif branch == 4:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )

            elif branch == 5:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
                
            elif branch == 6:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )

            elif branch == 7:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            return self.addNode(newCenter, size, [objData])
        
        elif root.position != objData.position and root.isLeafNode == False:
            branch = self.findBranch(root, objData.position)
            newSize = root.size / 2
            root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, objData)
        elif root.isLeafNode:
            if len(root.data) < MAX_OBJECTS_PER_CUBE:
                root.data.append(objData)
            elif len(root.data) == MAX_OBJECTS_PER_CUBE:
                root.data.append(objData)
                objList = root.data
                root.data = None
                root.isLeafNode = False
                newSize = root.size / 2
                for ob in objList:
                    branch = self.findBranch(root, ob.position)
                    root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, ob)
        return root

    def findPosition(self, root, position):
        if root == None:
            return None
        elif root.isLeafNode:
            return root.data
        else:
            branch = self.findBranch(root, position)
            return self.findPosition(root.branches[branch], position)
            

    def findBranch(self, root, position):
        vec1 = root.position
        vec2 = position
        result = 0
        for i in range(3):
            if vec1[i] <= vec2[i]:
                result += (-4 / (i + 1) / 2)
            else:
                result += (4 / (i + 1) / 2)
        result = DIRLOOKUP[str(result)]
        return result



if __name__ == "__main__":
    import random
    import time
    class TestObject:
        def _init_(self, name, position):
            self.name = name
            self.position = position
    myTree = Octree(15000.0000)
    NUM_TEST_OBJECTS = 2000
    NUM_COLLISION_LOOKUPS = 2000
    Start = time.time()
    for x in range(NUM_TEST_OBJECTS):
        name = "Node__" + str(x)
        pos = (random.randrange(-4500.000, 4500.000), random.randrange(-4500.00, 4500.00), random.randrange(-4500.00, 4500.00))
        testOb = TestObject(name, pos)
        myTree.insertNode(myTree.root, 15000.000, myTree.root, testOb)
    End = time.time() - Start

    print (str(NUM_TEST_OBJECTS) + "-Node Tree Generated in " + str(End) + " Seconds")
    print ("Tree Leaves contain a maximum of " + str(MAX_OBJECTS_PER_CUBE) + " objects each.")



    Start = time.time()
    for x in range(NUM_COLLISION_LOOKUPS):
        pos = (random.randrange(-4500.000, 4500.000), random.randrange(-4500.00, 4500.00), random.randrange(-4500.00, 4500.00))
        result = myTree.findPosition(myTree.root, pos)


    End = time.time() - Start

    print (str(NUM_COLLISION_LOOKUPS) + " Collision Lookups performed in " + str(End) + " Seconds")
    print ("Tree Leaves contain a maximum of " + str(MAX_OBJECTS_PER_CUBE) + " objects each.")

    x = raw_input("Press any key (Wheres the any key?):")
