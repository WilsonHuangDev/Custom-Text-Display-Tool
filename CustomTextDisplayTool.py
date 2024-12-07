import wx
import os
import json
import sys


class MyApp(wx.App):
    def OnInit(self):
        self.inputframe = InputFrame(None, title="自定义文本输出工具 v2.7.0.1206")
        self.inputframe.Show()
        return True


class InputFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(
            parent,
            title=title,
            size=(640, 600),
            style=wx.CAPTION
            | wx.SYSTEM_MENU
            | wx.MINIMIZE_BOX,
        )
        self.panel = wx.Panel(self)

        # 文本输入框
        self.text_ctrl = wx.TextCtrl(
            self.panel, style=wx.TE_MULTILINE, size=(600, 400), pos=(10, 10)
        )

        # 字体大小输入
        self.font_size_label = wx.StaticText(
            self.panel, label="字体大小", pos=(20, 420)
        )
        self.font_size_input = wx.SpinCtrl(
            self.panel, value="18", min=8, max=100, pos=(75, 415), size=(60, -1)
        )
        self.font_size_input.Bind(wx.EVT_SPINCTRL, self.on_font_size_change)

        # 字体粗细选择
        self.font_weight_label = wx.StaticText(
            self.panel, label="字体粗细", pos=(250, 420)
        )
        self.font_weight_choices = ["常规", "粗体"]
        self.font_weight_combo = wx.ComboBox(
            self.panel, choices=self.font_weight_choices, pos=(305, 415), size=(60, -1)
        )
        self.font_weight_combo.SetSelection(0)
        self.font_weight_combo.Bind(wx.EVT_COMBOBOX, self.on_font_weight_change)

        # 字体颜色选择
        self.font_color_label = wx.StaticText(
            self.panel, label="字体颜色", pos=(450, 420)
        )
        self.font_color_button = wx.Button(
            self.panel, label="选择颜色", pos=(500, 415), size=(60, -1)
        )
        self.font_color_button.Bind(wx.EVT_BUTTON, self.on_select_color)

        # 选择的颜色指示框
        self.now_color_label = wx.StaticText(
            self.panel, label="当前颜色", pos=(450, 450)
        )
        self.color_label = wx.StaticText(self.panel, label="███", pos=(505, 450))

        # 编辑模版按钮
        self.edit_button = wx.Button(
            self.panel, label="编辑模版", pos=(200, 490), size=(80, -1)
        )
        self.edit_button.Bind(wx.EVT_BUTTON, self.edit_template)

        self.templateframe = None

        # 使用模版按钮
        self.use_button = wx.Button(
            self.panel, label="使用模版", pos=(200, 520), size=(80, -1)
        )
        self.use_button.Bind(wx.EVT_BUTTON, self.load_template)

        # 输出按钮
        self.submit_button = wx.Button(
            self.panel, label="输出", pos=(330, 490), size=(80, -1)
        )
        self.submit_button.Bind(wx.EVT_BUTTON, self.show_custom_message)

        self.outputwindow = OutputWindow(None, title="")
        self.outputwindow.Show(False)

        # 隐藏按钮
        self.hide_button = wx.Button(
            self.panel, label="隐藏", pos=(330, 520), size=(80, -1)
        )
        self.hide_button.Bind(wx.EVT_BUTTON, self.hide_custom_message)

        # 退出程序按钮
        self.hide_button = wx.Button(
            self.panel, label="退出程序", pos=(520, 520), size=(80, -1)
        )
        self.hide_button.Bind(wx.EVT_BUTTON, self.exit)

    def on_select_color(self, event):
        color_data = wx.ColourData()
        dialog = wx.ColourDialog(self, data=color_data)
        if dialog.ShowModal() == wx.ID_OK:
            color = dialog.GetColourData().GetColour()
            self.color_label.SetForegroundColour(color)
            self.Refresh()
            self.output_color(event)
        dialog.Destroy()

    def output_color(self, event):
        output_color = self.color_label.GetForegroundColour()
        print(output_color)
        self.outputwindow.set_font_color(output_color)

    def on_font_size_change(self, event):
        font_size = int(self.font_size_input.GetValue())
        font_weight = self.get_font_weight()
        self.outputwindow.update_info(self.text_ctrl.GetValue(), font_size, font_weight)

    def on_font_weight_change(self, event):
        font_size = int(self.font_size_input.GetValue())
        font_weight = self.get_font_weight()
        self.outputwindow.update_info(self.text_ctrl.GetValue(), font_size, font_weight)

    def show_custom_message(self, event):
        custom_text = self.text_ctrl.GetValue().strip()
        if custom_text:
            self.outputwindow.update_info(
                custom_text,
                int(self.font_size_input.GetValue()),
                self.get_font_weight(),
            )
            self.output_color(event)
            self.outputwindow.center_on_second_screen()  # 调整输出窗口居中
            self.outputwindow.Show()
        else:
            wx.MessageBox("文本框为空!\n无法输出!", "警告", wx.OK | wx.ICON_WARNING)

    def edit_template(self, event):
        # 检查TemplateFrame是否存在
        if self.templateframe:
            # 如果存在，则销毁它
            self.templateframe.Destroy()
        
        # 创建一个新的TemplateFrame实例
        self.templateframe = TemplateFrame(None, title="模版编辑")
        self.templateframe.Show()

    def load_template(self, event):
        try:
            # 检查TemplateFrame是否存在
            if self.templateframe:
                # 如果存在，则销毁它
                self.templateframe.Destroy()

            # 创建一个新的TemplateFrame实例
            self.templateframe = TemplateFrame(None, title="模版编辑")

            config_path = self.templateframe.get_config_path()
            if os.path.exists(config_path):
                print("配置文件位置：", config_path)
                with open(config_path, "r") as f:
                    loaded_data = json.load(f)
                    self.text_ctrl.SetValue(loaded_data["text_value"])
                    self.font_size_input.SetValue(loaded_data["font_size_value"])
                    self.font_weight_combo.SetSelection(loaded_data["font_weight_value"])
                    loaded_color = self.templateframe.string_to_color(str(loaded_data["color_value"]))
                    print("模板字体颜色:", loaded_color)
                    self.color_label.SetForegroundColour(loaded_color)
                    self.Refresh()
            else:
                print("配置文件位置：", config_path, "未找到模板配置文件")
                wx.MessageBox("未找到模板配置文件!", "警告", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            print("模板加载失败:", e)
            wx.MessageBox("模板加载失败!", "错误", wx.OK | wx.ICON_ERROR)

    def hide_custom_message(self, event):
        self.outputwindow.Hide()

    def get_font_weight(self):
        return (
            wx.FONTWEIGHT_BOLD
            if self.font_weight_combo.GetSelection() == 1
            else wx.FONTWEIGHT_NORMAL
        )

    def exit(self, event):
        sys.exit(0)


class TemplateFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(
            parent,
            title=title,
            size=(640, 600),
            style=wx.CAPTION
            | wx.FRAME_NO_TASKBAR,
        )
        self.panel = wx.Panel(self)

        # 选择的颜色指示框
        self.now_color_label = wx.StaticText(
            self.panel, label="当前颜色", pos=(450, 450)
        )
        self.color_label = wx.StaticText(self.panel, label="███", pos=(505, 450))

        # 文本输入框
        self.text_ctrl = wx.TextCtrl(
            self.panel, style=wx.TE_MULTILINE, size=(600, 400), pos=(10, 10)
        )

        # 字体大小输入
        self.font_size_label = wx.StaticText(
            self.panel, label="字体大小", pos=(20, 420)
        )
        self.font_size_input = wx.SpinCtrl(
            self.panel, min=8, max=100, pos=(75, 415), size=(60, -1)
        )
        self.font_size_input.SetValue(18)

        # 字体粗细选择
        self.font_weight_label = wx.StaticText(
            self.panel, label="字体粗细", pos=(240, 420)
        )
        self.font_weight_choices = ["常规", "粗体"]
        self.font_weight_combo = wx.ComboBox(
            self.panel, choices=self.font_weight_choices, pos=(295, 415), size=(60, -1)
        )
        self.font_weight_combo.SetSelection(0)

        # 字体颜色选择
        self.font_color_label = wx.StaticText(
            self.panel, label="字体颜色", pos=(450, 420)
        )
        self.font_color_button = wx.Button(
            self.panel, label="选择颜色", pos=(500, 415), size=(60, -1)
        )
        self.font_color_button.Bind(wx.EVT_BUTTON, self.on_select_color)

        # 填充默认模版按钮
        self.use_button = wx.Button(
            self.panel, label="填充默认模版", pos=(200, 490), size=(80, -1)
        )
        self.use_button.Bind(wx.EVT_BUTTON, self.template_text)

        # 保存模版按钮
        self.submit_button = wx.Button(
            self.panel, label="保存模版", pos=(330, 490), size=(80, -1)
        )
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_save)

        # 加载模版按钮
        self.load_button = wx.Button(
            self.panel, label="加载模版", pos=(200, 520), size=(80, -1)
        )
        self.load_button.Bind(wx.EVT_BUTTON, self.load_data)

        # 删除模版按钮
        self.del_button = wx.Button(
            self.panel, label="删除模版", pos=(330, 520), size=(80, -1)
        )
        self.del_button.Bind(wx.EVT_BUTTON, self.del_custom_template)

        # 关闭按钮
        self.hide_button = wx.Button(
            self.panel, label="关闭", pos=(520, 520), size=(80, -1)
        )
        self.hide_button.Bind(wx.EVT_BUTTON, self.hide_Template_Frame)

    def template_text(self, event):
        self.text_ctrl.SetValue("如需定制播放生日歌等歌曲, 请联系九1班黄炜轩")
        self.font_size_input.SetValue(18)
        self.font_weight_combo.SetSelection(1)
        template_color = self.string_to_color(str("#000000"))
        print("默认模板字体颜色:", template_color)
        self.color_label.SetForegroundColour(template_color)
        self.Refresh()

    def on_select_color(self, event):
        color_data = wx.ColourData()
        dialog = wx.ColourDialog(self, data=color_data)
        if dialog.ShowModal() == wx.ID_OK:
            color = dialog.GetColourData().GetColour()
            print(color)
            self.color_label.SetForegroundColour(color)
            self.Refresh()
        dialog.Destroy()

    def get_font_weight(self):
        return (
            wx.FONTWEIGHT_BOLD
            if self.font_weight_combo.GetSelection() == 1
            else wx.FONTWEIGHT_NORMAL
        )

    def hide_Template_Frame(self, event):
        self.Destroy()

    def on_save(self, event):
        custom_text = self.text_ctrl.GetValue().strip()
        if custom_text:
            data = {
                "text_value": self.text_ctrl.GetValue(),
                "font_size_value": self.font_size_input.GetValue(),
                "font_weight_value": self.font_weight_combo.GetSelection(),
                "color_value": self.color_label.GetForegroundColour().GetAsString(wx.C2S_HTML_SYNTAX),
            }
            self.save_template(data)
        else:
            print("文本框为空!无法保存模版!")
            wx.MessageBox("文本框为空!\n无法保存模版!", "警告", wx.OK | wx.ICON_WARNING)

    def del_custom_template(self, event):
        config_path = self.get_config_path()
        if os.path.exists(config_path):
            print("配置文件位置：", config_path)
            os.remove(config_path)
            wx.MessageBox("模版删除成功!", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            print("配置文件位置：", config_path, "未找到模板配置文件")
            wx.MessageBox("未找到模板配置文件!", "警告", wx.OK | wx.ICON_WARNING)

    def get_config_path(self):
        appdata_dir = os.getenv("APPDATA") or os.path.expanduser("~")
        config_dir = os.path.join(appdata_dir, "CustomTextDisplayTool")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, "config.json")

    def save_template(self, data):
        try:
            config_path = self.get_config_path()
            print("配置文件位置：", config_path)
            with open(config_path, "w") as f:
                json.dump(data, f)
            wx.MessageBox("模版保存成功!", "提示", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            print("模板保存失败:", e)
            wx.MessageBox("模板保存失败!", "错误", wx.OK | wx.ICON_ERROR)

    def string_to_color(self, event):
        return wx.Colour(event)

    def load_data(self, event):
        try:
            config_path = self.get_config_path()
            if os.path.exists(config_path):
                print("配置文件位置：", config_path)
                with open(config_path, "r") as f:
                    loaded_data = json.load(f)
                    self.text_ctrl.SetValue(loaded_data["text_value"])
                    self.font_size_input.SetValue(loaded_data["font_size_value"])
                    self.font_weight_combo.SetSelection(loaded_data["font_weight_value"])
                    loaded_color = self.string_to_color(str(loaded_data["color_value"]))
                    print("模板字体颜色:", loaded_color)
                    self.color_label.SetForegroundColour(loaded_color)
                    self.Refresh()
            else:
                print("配置文件位置：", config_path, "未找到模板配置文件")
                wx.MessageBox("未找到模板配置文件!", "警告", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            print("模板加载失败:", e)
            wx.MessageBox("模板加载失败!", "错误", wx.OK | wx.ICON_ERROR)


class OutputWindow(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(
            parent,
            title=title,
            style=wx.CAPTION
            | wx.STAY_ON_TOP
            | wx.FRAME_NO_TASKBAR,
        )
        self.panel = wx.Panel(self)
        self.info_label = wx.StaticText(self.panel, label="", pos=(10, 10))
        self.info_label.Wrap(300)
        self.dragging = False
        self.resizing = False
        self.adjust_size()
        self.center_on_second_screen()

    def center_on_second_screen(self):
        display = wx.Display()
        screens = [display] + [wx.Display(i) for i in range(1, display.GetCount())]
        if len(screens) > 1:
            second_screen = screens[1]
        else:
            second_screen = screens[0]
        x, y = second_screen.GetGeometry().GetTopLeft()
        width, height = second_screen.GetGeometry().GetSize()
        x += (width - self.GetSize().GetWidth()) // 2
        y = -30  # 屏幕顶端
        self.SetPosition((x, y))

    def adjust_size(self):
        text_size = self.info_label.GetBestSize()
        width = text_size[0] + 40
        height = text_size[1] + 60
        self.SetSize((width, height))

    def set_font_color(self, color):
        self.info_label.SetForegroundColour(color)
        self.Refresh()

    def update_info(self, text, font_size, font_weight):
        font = self.info_label.GetFont()
        font.PointSize = font_size
        font.Weight = font_weight
        self.info_label.SetFont(font)
        self.info_label.SetLabel(text)
        self.adjust_size()  # 调整窗口大小以适应内容
        self.center_on_second_screen()  # 居中显示


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
