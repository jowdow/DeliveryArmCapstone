import time
import urx
import wx
import enum


class Modes(enum.Enum):
    stop = 1
    run = 2


# Custom class to allow for custom points
class DeliveryPoint:
    def __init__(self, jointDegree, name):
        self.jointDegree = jointDegree
        self.name = name


# Custom class to allow for custom points
class PickupPoint:
    def __init__(self, jointDegree, name):
        self.jointDegree = jointDegree
        self.name = name


def startApp(frameApp):
    rv = wx.PyApp.MainLoop(frameApp)
    frameApp.RestoreStdio()


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(731, 570), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(100, 100), wx.DefaultSize)

        self.m_toolBar1 = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.commandsTool = self.m_toolBar1.AddTool(wx.ID_ANY, u"tool", wx.Bitmap(u"sudoku.ico", wx.BITMAP_TYPE_ANY),
                                                    wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar1.Realize()

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Move Commands"), wx.VERTICAL)

        sbSizer3.SetMinSize(wx.Size(100, 100))
        gbSizer7 = wx.GridBagSizer(0, 0)
        gbSizer7.SetFlexibleDirection(wx.BOTH)
        gbSizer7.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        gbSizer7.SetMinSize(wx.Size(10, 10))
        m_choice2Choices = [u"MoveJ", u"MoveL", u"MoveP"]
        self.m_choice2 = wx.Choice(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   m_choice2Choices, 0)
        self.m_choice2.SetSelection(0)
        gbSizer7.Add(self.m_choice2, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Base", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        gbSizer7.Add(self.m_staticText7, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl7 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        gbSizer7.Add(self.m_textCtrl7, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText8 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Shoulder", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        gbSizer7.Add(self.m_staticText8, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl9 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        gbSizer7.Add(self.m_textCtrl9, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Elbow", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        gbSizer7.Add(self.m_staticText10, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl10 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        gbSizer7.Add(self.m_textCtrl10, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Wrist 1", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        gbSizer7.Add(self.m_staticText11, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl11 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        gbSizer7.Add(self.m_textCtrl11, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText12 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Wrist 2", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        gbSizer7.Add(self.m_staticText12, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl12 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        gbSizer7.Add(self.m_textCtrl12, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Wrist 3", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)

        gbSizer7.Add(self.m_staticText13, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl13 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        gbSizer7.Add(self.m_textCtrl13, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.moveBT = wx.Button(sbSizer3.GetStaticBox(), wx.ID_ANY, u"MOVE", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer7.Add(self.moveBT, wx.GBPosition(6, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.stopBT = wx.BitmapButton(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                      wx.DefaultSize, wx.BU_AUTODRAW | 0)

        self.stopBT.SetBitmap(wx.Bitmap(u"stop.bmp", wx.BITMAP_TYPE_ANY))
        gbSizer7.Add(self.stopBT, wx.GBPosition(15, 29), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        sbSizer3.Add(gbSizer7, 1, wx.EXPAND, 5)

        self.SetSizer(sbSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.stopBT.Bind(wx.EVT_BUTTON, self.stop)

    def __del__(self):
        pass

    def stop(self, event):
        programState = Modes.stop
        print("Stopped")
        self.Skip()


###########################################################################
## Class MyFrame2
###########################################################################


class MyFrame2(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.programState = Modes.stop

        self.m_toolBar2 = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        self.commandsTool = self.m_toolBar2.AddTool(wx.ID_ANY, u"tool", wx.Bitmap(u"sudoku.ico", wx.BITMAP_TYPE_ANY),
                                                    wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar2.Realize()

        wSizer3 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.startBT = wx.Button(self, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer3.Add(self.startBT, 0, wx.ALL, 5)

        self.stopBT = wx.BitmapButton(self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                      wx.BU_AUTODRAW | 0)

        self.stopBT.SetBitmap(wx.Bitmap(u"stop.bmp", wx.BITMAP_TYPE_ANY))
        wSizer3.Add(self.stopBT, 0, wx.ALL, 5)

        self.SetSizer(wSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.startBT.Bind(wx.EVT_BUTTON, self.start)
        self.stopBT.Bind(wx.EVT_BUTTON, self.stop)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class

    def start(self, event):
        self.programState = Modes.run
        event.Skip()

    def stop(self, event):
        self.programState = Modes.stop
        event.Skip()


def main():
    programState = Modes.stop

    mainDeliveryPoint = DeliveryPoint([0, 1.57, -1.57, 3.14, -1.57, 1.57], "Main")
    mainPickupPoint = PickupPoint([0, 1.57, -1.57, 3.14, -1.57, 1.57], "Main")

    # rob = urx.Robot("localhost")
    # The below set up is a random/default for the TCP and payload. Details on the numbers to put in is in the link below
    # https://academy.universal-robots.com/modules/e-Series%20core%20track/English/module3/story_html5.html?courseId=2166&language=English
    # rob.set_tcp((0, 0, 0.1, 0, 0, 0))
    # rob.set_payload(2, (0, 0, 0.1))

    time.sleep(0.2)  # leave some time to robot to process the setup commands

    # STARTING GUI
    app = wx.App()
    frame1 = MyFrame1(parent=None)
    frame2 = MyFrame2(parent=None)
    # app.MainLoop()
    print("Starting")
    startApp(app)
    print("a")
    while True:
        print(frame2.programState)
        frame2.Show()
        if frame2.programState == Modes.run:
            programState = Modes.run
            print("a")
        print("Stopped")
        time.sleep(2)
        while programState == Modes.run:
            print("Main loop running")
            time.sleep(2)
            if frame2.programState == Modes.stop:
                programState = Modes.stop
            # if found face that has delivery
            #   tell arm to go to pickup the spot
            #   tell arm to grab
            #   tell arm to go to delivery spot
            #   tell arm to drop
            #   tell arm to go to wait stop


if __name__ == '__main__':
    main()
