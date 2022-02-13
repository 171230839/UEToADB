
# -*- coding:utf8 -*-


import os, re, time, fnmatch, difflib

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
    f = open(filepath, "r")
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
    sourceDir = "./Engine/Source";
    dirList = ["Runtime", "Developer", "Editor"]
    for i in range(0, len(dirList)):
        path = os.path.join(sourceDir, dirList[i])
        # SearchAndReplace(search_path=path, search_string='PrivateIncludePaths.Add( "ThirdParty/',
        # replace_string='PrivateIncludePaths.Add( Target.UEThirdPartySourceDirectory + "',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='PublicIncludePaths.Add( "ThirdParty/',
        # replace_string='PublicIncludePaths.Add( Target.UEThirdPartySourceDirectory + "',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='PublicSystemIncludePaths.Add("ThirdParty/',
        # replace_string='PublicSystemIncludePaths.Add(Target.UEThirdPartySourceDirectory + "',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='Target.Type != TargetType.Editor',
        # replace_string='Target.Type != TargetType.Editor && Target.Type != TargetType.App',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='PublicIncludePaths.Add("Programs/',
        # replace_string='PublicIncludePaths.Add(Target.UEProgramsSourceDirectory + "',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='PrivateIncludePaths.Add("Programs/',
        # replace_string='PrivateIncludePaths.Add(Target.UEProgramsSourceDirectory + "',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='Target.Type == TargetType.Editor',
        # replace_string='Target.Type == TargetType.Editor || Target.Type == TargetType.App',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='Target.Type == TargetType.Editor || Target.Type == TargetType.App || Target.Type == TargetType.App',
        # replace_string='Target.Type == TargetType.Editor || Target.Type == TargetType.App',
        # search_only=False,
        # file_filter=("*.build.cs",))
        # SearchAndReplace(search_path=path, search_string='#include "ThirdParty/',
        # replace_string='#include "',
        # search_only=False,
        # file_filter=("*.*",))        


    # path = "./Engine/Plugins"
    # SearchAndReplace(search_path=path, search_string='"../../../../Source/Runtime',
    # replace_string='EngineSourceDir + "Runtime',
    #  search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='"../../../../Source/ThirdParty/',
    # replace_string='ThirdPartyDir + "',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='"Path.Combine(EngineDir, "Source", "ThirdParty",',
    # replace_string='Path.Combine(ThirdPartyDir,',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='"Path.Combine(EngineSourceDirectory, "ThirdParty/',
    # replace_string='Path.Combine(ThirdPartyDir, "',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='"Path.Combine(EngineDir, "Source/Runtime',
    # replace_string='Path.Combine(EngineSourceDir, "Runtime',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='Path.Combine(EngineDir, @"Source/Editor/',
    # replace_string='Path.Combine(EngineSourceDir, @"Editor/',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='Path.Combine(EngineDir, @"Source/Developer/',
    # replace_string='Path.Combine(EngineSourceDir, @"Developer/',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='Path.Combine(EngineDir, @"Source/Runtime/',
    # replace_string='Path.Combine(EngineSourceDir, @"Runtime/',
    # search_only=False,
    # file_filter=("*.build.cs",))
    path = "./Engine/Source/Programs"
    # SearchAndReplace(search_path=path, search_string='PrivateIncludePaths.Add("Programs/',
    # replace_string='PrivateIncludePaths.Add(Target.UEProgramsSourceDirectory + "',
    # search_only=False,
    # file_filter=("*.build.cs",))
    # SearchAndReplace(search_path=path, search_string='"Programs/',
    # replace_string='Target.UEProgramsSourceDirectory + "',
    # search_only=False,
    # file_filter=("*.build.cs",))

    path = "./Engine/SourceNew/Runtime/Projects"
    SearchAndReplace(search_path=path, search_string='Target.Type == TargetType.Editor || Target.Type == TargetType.App',
    replace_string='Target.Type == TargetType.Editor',
    search_only=False,
    file_filter=("*.build.cs",))
    SearchAndReplace(search_path=path, search_string='PrivateDefinitions.Add(String.Format("UBT_TARGET_ENABLED_PLUGINS={0}", String.Join(", ", EnabledPluginStrings)));',
    replace_string='''PrivateDefinitions.Add(String.Format("UBT_TARGET_ENABLED_PLUGINS={0}", String.Join(", ", EnabledPluginStrings))); 
				PublicDefinitions.Add(String.Format("UBT_TARGET_BUILD_ALLPLUGINS={0}", Target.bBuildAllPlugins?1:0));''',
    search_only=False,
    file_filter=("*.build.cs",))
   
    # path = "./Engine/SourceNew/Runtime/Projects/Private"
    # SearchAndReplace(search_path=path, search_string='bool bAllowEnginePluginsEnabledByDefault = true;',
    # replace_string='bool bAllowEnginePluginsEnabledByDefault = (bool)(UBT_TARGET_BUILD_ALLPLUGINS);',
    # search_only=False,
    # file_filter=("*.*",))



  