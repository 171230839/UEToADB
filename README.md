# UEToADE

## 目的
通过修改 虚幻引擎的 一些代码， 将其改造成一个便于开发3d应用的平台。比如说带3d的一些设计应用。一般情况下，只需要修改虚幻引擎的源码中source文件夹的一部分模块，就可以实现一个新的3d应用，但虚幻引擎本身很笨重，十分占用硬盘空间。如果每创建一个应用就创建一个新的虚幻引擎源码目录，实在是太浪费硬盘空间。这个项目就是为了解决这个问题，在复用所有不需要修改的内容的情况下，创建新的工程。

最终到达的效果是，控制调用脚本（GenerateProjectFilesNew.bat) 传入2个参数（新源码目录名和sln文件名），就会在 Engine 目录下 创建一个新源码目录，并将 Runtime，Develop， Editor 三个目录拷贝复制过去，并生成新的sln。打开sln后就可以得到一个新的默认应用。

## 使用步骤 （windows下ue5示例)
* 按照虚幻引擎官方教程，下载源码。运行setup.bat安装依赖，运行GenerateProjectFiles.bat得到默认sln文件。

* 拷贝覆盖本仓库UnrealBuildTool文件夹到 /Engine/Source/Programs/UnrealBuildTool.
  主要改动都在ubt里面，使用ue5代码做的测试。其他版本可参照修改。

* 其他文件放到 Engine 同级目录下， 使用控制台 运行 python changeSource.py.
  这个脚本会对Engine目录下的源码进行一次行的修改。 主要是修改模块设置文件（*build.cs）里的目录引用路径。
  
* 使用控制台运行 GenerateProjectFilesNew.bat, （新源码目录名和sln文件名），就会在 Engine 目录下 创建一个新源码目录，并将 Runtime，Develop， Editor 三个目录拷贝复制过去，并生成新的sln。打开   sln后就可以得到一个新的默认应用。这个应用会共享 原本的Source目录下的 Programs和 ThirdParty 以及插件目录。 
