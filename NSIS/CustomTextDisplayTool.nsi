; �ýű�ʹ�� HM VNISEdit �ű��༭���򵼲���

; ��װ�����ʼ���峣��
!define PRODUCT_NAME "�Զ����ı��������"
!define PRODUCT_VERSION "2.7"
!define PRODUCT_PUBLISHER "Wilson.Huang"
!define PRODUCT_WEB_SITE "https://github.com/WilsonHuangDev/Custom-Text-Display-Tool"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\CustomTextDisplayTool.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; ------ MUI �ִ����涨�� (1.67 �汾���ϼ���) ------
!include "MUI.nsh"
!include "nsProcess.nsh"

; MUI Ԥ���峣��
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-uninstall.ico"
;�޸����ͼƬ
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\nsis3-metro.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange-uninstall.bmp"
;�޸�HeadͼƬ
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\orange.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\orange-uninstall.bmp"

; ��ӭҳ��
!insertmacro MUI_PAGE_WELCOME
; ���Э��ҳ��
!define MUI_LICENSEPAGE_RADIOBUTTONS
!insertmacro MUI_PAGE_LICENSE "..\CustomTextDisplayTool\LICENCE.rtf"
; ��װĿ¼ѡ��ҳ��
!insertmacro MUI_PAGE_DIRECTORY
; ��װ����ҳ��
!insertmacro MUI_PAGE_INSTFILES
; ��װ���ҳ��
!define MUI_FINISHPAGE_RUN "$INSTDIR\Bin\CustomTextDisplayTool.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\README.rtf"
!insertmacro MUI_PAGE_FINISH

; ��װж�ع���ҳ��
!insertmacro MUI_UNPAGE_INSTFILES

; ��װ�����������������
!insertmacro MUI_LANGUAGE "SimpChinese"

; ��װԤ�ͷ��ļ�
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

;��дMacro�������жϰ�װ��ж�س���ʱָ�������Ƿ������У�����ʾ�Ƿ�ǿ�ƹرռ�����װ
!macro FindProcessAndKill
    StrCpy $1 "CustomTextDisplayTool.exe"
    nsProcess::_FindProcess "$1"
    Pop $R0
    ${If} $R0 = 0
          MessageBox MB_OKCANCEL|MB_ICONQUESTION   \
                     "��װ�����⵽ ${PRODUCT_NAME} �������С�$\r$\n$\r$\n��� ��ȷ���� ǿ�ƹر�${PRODUCT_NAME}��������װ��$\r$\n$\r$\n��� ��ȡ���� �˳���װ����" \
                     /SD IDOK IDOK label_ok IDCANCEL label_cancel
          label_ok:
                   nsProcess::_KillProcess "CustomTextDisplayTool.exe"
                   Goto end
          label_cancel:
                   Abort
    ${EndIf}
    end:
!macroend

; ------ MUI �ִ����涨����� ------

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
  CreateDirectory "$SMPROGRAMS\�Զ����ı��������"
  CreateShortCut "$SMPROGRAMS\�Զ����ı��������\�Զ����ı��������.lnk" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  CreateShortCut "$SMPROGRAMS\�Զ����ı��������\Github �ֿ�.lnk" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\�Զ����ı��������\�����ļ�.lnk" "$INSTDIR\README.rtf"
  CreateShortCut "$DESKTOP\�Զ����ı��������.lnk" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
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
  CreateShortCut "$SMPROGRAMS\�Զ����ı��������\ж��.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\Bin\CustomTextDisplayTool.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

/******************************
 *  �����ǰ�װ�����ж�ز���  *
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

  Delete "$SMPROGRAMS\�Զ����ı��������\ж��.lnk"
  Delete "$SMPROGRAMS\�Զ����ı��������\�Զ����ı��������.lnk"
  Delete "$DESKTOP\�Զ����ı��������.lnk"
  Delete "$SMPROGRAMS\�Զ����ı��������\Github �ֿ�.lnk"
  Delete "$SMPROGRAMS\�Զ����ı��������\�����ļ�.lnk"

  RMDir "$SMPROGRAMS\�Զ����ı��������"
  RMDir "$INSTDIR\Bin\_internal\wx"
  RMDir "$INSTDIR\Bin\_internal"
  RMDir "$INSTDIR\Bin"
  RMDir "$APPDATA\CustomTextDisplayTool"

  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd

#-- ���� NSIS �ű��༭�������� Function ���α�������� Section ����֮���д���Ա��ⰲװ�������δ��Ԥ֪�����⡣--#

Var UNINSTALL_PROG

Function .onInit
	;���ָ�������Ƿ�������
  !insertmacro FindProcessAndKill
  ClearErrors
  ReadRegStr $UNINSTALL_PROG ${PRODUCT_UNINST_ROOT_KEY} ${PRODUCT_UNINST_KEY} "UninstallString"
  IfErrors  done

  MessageBox MB_YESNO|MB_ICONQUESTION \
    "��⵽�Ѿ���װ�� ${PRODUCT_NAME}��\
    $\n$\n�Ƿ���ж���Ѱ�װ�İ汾��" \
      /SD IDYES \
      IDYES uninstall \
      IDNO cancel
  Abort

uninstall:
  CreateDirectory $TEMP
  CopyFiles $UNINSTALL_PROG "$TEMP\uninst.exe"

  ExecWait '"$TEMP\uninst.exe" /S _?=$TEMP' $0
  DetailPrint "uninst.exe returned $0"
  Delete "$TEMP\uninst.exe"
	Goto  done

cancel:
	MessageBox MB_ICONSTOP|MB_OK "$(^Name) ��ȡ����װ��"
  Quit

done:
FunctionEnd

Function un.onInit
	;���ָ�������Ƿ�������
  !insertmacro FindProcessAndKill
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "��ȷʵҪ��ȫ�Ƴ� $(^Name) ���������е������" IDYES +2
  Abort
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) �ѳɹ��ش����ļ�����Ƴ���"
FunctionEnd
