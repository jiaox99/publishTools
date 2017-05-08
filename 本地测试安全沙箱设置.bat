@echo off
::生成文件
echo C:\ > trust.txt
echo D:\ >> trust.txt
echo E:\ >> trust.txt
echo F:\ >> trust.txt
echo G:\ >> trust.txt
echo H:\ >> trust.txt
echo I:\ >> trust.txt

::检测版本
if exist if exist C:\Windows\SysWOW64\ (
	goto sys64
)else goto sys32

::32位系统目录已存在
:sys32
if exist C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\ (
	move /y trust.txt C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\
) else goto sys32NoDir
goto end

::32位系统目录还没建立
:sys32NoDir
md C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\
move /y trust.txt C:\Windows\System32\Macromed\Flash\FlashPlayerTrust\
goto end

::64位系统目录已存在
:sys64
if exist C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\ (
	move /y trust.txt C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\
) else goto sys64NoDir
goto end

::64位系统目录还没建立
:sys64NoDir
md C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\
move /y trust.txt C:\Windows\SysWOW64\Macromed\Flash\FlashPlayerTrust\
	
:end
echo 本地测试环境设置完成
pause