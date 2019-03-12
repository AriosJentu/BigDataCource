import wx
import model
import os

class AppFrame(wx.Frame):

	TOP_PADD = 46
	PLAY_ID = 2
	CLEAR_ID = 3
	OPEN_ID = 4
	SPIN_ID = 5

	def __init__(self, parent, fid, position, size):

		#Create frame
		wx.Frame.__init__(self, parent, fid, "Visualizer", 
			wx.Point(position), wx.Size(size)
		)

		#Graphical elements - buttons and info
		self.PlayButton = wx.Button(self, AppFrame.PLAY_ID, "Play", 
			wx.Point(self.GetSize().Width-2-60, 2), 
			wx.Size(60, AppFrame.TOP_PADD-4)
		)

		self.OpenButton = wx.Button(self, AppFrame.OPEN_ID, "Open",
			wx.Point(2, 2), wx.Size(60, AppFrame.TOP_PADD-4)
		)

		self.ClearButton = wx.Button(self, AppFrame.CLEAR_ID, "Clear",
			wx.Point(self.GetSize().Width-2*(2+60), 2), 
			wx.Size(60, AppFrame.TOP_PADD-4)
		)

		self.Spin = wx.SpinCtrl(self, AppFrame.SPIN_ID, "0",
			wx.Point(self.GetSize().Width - 4*(2+60), 2),
			wx.Size(120, AppFrame.TOP_PADD-4)
		)

		self.Info = wx.StaticText(self, -1, "Size: \nFrame: ; Frames:", 
			wx.Point(64, 2), wx.DefaultSize
		)
		
		self.OpenDialog = wx.FileDialog(self, "Open file", os.getcwd(), "", 
			"JSON Picture File (*.json)|*.json", wx.FD_OPEN
		)

		#GUI Properties
		self.SetMinSize(wx.Size(500, 400))
		self.Spin.SetRange(0, 100)

		#Properties
		self.PictureFile = model.PictureFile()
		self.Animated = False
		self.Brush = wx.Brush("white")

		self.PictureSize = wx.Size(self.PictureFile.get_size())
		self.PixelSize = wx.Size(1, 1)
		self.PlaneSize = wx.Size(0, 0)

		self.Pixels = None #Iterator
		self._BUFFER = wx.Bitmap(100, 100)

		#Events
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_BUTTON, self.OnClickPlay, self.PlayButton)
		self.Bind(wx.EVT_BUTTON, self.OnClickOpen, self.OpenButton)
		self.Bind(wx.EVT_BUTTON, self.OnClickClear, self.ClearButton)
		self.Bind(wx.EVT_SPINCTRL, self.OnScrollSpin, self.Spin)

		self.RecalculatePixelSize()
		self.UpdateDraw()


	def OnSize(self, event):

		self.PlayButton.SetPosition(wx.Point(self.GetSize().Width-2-60, 2))
		self.ClearButton.SetPosition(wx.Point(self.GetSize().Width-2*(2+60), 2))
		self.Spin.SetPosition(wx.Point(self.GetSize().Width-4*(2+60), 2))

		self.RecalculatePixelSize()

		self._BUFFER = wx.Bitmap(self.PlaneSize)
		self.UpdateDraw()


	def OnPaint(self, event=None):

		PaintZone = wx.PaintDC(self)
		PaintZone.DrawBitmap(self._BUFFER, 0, AppFrame.TOP_PADD)


	def RecalculatePixelSize(self):

		ClientSize = self.GetClientSize()
		SpinValue = self.Spin.GetValue()

		if self.PictureSize != wx.Size(0, 0) and SpinValue == 0:
			self.PixelSize = wx.Size(
				ClientSize.Width // self.PictureSize.Width,
				(ClientSize.Height-AppFrame.TOP_PADD)//self.PictureSize.Height
			)
		else:
			self.PixelSize = wx.Size(SpinValue, SpinValue)

		self.PlaneSize = wx.Size(
			ClientSize.Width, 
			ClientSize.Height-AppFrame.TOP_PADD
		)


	def Draw(self, memory):

		self.Info.SetLabel("Size: {}x{}\nFrame: {}; Frames: {}".format(
			self.PictureFile.width,
			self.PictureFile.height,
			self.PictureFile.frame, 
			self.PictureFile.frames
		))

		memory.SetBackground(self.Brush)
		memory.Clear()

		Index = 0
		for Pixels in self.Pixels:
			
			ix = Index // self.PictureSize.Width
			iy = Index % self.PictureSize.Width

			x = ix*self.PixelSize.Width
			y = iy*self.PixelSize.Height

			position = wx.Point(x, y)

			memory.SetBrush(wx.Brush(wx.Colour(*Pixels)))
			memory.SetPen(wx.Pen("white", 0))
			memory.DrawRectangle(position, self.PixelSize)

			Index += 1
	

	def UpdateDraw(self):

		Memory = wx.MemoryDC()
		Memory.SelectObject(self._BUFFER)
		self.Pixels = self.PictureFile.iter_current_frame()
		self.Draw(Memory)
		del Memory
		self.Refresh(eraseBackground=False)
		self.Update()


	def OnClickPlay(self, evt):

		self.Animated = not self.Animated
		self.PlayButton.SetLabel("Pause" if self.Animated else "Play")


	def OnClickOpen(self, evt):

		if self.OpenDialog.ShowModal() != wx.ID_CANCEL:

			path = self.OpenDialog.GetPath()

			self.PictureFile = model.PictureFile(path)
			self.PictureFile.open()
			self.PictureFile.read_meta()

			self.PictureSize = wx.Size(self.PictureFile.get_size())
			self.RecalculatePixelSize()

			spath = path[path.rfind("/"):]
			
			self.SetTitle("Visualizer: "+spath)
			self.Pixels = self.PictureFile.iter_current_frame()
			self.UpdateDraw()


	def OnClickClear(self, evt):

		self.PictureFile.clear()
		self.Animated = False

		self.PictureSize = wx.Size(0, 0)
		self.PixelSize = wx.Size(1, 1)

		self.Pixels = None
		self._BUFFER = wx.Bitmap(self.PlaneSize)
		self.UpdateDraw()


	def OnScrollSpin(self, evt):

		self.RecalculatePixelSize()
		self.UpdateDraw()


class Executor(wx.App):

	def OnInit(self):

		#Main event when initialize application
		self.Frame = AppFrame(None, -1, (0, 0), (500, 400))
		self.Frame.CentreOnScreen()
		self.Frame.Show()

		return True

app = Executor(0)
app.MainLoop()
