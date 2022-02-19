// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class TestAppUE4Target : TargetRules
{
	public TestAppUE4Target( TargetInfo Target ) : base(Target)
	{
		Type = TargetType.App;
		BuildEnvironment = TargetBuildEnvironment.Shared;
		//LinkType = TargetLinkType.Monolithic;
		LaunchModuleName = "Launch";

	
		bBuildAllModules = false;
		bBuildAllPlugins = false;
		ExtraModuleNames.Add("UE4Game");
		WindowsPlatform.bUseBundledDbgHelp = false;


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
