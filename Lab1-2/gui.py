import wx
import model
import os

class AppFrame(wx.Frame):

	TOP_PADD = 46
	PLAY_ID = 2
	OPEN_ID = 3

	def __init__(self, parent, fid, position, size):

		#Create frame
		wx.Frame.__init__(self, parent, fid, "Visualizer", 
			wx.Point(position), wx.Size(size)
		)

		self.SetMinSize(wx.Size(100, 100))

		#Graphical elements - buttons and info
		self.PlayButton = wx.Button(self, AppFrame.PLAY_ID, "Play", 
			wx.Point(self.GetSize().Width-2-60, 2), 
			wx.Size(60, AppFrame.TOP_PADD-4)
		)

		self.OpenButton = wx.Button(self, AppFrame.OPEN_ID, "Open",
			wx.Point(2, 2), wx.Size(60, AppFrame.TOP_PADD-4)
		)

		self.Info = wx.StaticText(self, -1, "Size: \nFrame: ; Frames:", 
			wx.Point(64, 2), wx.DefaultSize
		)
		
		self.OpenDialog = wx.FileDialog(self, "Open file", os.getcwd(), "", 
			"JSON Picture File (*.json)|*.json", wx.FD_OPEN
		)

		#Properties
		self.PictureFile = model.PictureFile()
		self.Animated = False
		self.Brush = wx.Brush("white")

		self.PictureSize = wx.Size(self.PictureFile.get_size())
		self.PixelSize = wx.Size(1, 1)

		self.Pixels = [] #[[r, g, b], [r, g, b]]

		#Events
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_BUTTON, self.OnClickPlay, self.PlayButton)
		self.Bind(wx.EVT_BUTTON, self.OnClickOpen, self.OpenButton)

		self.RecalculatePixelSize()


	def OnSize(self, event):
		self.PlayButton.SetPosition(wx.Point(self.GetSize().Width-2-60, 2))
		self.RecalculatePixelSize()


	def OnPaint(self, event):

		self.RecalculatePixelSize()
		self.PaintZone = wx.PaintDC(self)

		self.PaintZone.SetBackground(self.Brush)
		self.PaintZone.Clear()

		self.Draw()


	def RecalculatePixelSize(self):

		ClientSize = self.GetClientSize()

		if self.PictureSize != wx.Size(0, 0):
			self.PixelSize = wx.Size(
				ClientSize.Width // self.PictureSize.Width,
				(ClientSize.Height-AppFrame.TOP_PADD)//self.PictureSize.Height
			)


	def Draw(self):
		
		self.Info.SetLabel("Size: {}x{}\nFrame: {}; Frames: {}".format(
			self.PictureFile.width,
			self.PictureFile.height,
			self.PictureFile.frame, 
			self.PictureFile.frames
		))

		for IndexY in range(self.PictureSize.Height):
			for IndexX in range(self.PictureSize.Width):

				x = IndexX*self.PixelSize.Width
				y = IndexY*self.PixelSize.Height+AppFrame.TOP_PADD

				position = wx.Point(x, y)
				i = IndexY*self.PictureSize.Width + IndexX

				self.PaintZone.SetBrush(wx.Brush(wx.Colour(*self.Pixels[i])))
				self.PaintZone.SetPen(wx.Pen("white", 0))
				self.PaintZone.DrawRectangle(position, self.PixelSize)


	def OnClickPlay(self, evt):
		self.Animated = not self.Animated
		self.PlayButton.SetLabel("Pause" if self.Animated else "Play")


	def OnClickOpen(self, evt):

		if self.OpenDialog.ShowModal() != wx.ID_CANCEL:

			path = self.OpenDialog.GetPath()

			self.PictureFile = model.PictureFile(path)
			self.PictureFile.open()
			self.PictureFile.read_meta()

			spath = path[path.rfind("/"):]
			
			self.SetTitle("Visualizer: "+spath)
			self.UpdateMetaInfo()


	def UpdateMetaInfo(self):
			
			self.PictureSize = wx.Size(self.PictureFile.get_size())
			self.Pixels = self.PictureFile.read_next_frame()
			self.Draw()


class Executor(wx.App):

	def OnInit(self):

		#Main event when initialize application
		self.Frame = AppFrame(None, -1, (0, 0), (300, 300))
		self.Frame.CentreOnScreen()
		self.Frame.Show()

		return True

app = Executor(0)
app.MainLoop()
