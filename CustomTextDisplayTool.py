import wx
import os
import json
import sys


name = str("CustomTextDisplayTool")
name_zh = str("自定义文本输出工具")
template_frame_name_zh = str("模版编辑")


class MyApp(wx.App):
    def OnInit(self):
        self.inputframe = InputFrame(None, title=name_zh)
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
            | wx.MINIMIZE_BOX
            | wx.CLOSE_BOX,
        )
        self.panel = wx.Panel(self)

        # 绑定关闭事件到 on_close 方法
        self.Bind(wx.EVT_CLOSE, self.on_close)

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

        # 字体粗细选择
        self.font_weight_label = wx.StaticText(
            self.panel, label="字体粗细", pos=(250, 420)
        )
        self.font_weight_choices = ["常规", "粗体"]
        self.font_weight_combo = wx.ComboBox(
            self.panel, choices=self.font_weight_choices, pos=(305, 415), size=(60, -1)
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

        self.outputwindow = None

        # 隐藏按钮
        self.hide_button = wx.Button(
            self.panel, label="隐藏", pos=(330, 520), size=(80, -1)
        )
        self.hide_button.Bind(wx.EVT_BUTTON, self.hide_custom_message)

    def on_select_color(self, event):
        color_data = wx.ColourData()
        dialog = wx.ColourDialog(self, data=color_data)
        if dialog.ShowModal() == wx.ID_OK:
            color = dialog.GetColourData().GetColour()
            self.color_label.SetForegroundColour(color)
            output_color = self.color_label.GetForegroundColour()
            print(output_color)
            self.Refresh()
        dialog.Destroy()

    def show_custom_message(self, event):
        # 检查OutputWindow是否存在
        if self.outputwindow:
            # 如果存在，则销毁它
            self.outputwindow.Destroy()
        
        # 创建一个新的OutputWindow实例
        self.outputwindow = OutputWindow(None, title="")
        
        custom_text = self.text_ctrl.GetValue().strip()
        font_size = int(self.font_size_input.GetValue())
        font_weight = self.get_font_weight()
        output_color = self.color_label.GetForegroundColour()
        if custom_text:
            self.outputwindow.set_font_color(output_color)
            self.outputwindow.update_info(
                custom_text,
                font_size,
                font_weight,
            )
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
        self.templateframe = TemplateFrame(self, title=template_frame_name_zh)
        self.templateframe.load_data(event)
        self.templateframe.Show()

    def load_template(self, event):
        try:
            # 检查TemplateFrame是否存在
            if self.templateframe:
                # 如果存在，则销毁它
                self.templateframe.Destroy()

            # 创建一个新的TemplateFrame实例
            self.templateframe = TemplateFrame(self, title=template_frame_name_zh)

            config_path = self.templateframe.get_config_path()
            if os.path.exists(config_path):
                print("配置文件位置: ", config_path)
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
                print("配置文件位置: ", config_path, "未找到模板配置文件")
                wx.MessageBox("未找到模板配置文件!", "警告", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            print("模板加载失败:", e)
            wx.MessageBox("模板加载失败!", "错误", wx.OK | wx.ICON_ERROR)

    def hide_custom_message(self, event):
        self.outputwindow.Destroy()

    def get_font_weight(self):
        return (
            wx.FONTWEIGHT_BOLD
            if self.font_weight_combo.GetSelection() == 1
            else wx.FONTWEIGHT_NORMAL
        )

    def on_close(self, event):
        # 弹出一个对话框询问用户是否要退出
        dlg = wx.MessageDialog(self, "是否退出程序？", "退出程序", wx.YES_NO)
        result = dlg.ShowModal()
        dlg.Destroy()
        
        if result == wx.ID_YES:
            # 如果用户选择是，则退出应用程序
            sys.exit(0)
        else:
            # 如果用户选择否，则忽略关闭事件
            event.Veto()


class TemplateFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(
            parent,
            title=title,
            size=(640, 580),
            style=wx.CAPTION,
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
            self.panel, label="填充默认模版", pos=(170, 500), size=(80, -1)
        )
        self.use_button.Bind(wx.EVT_BUTTON, self.template_text)
        self.use_button.Enable(False)

        # 保存模版按钮
        self.submit_button = wx.Button(
            self.panel, label="保存模版", pos=(270, 500), size=(80, -1)
        )
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_save)

        # 删除模版按钮
        self.del_button = wx.Button(
            self.panel, label="删除模版", pos=(370, 500), size=(80, -1)
        )
        self.del_button.Bind(wx.EVT_BUTTON, self.del_custom_template)

        # 关闭按钮
        self.hide_button = wx.Button(
            self.panel, label="关闭", pos=(520, 500), size=(80, -1)
        )
        self.hide_button.Bind(wx.EVT_BUTTON, self.hide_Template_Frame)

    def template_text(self, event):
        print("该功能无法使用!仅定制版包含此功能!")
        wx.MessageBox("该功能无法使用!\n仅定制版包含此功能!", "错误", wx.OK | wx.ICON_ERROR)
        # self.text_ctrl.SetValue("")
        # self.font_size_input.SetValue(18)
        # self.font_weight_combo.SetSelection(0)
        # template_color = self.string_to_color(str("#000000"))
        # print("默认模板字体颜色:", template_color)
        # self.color_label.SetForegroundColour(template_color)
        # self.Refresh()

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
            print("配置文件位置: ", config_path)
            os.remove(config_path)

            # 清空模板编辑窗口的内容
            self.text_ctrl.SetValue("")
            self.font_size_input.SetValue(18)
            self.font_weight_combo.SetSelection(0)
            template_color = self.string_to_color(str("#000000"))
            self.color_label.SetForegroundColour(template_color)
            self.Refresh()
            
            wx.MessageBox("模版删除成功!", "提示", wx.OK | wx.ICON_INFORMATION)
        
        else:
            print("配置文件位置: ", config_path, "未找到模板配置文件")
            wx.MessageBox("未找到模板配置文件!", "警告", wx.OK | wx.ICON_WARNING)

    def get_config_path(self):
        appdata_dir = os.getenv("APPDATA") or os.path.expanduser("~")
        config_dir = os.path.join(appdata_dir, name)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, "config.json")

    def save_template(self, data):
        try:
            config_path = self.get_config_path()
            print("配置文件位置: ", config_path)
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
                print("配置文件位置: ", config_path)
                with open(config_path, "r") as f:
                    loaded_data = json.load(f)
                    self.text_ctrl.SetValue(loaded_data["text_value"])
                    self.font_size_input.SetValue(loaded_data["font_size_value"])
                    self.font_weight_combo.SetSelection(loaded_data["font_weight_value"])
                    loaded_color = self.string_to_color(str(loaded_data["color_value"]))
                    print("模板字体颜色:", loaded_color)
                    self.color_label.SetForegroundColour(loaded_color)
                    self.Refresh()
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
