@echo off
::�����ļ�
echo C:\ > trust.txt
echo D:\ >> trust.txt
echo E:\ >> trust.txt
echo F:\ >> trust.txt
echo G:\ >> trust.txt
echo H:\ >> trust.txt
echo I:\ >> trust.txt

::���汾
if exist if exist C:\Windows\SysWOW64\ (
	goto sys64
)else goto sys32

::32λϵͳĿ¼�Ѵ���
:sys32
if exist C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\ (
	move /y trust.txt C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\
) else goto sys32NoDir
goto end

::32λϵͳĿ¼��û����
:sys32NoDir
md C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\
move /y trust.txt C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\
goto end

::64λϵͳĿ¼�Ѵ���
:sys64
if exist C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\ (
	move /y trust.txt C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\
) else goto sys64NoDir
goto end

::64λϵͳĿ¼��û����
:sys64NoDir
md C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\
move /y trust.txt C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\
	
:end
echo ���ز��Ի����������
pause