import hou
import os

from PySide2 import QtCore, QtUiTools, QtWidgets

class visCo(QtWidgets.QWidget):
    def __init__(self):
        #define and load UI
        super(visCo, self).__init__()

        scriptpath = "D:/Desktop/new.ui"
        self.ui = QtUiTools.QUiLoader().load(scriptpath, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.ui.btn_Browse.clicked.connect(self.btnBrowse)
        self.ui.btn_BrowseOutput.clicked.connect(self.btnBrowseOutput)

        self.ui.btn_Process.clicked.connect(self.btnProcess)

        self.ui.list_FilesList.itemDoubleClicked.connect(self.on_item_double_clicked)

    def on_item_double_clicked(self, item):
        row = self.ui.list_FilesList.row(item)
        self.ui.list_FilesList.takeItem(row)

    def btnBrowse(self):
        # path = self.ui.line_Input
        if self.ui.line_InputPath == "":
            inputPath = hou.ui.selectFile(title = "Select an fbx file", file_type = hou.fileType.Fbx)
            if inputPath != "":
                self.ui.list_FilesList.addItem(inputPath)
        else:
            inputPath = hou.ui.selectFile(start_directory = self.ui.line_InputPath.text().replace('\\', '/'), title = "Select an fbx file", file_type = hou.fileType.Fbx)
            if inputPath != "":
                self.ui.list_FilesList.addItem(inputPath)
            self.ui.line_InputPath.setText("")

    def btnBrowseOutput(self):
        outputPath = hou.ui.selectFile(title = "Select a folder", file_type = hou.fileType.Directory)
        self.ui.lbl_OutputPath.setText(outputPath)

    def btnProcess(self):
        theList = self.ui.list_FilesList

        if theList.count() == 0:
            hou.ui.displayMessage("Please select at least one fbx file!")
        else:
            context = hou.node("/obj")
            hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).setPwd(context)
            myContainer = context.createNode("geo")

            myMerge = myContainer.createNode("merge")

            for i in range(theList.count()):
                myNode = myContainer.createNode("file")
                myNode.parm("file").set(theList.item(i).text())
                myNode.moveToGoodPosition()

                myMerge.setInput(i, myNode)
                myMerge.moveToGoodPosition()


            myNewNode = myContainer.createNode("connectivity")
            myNewNode.parm("connecttype").set(1)
            myNewNode.setInput(0, myMerge)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("compile_begin")
            myNewNode.parm("blockpath").set("../compile_end1")
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("block_begin")
            myNewNode.parm("method").set(1)
            myNewNode.parm("blockpath").set("../block_end1")
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("attribwrangle")
            myNewNode.parm("snippet").set("@P.y = 0;")
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("triangulate2d::3.0")
            myNewNode.parm("usesilhouettepolys").set(1)
            myNewNode.parm("silhouettepolys").set("*")
            myNewNode.parm("removeoutsidesilhouette").set(1)
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("divide")
            myNewNode.parm("removesh").set(1)
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("ends")
            myNewNode.parm("closeu").set(5)
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("block_end")
            myNewNode.parm("itermethod").set(1)
            myNewNode.parm("method").set(1)
            myNewNode.parm("class").set(0)
            myNewNode.parm("attrib").set("class")
            myNewNode.parm("blockpath").set("../block_begin1")
            myNewNode.parm("templatepath").set("../block_begin1")
            myNewNode.parm("multithread").set(1)
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("compile_end")
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("convertline")
            myNewNode.parm("computelength").set(0)
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("xform")
            myNewNode.parm("rx").set(90)
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNode = myNewNode

            myNewNode = myContainer.createNode("filecache::2.0")
            myNewNode.parm("filemethod").set(1)
            myNewNode.parm("timedependent").set(0)
            myNewNode.parm("file").set(self.ui.lbl_OutputPath.text() + "2d_plan.dxf")
            myNewNode.setInput(0, myNode)
            myNewNode.moveToGoodPosition()
            myNewNode.parm("execute").pressButton()
            myNode = myNewNode

            myNewContainer = context.createNode("geo")
            myNewNode = myNewContainer.createNode("file")
            myNewNode.parm("file").set(self.ui.lbl_OutputPath.text() + "2d_plan.dxf")
            # myNewNode.setDisplayFlag(1)
            # myNewNode.setRenderFlag(1)
            # myNewContainer.setGenericFlag(hou.nodeFlag.Current, 1)
            
            myContainer.destroy()

            mySceneViewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
            mySceneViewer.referencePlane().setIsVisible("on")
            mySceneViewer.curViewport().changeType(hou.geometryViewportType.Front)
            
            hou.ui.displayMessage("Done:)")

            mySceneViewer.curViewport().frameAll()
            
            # self.ui.list_FilesList.clear()
            # theList.clear()

# class MyWidgetList(QtWidgets.QListWidget):
#     def on_item_double_clicked(self):
#         item = MyWidgetList.itemDoubleClicked
#         row = self.row(item)
#         self.takeItem(row)


win = visCo()
win.show()