@echo off

set folderName=%1
if "%folderName%"=="" (
  echo  set the new Source dir Name. the dir will create in the Engine directory.
  goto End 
)
set slnName=%2
if "%slnName%"==""  (
  echo  set the create sln file name.
  goto End
)

set folder="%cd%\Engine\%1"
echo create dir in path : %folder%
md %folder%

set RuntimeDir="%cd%\Engine\%1\Runtime"
echo create dir : %RuntimeDir%
md %RuntimeDir%

set DeveloperDir="%cd%\Engine\%1\Developer"
echo create dir : %DeveloperDir%
md %DeveloperDir%

set EditorDir="%cd%\Engine\%1\Editor"
echo create dir : %EditorDir%
md %EditorDir%


xcopy ".\Engine\Source\Runtime"   %RuntimeDir% /e
xcopy ".\Engine\Source\Developer"  %DeveloperDir%   /e
xcopy ".\Engine\Source\Editor" %EditorDir%   /e
copy ".\Engine\Source\UnrealGame.Target.cs" %folder% 
copy "TestApp.Target.cs" %folder%

REM Install PS4 visualizer if the SDK and installation file are present
if exist "%~dp0Engine\Extras\VisualStudio[Debugging\PS4\InstallPS4Visualizer.bat" (
  call "%~dp0Engine\Extras\VisualStudioDebugging\PS4\InstallPS4Visualizer.bat"
)

if not exist "%~dp0Engine\Build\BatchFiles\GenerateProjectFiles.bat" goto Error_BatchFileInWrongLocation
call "%~dp0Engine\Build\BatchFiles\GenerateProjectFiles.bat" "-SourceDir=%folder%"   "-ProjectName=%2"
exit /B %ERRORLEVEL%

:Error_NOPYFile
echo can not find changeSource file.



:Error_BatchFileInWrongLocation
echo GenerateProjectFiles ERROR: The batch file does not appear to be located in the root UE4 directory.  This script must be run from within that directory.
pause
exit /B 1



:End
