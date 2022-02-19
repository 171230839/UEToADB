
# -*- coding:utf8 -*-


import os, re, time, fnmatch, difflib, sys
from chardet import detect

# get file encoding type
def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']
RE_TYPE = type(re.compile(""))
class SearchAndReplace(object):
  def __init__(self, search_path, search_string, replace_string,
                    search_only=True, file_filter=("*.*",)):
    self.search_path = search_path
    self.search_string = search_string
    self.replace_string = replace_string
    self.search_only = search_only
    self.file_filter = file_filter
    assert isinstance(self.file_filter, (list, tuple))
    # FIXME: see http://stackoverflow.com/questions/4730121/cant-get-an-objects-class-name-in-python
    self.is_re = isinstance(self.search_string, RE_TYPE)
    print("Search '%s' in [%s]..." % (
      self.search_string, self.search_path
    ))
    print("_" * 80)
    time_begin = time.time()
    file_count = self.walk()
    print("_" * 80)
    print("%s files searched in %0.2fsec." % (
      file_count, (time.time() - time_begin)
    ))
  def walk(self):
    file_count = 0
    for root, dirlist, filelist in os.walk(self.search_path):
      if ".svn" in root:
        continue
      for filename in filelist:
        for file_filter in self.file_filter:
          if fnmatch.fnmatch(filename, file_filter):
            self.search_file(os.path.join(root, filename))
            file_count += 1
    return file_count
  def search_file(self, filepath):
    f = open(filepath, "r", encoding=get_encoding_type(filepath) ,errors="ignore")
    old_content = f.read()
    f.close()
    if self.is_re or self.search_string in old_content:
      new_content = self.replace_content(old_content, filepath)
      if self.is_re and new_content == old_content:
        return
      print(filepath)
      self.display_plaintext_diff(old_content, new_content)
  def replace_content(self, old_content, filepath):
    if self.is_re:
      new_content = self.search_string.sub(self.replace_string, old_content)
      if new_content == old_content:
        return old_content
    else:
      new_content = old_content.replace(
        self.search_string, self.replace_string
      )
    if self.search_only != False:
      return new_content
    print("Write new content into %s..." % filepath, end=' ')
    try:
      f = open(filepath, "w")
      f.write(new_content)
      f.close()
    except IOError as msg:
      print("Error:", msg)
    else:
      print("OK")
    print()
    return new_content
  def display_plaintext_diff(self, content1, content2):
    """
    Display a diff.
    """
    content1 = content1.splitlines()
    content2 = content2.splitlines()
    diff = difflib.Differ().compare(content1, content2)
    def is_diff_line(line):
      for char in ("-", "+", "?"):
        if line.startswith(char):
          return True
      return False
    print("line | text\n-------------------------------------------")
    old_line = ""
    in_block = False
    old_lineno = lineno = 0
    for line in diff:
      if line.startswith(" ") or line.startswith("+"):
        lineno += 1
      if old_lineno == lineno:
        display_line = "%4s | %s" % ("", line.rstrip())
      else:
        display_line = "%4s | %s" % (lineno, line.rstrip())
      if is_diff_line(line):
        if not in_block:
          print("...")
          # Display previous line
          print(old_line)
          in_block = True
        print(display_line)
      else:
        if in_block:
          # Display the next line aber a diff-block
          print(display_line)
        in_block = False
      old_line = display_line
      old_lineno = lineno
    print("...")


