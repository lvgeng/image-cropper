import wx
import os



class MainWindow(wx.Frame):

    def __init__(self, parent):
        self.width = 640
        self.height = 480
        self.color = 'Red'
        self.thinkness = 5
        self.sampleWidth = 56
        self.sampleHeight = 56
        self.imageIndex = 0
        self.hasImages = False
        self.images = []
        self.imagesName = []
        super(MainWindow, self).__init__(parent, -1, "Sampling Application", wx.DefaultPosition, size=(self.width, self.height)) 
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour('White') 
        self.makeMenu()
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusWidths([-1, -2])
        self.bindEvents()
        self.Show(True)



    def bindEvents(self):
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.onImageChange)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.openitem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exititem)
        
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
            dc.Clear()
        self.StretchBackground(dc)
    def StretchBackground(self, dc):
        sz = self.GetClientSize()
        if self.hasImages:
            image = self.images[self.imageIndex].Scale(sz.x,sz.y)
            bg_bmp = image.ConvertToBitmap()
            self.statusBar.SetStatusText("File Name:" + self.imagesName[self.imageIndex], 0)
            dc.DrawBitmap(bg_bmp, 0, 0)  

    def makeMenu(self):
        ''' Make a menu to read images and exit the program '''
    	filemenu = wx.Menu()
    	self.openitem = filemenu.Append(wx.ID_OPEN,"&Open"," Open images for sampling")
    	filemenu.AppendSeparator()
    	self.exititem = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
    	menubar = wx.MenuBar()
    	menubar.Append(filemenu,"&File")        
    	self.SetMenuBar(menubar)
	

    def onLeftDown(self, event):
        ''' Called when the left mouse button is pressed. '''
        self.previousPosition = event.GetPositionTuple()
        print("onLeftDown")

    def onRightDown(self, event):
        ''' Called when the left mouse button is pressed. '''
        dlg = wx.SingleChoiceDialog(self, 'Please select the label: ','Single Choice',['0', '1', '2', '3', '4','5', '6', '7', '8','9'])
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetStringSelection()
            sz = self.GetClientSize()
            image = self.images[self.imageIndex].Scale(sz.x,sz.y)
            bg_bmp = image.ConvertToBitmap()
            grabBitmap = bg_bmp.GetSubBitmap(wx.Rect(  
                    min(self.previousPosition[0], self.currentPosition[0]),  
                    min(self.previousPosition[1], self.currentPosition[1]),  
                    abs(self.previousPosition[0] - self.currentPosition[0]),  
                    abs(self.previousPosition[1] - self.currentPosition[1])  
                   ))  
            grabImage = grabBitmap.ConvertToImage().Scale(self.sampleWidth, self.sampleHeight)
            dirPath = os.path.join(self.dir, response) 
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            imageName = os.path.splitext(self.imagesName[len(self.imagesName) -1])[0]
            fileextend = os.path.splitext(self.imagesName[len(self.imagesName) -1])[1]
            grabImage.SaveFile(os.path.join(dirPath, imageName + '-' + response + ".png"),wx.BITMAP_TYPE_PNG)
        print("onRightDown")
        print(imageName)
        dlg.Destroy() 
        self.Refresh() 

    def onLeftUp(self, event):
        ''' Called when the left mouse button is released. '''    
        dc = wx.ClientDC(self)
        #self.panel.Refresh()
        dc.BeginDrawing()
        pen = wx.Pen(wx.NamedColour(self.color), self.thinkness, wx.SOLID)
        dc.SetPen(pen)
        dc.DrawLine(self.previousPosition[0], self.previousPosition[1], self.currentPosition[0], self.previousPosition[1])
        dc.DrawLine(self.previousPosition[0], self.previousPosition[1], self.previousPosition[0], self.currentPosition[1])
        dc.DrawLine(self.previousPosition[0], self.currentPosition[1], self.currentPosition[0], self.currentPosition[1])
        dc.DrawLine(self.currentPosition[0], self.previousPosition[1], self.currentPosition[0], self.currentPosition[1])
        dc.EndDrawing()
        print("onLeftUp")


    def onMotion(self, event):
        ''' Called when the mouse is in motion. If the left button is
            dragging then draw a line from the last event position to the
            current one. Save the coordinants for redraws. '''
        if event.Dragging() and event.LeftIsDown():
             self.currentPosition = event.GetPositionTuple()
             dc = wx.ClientDC(self)
#            erase the draw lines
             self.Refresh()
             width = self.currentPosition[0] - self.previousPosition[0]
             height =  self.currentPosition[1] - self.previousPosition[1]
             self.statusBar.SetStatusText("Mouse Pos:" + str(event.GetPositionTuple()) + " Width:" '%d' %width + "Height:" + '%d' %height, 1)
             dc.BeginDrawing()
             pen = wx.Pen(wx.NamedColour(self.color), self.thinkness, wx.SOLID)
             dc.SetPen(pen)
             dc.DrawLine(self.previousPosition[0], self.previousPosition[1], self.currentPosition[0], self.previousPosition[1])
             dc.DrawLine(self.previousPosition[0], self.previousPosition[1], self.previousPosition[0], self.currentPosition[1])
             dc.DrawLine(self.previousPosition[0], self.currentPosition[1], self.currentPosition[0], self.currentPosition[1])
             dc.DrawLine(self.currentPosition[0], self.previousPosition[1], self.currentPosition[0], self.currentPosition[1])
             dc.EndDrawing()


    def onImageChange(self, event):
        sk = event.GetKeyCode()

#       for key left, move to the next image
        if sk == wx.WXK_LEFT:   
            if self.imageIndex < len(self.images) - 1:
                self.imageIndex = self.imageIndex + 1
                self.Refresh()
        if sk == wx.WXK_RIGHT:
            if self.imageIndex != 0:
                self.imageIndex  = self.imageIndex - 1
                self.Refresh()
        print("onImageChange")

    def onSize(self, event):
        ''' Called when the window is resized. '''
        self.Refresh()
      

    def cleanup(self, event):
        if hasattr(self, "menu"):
            self.menu.Destroy()
            del self.menu


    def OnOpen(self, event):
        '''
        Open the file dialog
        '''
        print("OnOpen")
        file_wildcard = "Image files(*.png)|*.png|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Open Image files...",
                            os.getcwd(), 
                            style = wx.OPEN|wx.MULTIPLE,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            files = dlg.GetPaths()
            filesName = []
            for myfile in files:
                data_dir, data_file = os.path.split(myfile)
                filesName.append(data_file)
            self.dir = data_dir
            self.hasImages = True
            self.images = []
            for image in filesName:
                newSize = self.GetSize()
                images =  wx.Image(image,wx.BITMAP_TYPE_PNG).Scale(newSize.GetWidth(),newSize.GetHeight(),quality=wx.IMAGE_QUALITY_NORMAL)
                self.images.append(images)
                self.imagesName.append(image)
            self.imageIndex = 0
            self.Refresh()
        dlg.Destroy()


    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.StretchBackground(dc)
        
    def OnExit(self, event):
        self.cleanup(event)
        self.Destroy()
        


        


app = wx.App(False)
frame = MainWindow(None)
app.MainLoop()


