// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class TestAppTarget : TargetRules
{
	public TestAppTarget( TargetInfo Target ) : base(Target)
	{
		Type = TargetType.App;
		BuildEnvironment = TargetBuildEnvironment.Shared;
		//LinkType = TargetLinkType.Monolithic;
		LaunchModuleName = "Launch";

		ModuleNameExtra = "App";
		bBuildAllModules = false;
		bBuildAllPlugins = false;
		ExtraModuleNames.Add("UnrealGame");
		WindowsPlatform.bUseBundledDbgHelp = false;


        EnablePlugins.Add("InterChange");
        EnablePlugins.Add("SunPosition");
        EnablePlugins.Add("DataPrepEditor");
        EnablePlugins.Add("DatasmithImporter");
        EnablePlugins.Add("VariantManager");
        EnablePlugins.Add("PythonScriptPlugin");
        EnablePlugins.Add("HDRIBackdrop");
        EnablePlugins.Add("SequencerScripting");
        EnablePlugins.Add("DatasmithCADImporter");
        EnablePlugins.Add("DatasmithIFCImporter");
        EnablePlugins.Add("DatasmithGLTFImporter");
        EnablePlugins.Add("AxFImporter");
        EnablePlugins.Add("ModelingToolsEditorMode");
        EnablePlugins.Add("DatasmithC4DImporter");
        EnablePlugins.Add("MovieRenderPipeline");

    }
}