if __name__ == "__main__":
    path = "./Engine/Source/Programs/UnrealBuildTool/Configuration"
    SearchAndReplace(search_path=path, search_string='''/// <summary>
			/// Any targets.
			/// </summary>
			Any,''',
        replace_string='''/// <summary>
			/// Any targets.
			/// </summary>
			Any,

			App,''',
        search_only=False,
        file_filter=("ModuleRules.cs",))
    SearchAndReplace(search_path=path, search_string='''/// <summary>
			/// Any targets.
			/// </summary>
			Any,

			App,

			App,''',
        replace_string='''/// <summary>
			/// Any targets.
			/// </summary>
			Any,

			App,''',
        search_only=False,
        file_filter=("ModuleRules.cs",))

    SearchAndReplace(search_path=path, search_string='''/// <summary>
		/// Constructor. For backwards compatibility while the parameterless constructor is being phased out, initialization which would happen here is done by 
		/// RulesAssembly.CreateModulRules instead.
		/// </summary>
		/// <param name="Target">Rules for building this target</param>
		public ModuleRules(ReadOnlyTargetRules Target)
		{
			this.Target = Target;''',
        replace_string='''public String  EngineSourceDir = "";
		public String  ThirdPartyDir = "";
		/// <summary>
		/// Constructor. For backwards compatibility while the parameterless constructor is being phased out, initialization which would happen here is done by 
		/// RulesAssembly.CreateModulRules instead.
		/// </summary>
		/// <param name="Target">Rules for building this target</param>
		public ModuleRules(ReadOnlyTargetRules Target)
		{
			this.Target = Target;
			this.EngineSourceDir = Target.UEEngineSourceDirectory;
			this.ThirdPartyDir = Target.UEThirdPartySourceDirectory;''',
        search_only=False,
        file_filter=("ModuleRules.cs",))
    SearchAndReplace(search_path=path, search_string='''public String  EngineSourceDir = "";
		public String  ThirdPartyDir = "";
		public String  EngineSourceDir = "";
		public String  ThirdPartyDir = "";
		/// <summary>
		/// Constructor. For backwards compatibility while the parameterless constructor is being phased out, initialization which would happen here is done by 
		/// RulesAssembly.CreateModulRules instead.
		/// </summary>
		/// <param name="Target">Rules for building this target</param>
		public ModuleRules(ReadOnlyTargetRules Target)
		{
			this.Target = Target;
			this.EngineSourceDir = Target.UEEngineSourceDirectory;
			this.ThirdPartyDir = Target.UEThirdPartySourceDirectory;
			this.EngineSourceDir = Target.UEEngineSourceDirectory;
			this.ThirdPartyDir = Target.UEThirdPartySourceDirectory;''',
        replace_string='''public String  EngineSourceDir = "";
		public String  ThirdPartyDir = "";
		/// <summary>
		/// Constructor. For backwards compatibility while the parameterless constructor is being phased out, initialization which would happen here is done by 
		/// RulesAssembly.CreateModulRules instead.
		/// </summary>
		/// <param name="Target">Rules for building this target</param>
		public ModuleRules(ReadOnlyTargetRules Target)
		{
			this.Target = Target;
			this.EngineSourceDir = Target.UEEngineSourceDirectory;
			this.ThirdPartyDir = Target.UEThirdPartySourceDirectory;''',
        search_only=False,
        file_filter=("ModuleRules.cs",))


    SearchAndReplace(search_path=path, search_string='''	case ModuleRules.PrecompileTargetsType.Default:
						return (Target.Type == TargetType.Editor || !UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineDirectory, "Source/Developer").Any(Dir => RulesFile.IsUnderDirectory(Dir)) || Plugin != null);
					case ModuleRules.PrecompileTargetsType.Game:
						return (Target.Type == TargetType.Client || Target.Type == TargetType.Server || Target.Type == TargetType.Game);
					case ModuleRules.PrecompileTargetsType.Editor:
						return (Target.Type == TargetType.Editor);''',
        replace_string='''	case ModuleRules.PrecompileTargetsType.Default:
						return (Target.Type == TargetType.Editor ||  Target.Type == TargetType.App || !UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineSourceDirectory, "Developer").Any(Dir => RulesFile.IsUnderDirectory(Dir)) || Plugin != null);
					case ModuleRules.PrecompileTargetsType.Game:
						return (Target.Type == TargetType.Client || Target.Type == TargetType.Server || Target.Type == TargetType.Game);
					case ModuleRules.PrecompileTargetsType.Editor:
						return (Target.Type == TargetType.Editor) ;
					case ModuleRules.PrecompileTargetsType.App:
						return (Target.Type == TargetType.App);''',
        search_only=False,
        file_filter=("ModuleRules.cs",))

    SearchAndReplace(search_path=path, search_string='''/// <summary>
		/// Program (standalone program, e.g. ShaderCompileWorker.exe, can be modular or monolithic depending on the program)
		/// </summary>
		Program,''',
        replace_string='''/// <summary>
		/// Program (standalone program, e.g. ShaderCompileWorker.exe, can be modular or monolithic depending on the program)
		/// </summary>
		Program,

		App,''',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='''/// <summary>
		/// Program (standalone program, e.g. ShaderCompileWorker.exe, can be modular or monolithic depending on the program)
		/// </summary>
		Program,

		App,

		App,''',
        replace_string='''/// <summary>
		/// Program (standalone program, e.g. ShaderCompileWorker.exe, can be modular or monolithic depending on the program)
		/// </summary>
		Program,

		App,''',
        search_only=False,
        file_filter=("TargetRules.cs",))  


    SearchAndReplace(search_path=path, search_string='''public const global::UnrealBuildTool.TargetType Program = global::UnrealBuildTool.TargetType.Program;''',
        replace_string='''public const global::UnrealBuildTool.TargetType Program = global::UnrealBuildTool.TargetType.Program;
			public const global::UnrealBuildTool.TargetType App = global::UnrealBuildTool.TargetType.App;''',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='''public const global::UnrealBuildTool.TargetType Program = global::UnrealBuildTool.TargetType.Program;
			public const global::UnrealBuildTool.TargetType App = global::UnrealBuildTool.TargetType.App;
			public const global::UnrealBuildTool.TargetType App = global::UnrealBuildTool.TargetType.App;''',
        replace_string='''public const global::UnrealBuildTool.TargetType Program = global::UnrealBuildTool.TargetType.Program;
			public const global::UnrealBuildTool.TargetType App = global::UnrealBuildTool.TargetType.App;''',
        search_only=False,
        file_filter=("TargetRules.cs",))



    SearchAndReplace(search_path=path, search_string='''[Obsolete("bBuildAllPlugins has been deprecated. Use bPrecompile to build all modules which are not part of the target.")]
		public bool bBuildAllPlugins = false;''',
        replace_string='''public bool bBuildAllPlugins = true;''',
        search_only=False,
        file_filter=("TargetRules.cs",))
   
    SearchAndReplace(search_path=path, search_string='''[Obsolete("bBuildAllPlugins has been deprecated. Use bPrecompile to build all modules which are not part of the target.")]
		public bool bBuildAllPlugins''',
        replace_string='''public bool bBuildAllPlugins''',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='Type == TargetType.Editor',
        replace_string='(Type == TargetType.Editor || Type == TargetType.App)',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='((Type == TargetType.Editor || Type == TargetType.App) || Type == TargetType.App)',
        replace_string='(Type == TargetType.Editor || Type == TargetType.App)',
        search_only=False,
        file_filter=("TargetRules.cs",))

    SearchAndReplace(search_path=path, search_string='Type == global::UnrealBuildTool.TargetType.Editor',
        replace_string='(Type == global::UnrealBuildTool.TargetType.Editor  ||  Type == global::UnrealBuildTool.TargetType.App)',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='((Type == global::UnrealBuildTool.TargetType.Editor  ||  Type == global::UnrealBuildTool.TargetType.App)  ||  Type == global::UnrealBuildTool.TargetType.App)',
        replace_string='(Type == global::UnrealBuildTool.TargetType.Editor  ||  Type == global::UnrealBuildTool.TargetType.App)',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='''public string RelativeEnginePath
		{
			get { return UnrealBuildTool.EngineDirectory.MakeRelativeTo(DirectoryReference.GetCurrentDirectory()); }
		}''',
        replace_string='''public string RelativeEnginePath
		{
			get { return UnrealBuildTool.EngineDirectory.MakeRelativeTo(DirectoryReference.GetCurrentDirectory()); }
		}


		public string UEEngineSourceDirectory
		{
			get { return UnrealBuildTool.EngineSourceDirectory.ToString().Replace("\\\\", "/") + "/"; }
		}''',
        search_only=False,
        file_filter=("TargetRules.cs",))
    SearchAndReplace(search_path=path, search_string='''public string RelativeEnginePath
		{
			get { return UnrealBuildTool.EngineDirectory.MakeRelativeTo(DirectoryReference.GetCurrentDirectory()); }
		}


		public string UEEngineSourceDirectory
		{
			get { return UnrealBuildTool.EngineSourceDirectory.ToString().Replace("\\\\", "/") + "/"; }
		}


		public string UEEngineSourceDirectory
		{
			get { return UnrealBuildTool.EngineSourceDirectory.ToString().Replace("\\\\", "/") + "/"; }
		}''',
        replace_string='''public string RelativeEnginePath
		{
			get { return UnrealBuildTool.EngineDirectory.MakeRelativeTo(DirectoryReference.GetCurrentDirectory()); }
		}


		public string UEEngineSourceDirectory
		{
			get { return UnrealBuildTool.EngineSourceDirectory.ToString().Replace("\\\\", "/") + "/"; }
		}''',
        search_only=False,
        file_filter=("TargetRules.cs",))
    
    SearchAndReplace(search_path=path, search_string='''		public string UEThirdPartySourceDirectory
		{
			get { return "ThirdParty/"; }
		}''',
        replace_string='''		public string UEThirdPartySourceDirectory
		{
			get { return UnrealBuildTool.EngineSourceThirdPartyDirectory.ToString().Replace("\\\\","/") + "/"; }
		}

		public string UEProgramsSourceDirectory
		{
			get { return UnrealBuildTool.EngineSourceProgramsDirectory.ToString().Replace("\\\\", "/") + "/"; }
		}''',
        search_only=False,
        file_filter=("TargetRules.cs",))


    SearchAndReplace(search_path=path, search_string='''case TargetType.Server:
					BaseTargetName = "UnrealServer";
					break;''',
        replace_string='''case TargetType.Server:
					BaseTargetName = "UnrealServer";
					break;
				case TargetType.App:
					BaseTargetName = ThisTargetName;
					break;''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''				case TargetType.Server:
					BaseTargetName = "UE4Server";
					break;''',
        replace_string='''				case TargetType.Server:
					BaseTargetName = "Un4Server";
					break;
				case TargetType.App:
					BaseTargetName = ThisTargetName;
					break;''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''if (bUseSharedBuildEnvironment)
			{
				if(Rules.Type == TargetType.Program)''',
        replace_string='''if (bUseSharedBuildEnvironment)
			{
				if(Rules.Type == TargetType.Program || TargetType == TargetType.App)''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''	foreach (DirectoryReference ExtensionDir in UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineDirectory))
				{
					DirectoryReference SourceDeveloperDir = DirectoryReference.Combine(ExtensionDir, "Source/Developer");
					if(Module.RulesFile.IsUnderDirectory(SourceDeveloperDir))
					{
						return false;
					}

					DirectoryReference SourceEditorDir = DirectoryReference.Combine(ExtensionDir, "Source/Editor");
					if(Module.RulesFile.IsUnderDirectory(SourceEditorDir))
					{
						return false;
					}
				}''',
        replace_string='''DirectoryReference SourceDeveloperDir = DirectoryReference.Combine(UnrealBuildTool.EngineSourceDirectory, "Developer");
					if(Module.RulesFile.IsUnderDirectory(SourceDeveloperDir))
					{
						return false;
					}

					DirectoryReference SourceEditorDir = DirectoryReference.Combine(UnrealBuildTool.EngineSourceDirectory, "Editor");
					if(Module.RulesFile.IsUnderDirectory(SourceEditorDir))
					{
						return false;
					}''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.EngineDirectory, "Source/''',
        replace_string='''UnrealBuildTool.EngineSourceDirectory, "''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''// Add all the plugin modules that need to be compiled
			List<PluginInfo> Plugins = RulesAssembly.EnumeratePlugins().ToList();''',
        replace_string='''			// Add all the plugin modules that need to be compiled
			if (Rules.bBuildAllPlugins)
			{
				List<PluginInfo> Plugins = RulesAssembly.EnumeratePlugins().ToList();''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''// Create rules for each remaining module, and check that it's set to be compiled
			foreach(string FilteredModuleName in FilteredModuleNames)''',
        replace_string='''}
			
			// Create rules for each remaining module, and check that it's set to be compiled
			foreach (string FilteredModuleName in FilteredModuleNames)''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''bool bAllowEnginePluginsEnabledByDefault = true;''',
        replace_string='''bool bAllowEnginePluginsEnabledByDefault = Rules.bBuildAllPlugins;''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='''GlobalCompileEnvironment.UserIncludePaths.Add(UnrealBuildTool.EngineSourceDirectory);''',
        replace_string='''GlobalCompileEnvironment.UserIncludePaths.Add(UnrealBuildTool.EngineSourceDirectory);

			GlobalCompileEnvironment.UserIncludePaths.Add(UnrealBuildTool.EngineSourceThirdPartyDirectory);''',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))


    SearchAndReplace(search_path=path, search_string='ThisRules.Type == TargetType.Editor',
        replace_string='(ThisRules.Type == TargetType.Editor || ThisRules.Type == TargetType.App)',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='((ThisRules.Type == TargetType.Editor || ThisRules.Type == TargetType.App) || ThisRules.Type == TargetType.App)',
        replace_string='(ThisRules.Type == TargetType.Editor || ThisRules.Type == TargetType.App)',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))

    SearchAndReplace(search_path=path, search_string='Target.Type != TargetType.Editor',
        replace_string='(Target.Type != TargetType.Editor && Target.Type != TargetType.App)',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='((Target.Type != TargetType.Editor && Target.Type != TargetType.App) && Target.Type != TargetType.App)',
        replace_string='(Target.Type != TargetType.Editor && Target.Type != TargetType.App)',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))

    SearchAndReplace(search_path=path, search_string='TargetType == TargetType.Editor',
        replace_string='(TargetType == TargetType.Editor || TargetType == TargetType.App)',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))
    SearchAndReplace(search_path=path, search_string='((TargetType == TargetType.Editor || TargetType == TargetType.App) || TargetType == TargetType.App)',
        replace_string='(TargetType == TargetType.Editor || TargetType == TargetType.App)',
        search_only=False,
        file_filter=("UEBuildTarget.cs",))


    path = "./Engine/Source/Programs/UnrealBuildTool/Modes"

    SearchAndReplace(search_path=path, search_string='''List<string> NamePrefixes = new List<string>();
				if (Target.Type != TargetType.Program)''',
        replace_string='''List<string> NamePrefixes = new List<string>();
				if (Target.Type != TargetType.Program && Target.Type != TargetType.App)''',
        search_only=False,
        file_filter=("CleanMode.cs",))



    SearchAndReplace(search_path=path, search_string='''[CommandLine("-Automated")]
		bool bAutomated = false;''',
        replace_string='''[CommandLine("-Automated")]
		bool bAutomated = false;

		[CommandLine("-ProjectName")]
		string ProjectName = "";''',
        search_only=False,
        file_filter=("GenerateProjectFilesMode.cs",))
    SearchAndReplace(search_path=path, search_string='''[CommandLine("-Automated")]
		bool bAutomated = false;

		[CommandLine("-ProjectName")]
		string ProjectName = "";

		[CommandLine("-ProjectName")]
		string ProjectName = "";''',
        replace_string='''[CommandLine("-Automated")]
		bool bAutomated = false;

		[CommandLine("-ProjectName")]
		string ProjectName = "";''',
        search_only=False,
        file_filter=("GenerateProjectFilesMode.cs",))



    SearchAndReplace(search_path=path, search_string='''Generators.Add(Generator);''',
        replace_string='''if (!string.IsNullOrEmpty(ProjectName))
				{
					Generator.MasterProjectName = ProjectName;
					ProjectFileGenerator.EngineProjectFileNameBase = ProjectName;
				}
				Generators.Add(Generator);''',
        search_only=False,
        file_filter=("GenerateProjectFilesMode.cs",))
    SearchAndReplace(search_path=path, search_string='''if (!string.IsNullOrEmpty(ProjectName))
				{
					Generator.MasterProjectName = ProjectName;
					ProjectFileGenerator.EngineProjectFileNameBase = ProjectName;
				}
				if (!string.IsNullOrEmpty(ProjectName))
				{
					Generator.MasterProjectName = ProjectName;
					ProjectFileGenerator.EngineProjectFileNameBase = ProjectName;
				}
				Generators.Add(Generator);''',
        replace_string='''if (!string.IsNullOrEmpty(ProjectName))
				{
					Generator.MasterProjectName = ProjectName;
					ProjectFileGenerator.EngineProjectFileNameBase = ProjectName;
				}
				Generators.Add(Generator);''',
        search_only=False,
        file_filter=("GenerateProjectFilesMode.cs",))   


    path = "./Engine/Source/Programs/UnrealBuildTool/ProjectFiles"
    SearchAndReplace(search_path=path, search_string='''public const string EngineProjectFileNameBase''',
        replace_string='''public  static string EngineProjectFileNameBase''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''protected string MasterProjectName''',
        replace_string='''public string MasterProjectName''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''DirectoryReference.Combine(UnrealBuildTool.EngineSourceDirectory, "Programs",''',
        replace_string='''DirectoryReference.Combine(UnrealBuildTool.EngineSourceProgramsDirectory,''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineDirectory, "Source/Programs");''',
        replace_string='''UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineSourceProgramsDirectory);''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''{
				if( IncludeEnginePrograms )''',
        replace_string='''{
				if( IncludeEnginePrograms && (ProgramProjects.Count() != 0))''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''SubdirectoryNamesToExclude.Add("Content");''',
        replace_string='''SubdirectoryNamesToExclude.Add("Content");
						if (UnrealBuildTool.EngineSourceDirectory != DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
						{
							SubdirectoryNamesToExclude.Add("Source");
						}''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''SubdirectoryNamesToExclude.Add("Content");
						if (UnrealBuildTool.EngineSourceDirectory != DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
						{
							SubdirectoryNamesToExclude.Add("Source");
						}
						if (UnrealBuildTool.EngineSourceDirectory != DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
						{
							SubdirectoryNamesToExclude.Add("Source");
						}''',
        replace_string='''SubdirectoryNamesToExclude.Add("Content");
						if (UnrealBuildTool.EngineSourceDirectory != DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
						{
							SubdirectoryNamesToExclude.Add("Source");
						}''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))



    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.EngineDirectory, "Source"''',
        replace_string='''UnrealBuildTool.EngineSourceDirectory''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='ProjectTarget.TargetRules.Type == TargetType.Editor',
        replace_string='(ProjectTarget.TargetRules.Type == TargetType.Editor  || ProjectTarget.TargetRules.Type == TargetType.App)',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='((ProjectTarget.TargetRules.Type == TargetType.Editor  || ProjectTarget.TargetRules.Type == TargetType.App)  || ProjectTarget.TargetRules.Type == TargetType.App)',
        replace_string='(ProjectTarget.TargetRules.Type == TargetType.Editor  || ProjectTarget.TargetRules.Type == TargetType.App)',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))

    SearchAndReplace(search_path=path, search_string='TargetRulesObject.Type != TargetType.Editor',
        replace_string='(TargetRulesObject.Type != TargetType.Editor && TargetRulesObject.Type != TargetType.App)',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='((TargetRulesObject.Type != TargetType.Editor && TargetRulesObject.Type != TargetType.App) && TargetRulesObject.Type != TargetType.App)',
        replace_string='(TargetRulesObject.Type != TargetType.Editor && TargetRulesObject.Type != TargetType.App)',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))

    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.EngineSourceDirectory, "Programs"''',
        replace_string='''UnrealBuildTool.EngineSourceProgramsDirectory''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.EngineDirectory, "Source/Programs"''',
        replace_string='''UnrealBuildTool.EngineSourceProgramsDirectory''',
        search_only=False,
        file_filter=("ProjectFileGenerator.cs",))

    path = "./Engine/Source/Programs/UnrealBuildTool/ProjectFiles/VisualStudio/"
    SearchAndReplace(search_path=path, search_string='''SolutionTarget == TargetType.Editor''',
        replace_string='''(SolutionTarget == TargetType.Editor || SolutionTarget == TargetType.App)''',
        search_only=False,
        file_filter=("VCProject.cs",))
    SearchAndReplace(search_path=path, search_string='''((SolutionTarget == TargetType.Editor || SolutionTarget == TargetType.App) || SolutionTarget == TargetType.App)''',
        replace_string='''(SolutionTarget == TargetType.Editor || SolutionTarget == TargetType.App)''',
        search_only=False,
        file_filter=("VCProject.cs",))

    SearchAndReplace(search_path=path, search_string='''					if (!bShouldCompileMonolithic && TargetRulesObject.Type != TargetType.Program && TargetRulesObject.BuildEnvironment != TargetBuildEnvironment.Unique)
					{
						BaseExeName = "Unreal" + TargetRulesObject.Type.ToString();
					}''',
        replace_string='''					// if (!bShouldCompileMonolithic && TargetRulesObject.Type != TargetType.Program && TargetRulesObject.BuildEnvironment != TargetBuildEnvironment.Unique)
					// {
					// 	BaseExeName = "Unreal" + TargetRulesObject.Type.ToString();
					// }''',
        search_only=False,
        file_filter=("VCProject.cs",))

    SearchAndReplace(search_path=path, search_string='''					if (!bShouldCompileMonolithic && TargetRulesObject.Type != TargetType.Program && TargetRulesObject.BuildEnvironment != TargetBuildEnvironment.Unique)
					{
						BaseExeName = "UE4" + TargetRulesObject.Type.ToString();
					}''',
        replace_string='''					// if (!bShouldCompileMonolithic && TargetRulesObject.Type != TargetType.Program && TargetRulesObject.BuildEnvironment != TargetBuildEnvironment.Unique)
					// {
					// 	BaseExeName = "Unreal" + TargetRulesObject.Type.ToString();
					// }''',
        search_only=False,
        file_filter=("VCProject.cs",))
    SearchAndReplace(search_path=path, search_string='''DirectoryReference BatchFilesDirectory = DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Build", "BatchFiles");
''',
        replace_string='''if (UnrealBuildTool.EngineSourceDirectory !=   DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
					{
						BuildArguments.AppendFormat(" -SourceDir={0}", UnrealBuildTool.EngineSourceDirectory);
					}


					DirectoryReference BatchFilesDirectory = DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Build", "BatchFiles");''',
        search_only=False,
        file_filter=("VCProject.cs",))
    SearchAndReplace(search_path=path, search_string='''if (UnrealBuildTool.EngineSourceDirectory !=   DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
					{
						BuildArguments.AppendFormat(" -SourceDir={0}", UnrealBuildTool.EngineSourceDirectory);
					}


					if (UnrealBuildTool.EngineSourceDirectory !=   DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
					{
						BuildArguments.AppendFormat(" -SourceDir={0}", UnrealBuildTool.EngineSourceDirectory);
					}


					DirectoryReference BatchFilesDirectory = DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Build", "BatchFiles");''',
        replace_string='''if (UnrealBuildTool.EngineSourceDirectory !=   DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Source"))
					{
						BuildArguments.AppendFormat(" -SourceDir={0}", UnrealBuildTool.EngineSourceDirectory);
					}


					DirectoryReference BatchFilesDirectory = DirectoryReference.Combine(UnrealBuildTool.EngineDirectory, "Build", "BatchFiles");''',
        search_only=False,
        file_filter=("VCProject.cs",))
   
    SearchAndReplace(search_path=path, search_string='TargetRulesObject.Type == TargetType.Editor',
        replace_string='(TargetRulesObject.Type == TargetType.Editor || TargetRulesObject.Type == TargetType.App)',
        search_only=False,
        file_filter=("VCProject.cs",))
    SearchAndReplace(search_path=path, search_string='((TargetRulesObject.Type == TargetType.Editor || TargetRulesObject.Type == TargetType.App) || TargetRulesObject.Type == TargetType.App)',
        replace_string='(TargetRulesObject.Type == TargetType.Editor || TargetRulesObject.Type == TargetType.App)',
        search_only=False,
        file_filter=("VCProject.cs",))

    
    SearchAndReplace(search_path=path, search_string='''x.TargetConfigurationName == TargetType.Editor''',
        replace_string='''(x.TargetConfigurationName == TargetType.Editor || x.TargetConfigurationName == TargetType.App)''',
        search_only=False,
        file_filter=("VCProjectFileGenerator.cs",))
    SearchAndReplace(search_path=path, search_string='''((x.TargetConfigurationName == TargetType.Editor || x.TargetConfigurationName == TargetType.App) || x.TargetConfigurationName == TargetType.App)''',
        replace_string='''(x.TargetConfigurationName == TargetType.Editor || x.TargetConfigurationName == TargetType.App)''',
        search_only=False,
        file_filter=("VCProjectFileGenerator.cs",)) 
    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.EngineSourceDirectory, "Programs"''',
        replace_string='''UnrealBuildTool.EngineSourceProgramsDirectory''',
        search_only=False,
        file_filter=("VCProjectFileGenerator.cs",))
    path = "./Engine/Source/Programs/UnrealBuildTool/System"

    SearchAndReplace(search_path=path, search_string='''if(TargetType == TargetType.Program)''',
        replace_string='''if(TargetType == TargetType.Program || TargetType == TargetType.App)''',
        search_only=False,
        file_filter=("ActionHistory.cs",))
    SearchAndReplace(search_path=path, search_string='''	string AppName;
				if (TargetType == TargetType.Program)''',
        replace_string='''string AppName = TargetName;
				if (TargetType == TargetType.Program || TargetType == TargetType.App)''',
        search_only=False,
        file_filter=("CppDependencyCache.cs",))
    SearchAndReplace(search_path=path, search_string='DirectoryItem.Combine(BaseDirectory, "Source");',
        replace_string='DirectoryItem.GetItemByDirectoryReference(UnrealBuildTool.EngineSourceDirectory);',
        search_only=False,
        file_filter=("FileMetadataPrefetch.cs",))

    SearchAndReplace(search_path=path, search_string='Target.Type == TargetType.Editor',
        replace_string='(Target.Type == TargetType.Editor || Target.Type == TargetType.App)',
        search_only=False,
        file_filter=("ModuleDescriptor.cs",))
    SearchAndReplace(search_path=path, search_string='((Target.Type == TargetType.Editor || Target.Type == TargetType.App) || Target.Type == TargetType.App)',
        replace_string='(Target.Type == TargetType.Editor || Target.Type == TargetType.App)',
        search_only=False,
        file_filter=("ModuleDescriptor.cs",))

    SearchAndReplace(search_path=path, search_string='TargetType == TargetType.Editor',
        replace_string='(TargetType == TargetType.Editor || TargetType == TargetType.App)',
        search_only=False,
        file_filter=("ModuleDescriptor.cs",))
    SearchAndReplace(search_path=path, search_string='((TargetType == TargetType.Editor || TargetType == TargetType.App) || TargetType == TargetType.App)',
        replace_string='(TargetType == TargetType.Editor || TargetType == TargetType.App)',
        search_only=False,
        file_filter=("ModuleDescriptor.cs",))


    SearchAndReplace(search_path=path, search_string='TargetType == TargetType.Editor',
        replace_string='(TargetType == TargetType.Editor || TargetType == TargetType.App)',
        search_only=False,
        file_filter=("Plugins.cs",))
    SearchAndReplace(search_path=path, search_string='((TargetType == TargetType.Editor || TargetType == TargetType.App) || TargetType == TargetType.App)',
        replace_string='(TargetType == TargetType.Editor || TargetType == TargetType.App)',
        search_only=False,
        file_filter=("Plugins.cs",))


    SearchAndReplace(search_path=path, search_string='''Folders.AddRange(UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineDirectory, "Source"));''',
        replace_string='''Folders.AddRange(UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineSourceDirectory));
				Folders.AddRange(UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineSourceProgramsDirectory));
				Folders.AddRange(UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineSourceThirdPartyDirectory));''',
        search_only=False,
        file_filter=("RulesCompiler.cs",))
    SearchAndReplace(search_path=path, search_string='''DirectoryReference SourceDirectory = DirectoryReference.Combine(RootDirectory, "Source");

					AddEngineModuleRulesWithContext(SourceDirectory, "Runtime", DefaultModuleContext, UHTModuleType.EngineRuntime, ModuleFileToContext);
					AddEngineModuleRulesWithContext(SourceDirectory, "Developer", DefaultModuleContext, UHTModuleType.EngineDeveloper, ModuleFileToContext);
					AddEngineModuleRulesWithContext(SourceDirectory, "Editor", DefaultModuleContext, UHTModuleType.EngineEditor, ModuleFileToContext);
					AddEngineModuleRulesWithContext(SourceDirectory, "ThirdParty", DefaultModuleContext, UHTModuleType.EngineThirdParty, ModuleFileToContext);''',
        replace_string='''DirectoryReference SourceDirectory = UnrealBuildTool.EngineSourceDirectory;
 					AddEngineModuleRulesWithContext(SourceDirectory, "Runtime", DefaultModuleContext, UHTModuleType.EngineRuntime, ModuleFileToContext);
					AddEngineModuleRulesWithContext(SourceDirectory, "Developer", DefaultModuleContext, UHTModuleType.EngineDeveloper, ModuleFileToContext);
					AddEngineModuleRulesWithContext(SourceDirectory, "Editor", DefaultModuleContext, UHTModuleType.EngineEditor, ModuleFileToContext);
					AddEngineModuleRulesWithContext(UnrealBuildTool.EngineSourceThirdPartyDirectory, "", DefaultModuleContext, UHTModuleType.EngineThirdParty, ModuleFileToContext);''',
        search_only=False,
        file_filter=("RulesCompiler.cs",))
    SearchAndReplace(search_path=path, search_string='''ProgramTargetFiles.AddRange(FindAllRulesFiles(SourceDirectory, RulesFileType.Target));''',
        replace_string='''ProgramTargetFiles.AddRange(FindAllRulesFiles(UnrealBuildTool.EngineSourceDirectory, RulesFileType.Target));
				    ProgramTargetFiles.AddRange(FindAllRulesFiles(UnrealBuildTool.EngineSourceProgramsDirectory, RulesFileType.Target));''',
        search_only=False,
        file_filter=("RulesCompiler.cs",))


    path = "./Engine/Source/Programs/UnrealBuildTool/ToolChain"
    SearchAndReplace(search_path=path, search_string='''UnrealBuildTool.EngineSourceDirectory.FullName, "ThirdParty",''',
        replace_string='''UnrealBuildTool.EngineSourceThirdPartyDirectory.ToString(),''',
        search_only=False,
        file_filter=("UEToolChain.cs",))
    

   


    

        
    path = "./Engine/Source/Programs/UnrealBuildTool/"
    SearchAndReplace(search_path=path, search_string='''public static readonly DirectoryReference EngineSourceDirectory = DirectoryReference.Combine(EngineDirectory, "Source");''',
        replace_string='''public  static DirectoryReference EngineSourceDirectory = DirectoryReference.Combine(EngineDirectory, "Source");''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))
    SearchAndReplace(search_path=path, search_string='''[Obsolete("Please use UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineDirectory, \\"Source/Programs\\") instead.")]
		public static readonly DirectoryReference EngineSourceProgramsDirectory = DirectoryReference.Combine(EngineSourceDirectory, "Programs");''',
        replace_string='''public static  readonly DirectoryReference EngineSourceProgramsDirectory = DirectoryReference.Combine(EngineSourceDirectory, "Programs");''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))
    SearchAndReplace(search_path=path, search_string='''[Obsolete("Please use UnrealBuildTool.GetExtensionDirs(UnrealBuildTool.EngineDirectory, \\"Source/ThirdParty\\") instead.")]
		public static readonly DirectoryReference EngineSourceThirdPartyDirectory = DirectoryReference.Combine(EngineSourceDirectory, "ThirdParty");''',
        replace_string='''public static  readonly DirectoryReference EngineSourceThirdPartyDirectory = DirectoryReference.Combine(EngineSourceDirectory, "ThirdParty");''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))
    SearchAndReplace(search_path=path, search_string='''public string RemoteIni = "";''',
        replace_string='''public string RemoteIni = "";

			[CommandLine(Prefix = "-SourceDir")]
			public string SourceDir = "";''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))
    SearchAndReplace(search_path=path, search_string='''public string RemoteIni = "";

			[CommandLine(Prefix = "-SourceDir")]
			public string SourceDir = "";

			[CommandLine(Prefix = "-SourceDir")]
			public string SourceDir = "";''',
        replace_string='''public string RemoteIni = "";

			[CommandLine(Prefix = "-SourceDir")]
			public string SourceDir = "";''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))
    SearchAndReplace(search_path=path, search_string='''Log.AddFileWriter("LogTraceListener", Options.LogFileName);
				}''',
        replace_string='''Log.AddFileWriter("LogTraceListener", Options.LogFileName);
				}
				 
				if (!string.IsNullOrEmpty(Options.SourceDir))
				{
					UnrealBuildTool.EngineSourceDirectory = DirectoryReference.FromString(Options.SourceDir);
				}''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))

    SearchAndReplace(search_path=path, search_string='''Log.AddFileWriter("LogTraceListener", Options.LogFileName);
				}
				 
				if (!string.IsNullOrEmpty(Options.SourceDir))
				{
					UnrealBuildTool.EngineSourceDirectory = DirectoryReference.FromString(Options.SourceDir);
				}
				 
				if (!string.IsNullOrEmpty(Options.SourceDir))
				{
					UnrealBuildTool.EngineSourceDirectory = DirectoryReference.FromString(Options.SourceDir);
				}''',
        replace_string='''Log.AddFileWriter("LogTraceListener", Options.LogFileName);
				}
				 
				if (!string.IsNullOrEmpty(Options.SourceDir))
				{
					UnrealBuildTool.EngineSourceDirectory = DirectoryReference.FromString(Options.SourceDir);
				}''',
        search_only=False,
        file_filter=("UnrealBuildTool.cs",))



