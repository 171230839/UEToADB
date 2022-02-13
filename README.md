# UEToADE

## 目的
通过修改 虚幻引擎的 一些代码， 将其改造成一个便于开发3d应用的平台。比如说带3d的一些设计应用。一般情况下，只需要修改虚幻引擎的源码中source文件夹的一部分模块，就可以实现一个新的3d应用，但虚幻引擎本身很笨重，十分占用硬盘空间。如果每创建一个应用就创建一个新的虚幻引擎源码目录，实在是太浪费硬盘空间。这个项目就是为了解决这个问题，在复用所有不需要修改的内容的情况下，创建新的工程。

最终到达的效果是，控制调用脚本（GenerateProjectFilesNew.bat) 传入2个参数（新源码目录名和sln文件名），就会在 Engine 目录下 创建一个新源码目录，并将 Runtime，Develop， Editor 三个目录拷贝复制过去，并生成新的sln。打开sln后就可以得到一个新的默认应用。

## 使用步骤 （windows下使用 vs2019 以及 ue5 源码 的示例)
* 按照虚幻引擎官方教程，下载源码。运行setup.bat安装依赖。

* 拷贝覆盖本仓库UnrealBuildTool文件夹到 /Engine/Source/Programs/UnrealBuildTool.
  主要改动都在ubt里面，使用ue5代码做的测试。其他版本可参照修改。

* 其他文件放到 Engine 同级目录下， 使用控制台 运行 python changeSource.py.
  这个脚本会对Engine目录下的源码进行一次行的修改。 主要是修改模块设置文件（*build.cs）里的目录引用路径。
  
* 使用控制台运行 GenerateProjectFilesNew.bat, （新源码目录名和sln文件名），就会在 Engine 目录下 创建一个新源码目录，并将 Runtime，Develop， Editor 三个目录拷贝复制过去，并生成新的sln。

![image](https://user-images.githubusercontent.com/5336757/153746555-c5210cb5-1097-4e47-b146-978a2828cbb3.png)
  
* 如果没有报错，结果如下图就是成功了

![image](https://user-images.githubusercontent.com/5336757/153746634-9c9fac70-b5fc-4ab9-8d9c-8c9f3f360c53.png)
![image](https://user-images.githubusercontent.com/5336757/153749630-86758665-a360-49ac-bd29-2a8f8aff4027.png)


* 双击sln,打开vs.打开sln工程后就可以得到一个新的默认应用。这个应用会共享 原本的Source目录下的 Programs和 ThirdParty 以及插件目录。 
  修改一下解决方案配置（选择后面带App的）和解决方案平台（win64)。选择启动项目TestApp，启动调试器，经过一段长时间的编译，就会得到一个默认的编辑器。
  
  ![image](https://user-images.githubusercontent.com/5336757/153746762-63429b28-d2f7-45cf-925a-ed7a4e075362.png)
  
## 注意事项
  原本的UnrealEditor目标默认是编译所有模块及插件的，十分耗费时间。为了减少编译时间，在TestApp.build.cs里 设置了	bBuildAllModules = false;
  并修改了ubt内部代码，使新目标默认是只加载相关模块。
  新添加了一种加载插件的方式。通过设置bBuildAllPlugins = false; 目标会不一下加载所有插件。而是通过给 EnablePlugins这个变量容器添加插件名 来指定需要加载的插件。
  比如当编辑器打开 uproject工程时，一般会要求编辑器程序中包含 uproject里设置的插件模块。这时可以通过在TestApp.build.cs中添加 给 EnablePlugins 添加模块来解决这个问题。
  即可以选择像原有的一样加载所有插件，也可以指定需要的一些插件加载，减少编译时间。这个地方根据自己的需要进行修改。
  
  ![image](https://user-images.githubusercontent.com/5336757/153750442-fd4f5d09-a000-4565-a536-a759e97d06d6.png)


