; 该脚本使用 HM VNISEdit 脚本编辑器向导产生

; 安装程序初始定义常量
!define PRODUCT_NAME "自定义文本输出工具"
!define PRODUCT_PUBLISHER "Wilson.Huang"
!define PRODUCT_WEB_SITE "https://github.com/WilsonHuangDev/Custom-Text-Display-Tool"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\CustomTextDisplayTool.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

Unicode True
SetCompressor lzma

; ------ MUI 现代界面定义 (1.67 版本以上兼容) ------
!include "MUI.nsh"
!include "nsProcess.nsh"

; MUI 预定义常量
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-uninstall.ico"
;修改左侧图片
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\nsis3-metro.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange-uninstall.bmp"
;修改Head图片
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\orange.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\orange-uninstall.bmp"

; 欢迎页面
!insertmacro MUI_PAGE_WELCOME
; 许可协议页面
!define MUI_LICENSEPAGE_RADIOBUTTONS
!insertmacro MUI_PAGE_LICENSE "..\CustomTextDisplayTool\LICENCE.rtf"
; 安装目录选择页面
!insertmacro MUI_PAGE_DIRECTORY
; 安装过程页面
!insertmacro MUI_PAGE_INSTFILES
; 安装完成页面
!define MUI_FINISHPAGE_RUN "$INSTDIR\Bin\CustomTextDisplayTool.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.rtf"
!insertmacro MUI_PAGE_FINISH

; 安装卸载过程页面
!insertmacro MUI_UNPAGE_INSTFILES

; 安装界面包含的语言设置
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SimpChinese"

; 安装预释放文件
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

;编写Macro，用于判断安装或卸载程序时指定程序是否在运行，并提示是否强制关闭继续安装
!macro FindProcessAndKill
    StrCpy $1 "CustomTextDisplayTool.exe"
    nsProcess::_FindProcess "$1"
    Pop $R0
    ${If} $R0 = 0
          MessageBox MB_OKCANCEL|MB_ICONQUESTION   \
                     "安装程序检测到 ${PRODUCT_NAME} 正在运行。$\r$\n$\r$\n点击 “确定” 强制关闭${PRODUCT_NAME}，继续安装。$\r$\n$\r$\n点击 “取消” 退出安装程序。" \
                     /SD IDOK IDOK label_ok IDCANCEL label_cancel
          label_ok:
                   nsProcess::_KillProcess "CustomTextDisplayTool.exe"
                   Goto end
          label_cancel:
									 Abort
    ${EndIf}
    end:
!macroend

; ------ MUI 现代界面定义结束 ------

Name "${PRODUCT_NAME}"
OutFile "CustomTextDisplayTool_Setup.exe"
InstallDir "$PROGRAMFILES\CustomTextDisplayTool"
InstallDirRegKey HKLM "${PRODUCT_UNINST_KEY}" "UninstallString"
ShowInstDetails show
ShowUnInstDetails show
BrandingText "CustomTextDisplayTool"

Section "Main" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on
  File "..\CustomTextDisplayTool\README.rtf"
  File "..\CustomTextDisplayTool\LICENCE.rtf"
  SetOutPath "$INSTDIR\Assets"
  File "..\CustomTextDisplayTool\Assets\icon.ico"
  SetOutPath "$INSTDIR\Bin"
  File "..\CustomTextDisplayTool\Bin\CustomTextDisplayTool.exe"
  CreateShortCut "$DESKTOP\自定义文本输出工具.lnk" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  CreateDirectory "$SMPROGRAMS\自定义文本输出工具"
  CreateShortCut "$SMPROGRAMS\自定义文本输出工具\自定义文本输出工具.lnk" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  CreateShortCut "$SMPROGRAMS\自定义文本输出工具\Github 仓库.lnk" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\自定义文本输出工具\自述文件.lnk" "$INSTDIR\README.rtf"
  SetOutPath "$INSTDIR\Bin\_internal"
  File "..\CustomTextDisplayTool\Bin\_internal\base_library.zip"
  File "..\CustomTextDisplayTool\Bin\_internal\libcrypto-1_1.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\python38.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\select.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\unicodedata.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\VCRUNTIME140.dll"
  SetOutPath "$INSTDIR\Bin\_internal\wx"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\MSVCP140.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\siplib.cp38-win32.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\VCRUNTIME140.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\wxbase32u_net_vc140.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\wxbase32u_vc140.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\wxmsw32u_core_vc140.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\wxmsw32u_html_vc140.dll"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\_adv.cp38-win32.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\_core.cp38-win32.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\_html.cp38-win32.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\wx\_msw.cp38-win32.pyd"
  SetOutPath "$INSTDIR\Bin\_internal"
  File "..\CustomTextDisplayTool\Bin\_internal\_bz2.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\_hashlib.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\_lzma.pyd"
  File "..\CustomTextDisplayTool\Bin\_internal\_socket.pyd"
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  CreateShortCut "$SMPROGRAMS\自定义文本输出工具\卸载.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

