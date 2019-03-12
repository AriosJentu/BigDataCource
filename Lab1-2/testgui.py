import wx

class AppFrame(wx.Frame):

	def __init__(self):

		wx.Frame.__init__(self, None, wx.ID_ANY, "Test", 
			wx.Point(100, 100), wx.Size(500, 400)
		)

		self._BUFFER = wx.Bitmap(100, 100)
		self.Pixels = [
			[102, 0, 255],
			[203, 102, 200],
			[0, 255, 124],
			[142, 175, 204]
		]

		self.Width = 2
		self.Height = 2

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnResize)
		self.UpdateDraw()


	def OnResize(self, event):

		self._BUFFER.SetSize(wx.Size(300, 300))


	def OnPaint(self, event):

		PaintZone = wx.PaintDC(self)
		PaintZone.DrawBitmap(self._BUFFER, 0, 0)

	def UpdateDraw(self):

		Memory = wx.MemoryDC()
		Memory.SelectObject(self._BUFFER)
		self.Draw(Memory)
		del Memory
		self.Refresh(eraseBackground=False)
		self.Update()

	def Draw(self, memory):

		memory.SetBackground(wx.Brush("white"))
		memory.Clear()

		for i in range(self.Width):
			for j in range(self.Height):

				x = i*10
				y = j*10

				position = wx.Point(x, y)
				indx = i*self.Width + j

				memory.SetBrush(wx.Brush(wx.Colour(*self.Pixels[indx])))
				memory.SetPen(wx.Pen("white", 0))
				memory.DrawRectangle(position, wx.Size(10, 10))




app = wx.App(0)
frame = AppFrame()
frame.Show()
app.MainLoop()
