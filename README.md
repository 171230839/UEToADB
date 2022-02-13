# UEToADE
通过修改 虚幻引擎的 一些代码， 将其改造成一个便于开发3d应用的平台。比如说带3d的一些设计应用。一般情况下，只需要修改虚幻引擎的源码中source文件夹的一部分模块，就可以实现一个新的3d应用，但虚幻引擎本身很笨重，十分占用硬盘空间。如果没创建一个应用就创建一个新的虚幻引擎目录，实在是太浪费硬盘空间。这个项目就是为了解决这个问题，最终到达的效果是，控制调用脚本（GenerateProjectFilesNew.bat) 传入2个参数（新源码目录名和sln文件名），就会在 Engine 目录下 创建一个新源码目录，并将 Runtime，Develop， Editor 三个目录拷贝复制过去，并生成新的sln。打开sln后就可以得到一个新的默认应用。