/******************************
 *  以下是安装程序的卸载部分  *
 ******************************/

Section Uninstall
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\Bin\_internal\_socket.pyd"
  Delete "$INSTDIR\Bin\_internal\_lzma.pyd"
  Delete "$INSTDIR\Bin\_internal\_hashlib.pyd"
  Delete "$INSTDIR\Bin\_internal\_bz2.pyd"
  Delete "$INSTDIR\Bin\_internal\wx\_msw.cp38-win32.pyd"
  Delete "$INSTDIR\Bin\_internal\wx\_html.cp38-win32.pyd"
  Delete "$INSTDIR\Bin\_internal\wx\_core.cp38-win32.pyd"
  Delete "$INSTDIR\Bin\_internal\wx\_adv.cp38-win32.pyd"
  Delete "$INSTDIR\Bin\_internal\wx\wxmsw32u_html_vc140.dll"
  Delete "$INSTDIR\Bin\_internal\wx\wxmsw32u_core_vc140.dll"
  Delete "$INSTDIR\Bin\_internal\wx\wxbase32u_vc140.dll"
  Delete "$INSTDIR\Bin\_internal\wx\wxbase32u_net_vc140.dll"
  Delete "$INSTDIR\Bin\_internal\wx\VCRUNTIME140.dll"
  Delete "$INSTDIR\Bin\_internal\wx\siplib.cp38-win32.pyd"
  Delete "$INSTDIR\Bin\_internal\wx\MSVCP140.dll"
  Delete "$INSTDIR\Bin\_internal\VCRUNTIME140.dll"
  Delete "$INSTDIR\Bin\_internal\unicodedata.pyd"
  Delete "$INSTDIR\Bin\_internal\select.pyd"
  Delete "$INSTDIR\Bin\_internal\python38.dll"
  Delete "$INSTDIR\Bin\_internal\libcrypto-1_1.dll"
  Delete "$INSTDIR\Bin\_internal\base_library.zip"
  Delete "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  Delete "$INSTDIR\Assets\icon.ico"
  Delete "$INSTDIR\LICENCE.rtf"
  Delete "$INSTDIR\README.rtf"
  Delete "$APPDATA\CustomTextDisplayTool\config.json"

  Delete "$SMPROGRAMS\自定义文本输出工具\卸载.lnk"
  Delete "$SMPROGRAMS\自定义文本输出工具\自定义文本输出工具.lnk"
  Delete "$DESKTOP\自定义文本输出工具.lnk"
  Delete "$SMPROGRAMS\自定义文本输出工具\Github 仓库.lnk"
  Delete "$SMPROGRAMS\自定义文本输出工具\自述文件.lnk"

  RMDir /r "$SMPROGRAMS\自定义文本输出工具"
  RMDir /r "$INSTDIR\Bin\_internal\wx"
  RMDir /r "$INSTDIR\Bin\_internal"
  RMDir /r "$INSTDIR\Bin"
  RMDir /r "$APPDATA\CustomTextDisplayTool"

  RMDir /r "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd

#-- 根据 NSIS 脚本编辑规则，所有 Function 区段必须放置在 Section 区段之后编写，以避免安装程序出现未可预知的问题。--#

Var UNINSTALL_PROG

Function .onInit
  ClearErrors
  ReadRegStr $UNINSTALL_PROG ${PRODUCT_UNINST_ROOT_KEY} ${PRODUCT_UNINST_KEY} "UninstallString"
  IfErrors  done

  MessageBox MB_YESNO|MB_ICONQUESTION \
    "检测到已经安装了 ${PRODUCT_NAME}。\
    $\n$\n是否先卸载已安装的版本？" \
      /SD IDYES \
      IDYES uninstall \
      IDNO cancel
	Abort

uninstall:
	CreateDirectory "$TEMP"
	CopyFiles "$INSTDIR\uninst.exe" "$TEMP"
  ExecWait '"$TEMP\uninst.exe" _?=$INSTDIR' $0
  DetailPrint "uninst.exe returned $0"
	Goto  done

cancel:
	MessageBox MB_ICONSTOP|MB_OK "$(^Name) 已取消安装。"
	Abort

done:
FunctionEnd

Function un.onInit
	;检查指定程序是否在运行
  !insertmacro FindProcessAndKill
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "您确实要完全移除 $(^Name) ，及其所有的组件？" IDYES +2
  Abort
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) 已成功地从您的计算机移除。"
FunctionEnd