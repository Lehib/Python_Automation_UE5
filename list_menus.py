import unreal

# going to iterate over some numbers to construct the name of unreal object and if we retrieve any object by that name we've found an existing menu name
def list_menu(num=1000):
    menu_list = set()
    for i in range (num):
        obj = unreal.find_object(None, "/Engine/Transient.ToolMenus_0:RegisteredMenu_%s" % i)
        if not obj:
            obj = unreal.find_object(None, f"/Engine/Transient.ToolMenus_0:ToolMenu_{i}") # for backwards compatibility
        
        # skips all objects that are not found
        if not obj:
            continue

        menu_name = str(obj.menu_name)
        if menu_name == "None":
            continue

        menu_list.add(menu_name)

    return list(menu_list)

print(list_menu())

# creating a custom menu item for the users automation scripts
menus = unreal.ToolMenus.get()
main_menu = menus.find_menu("LevelEditor.MainMenu") # type: ignore
custom_menu = main_menu.add_sub_menu("Custom Menu", "Python Automation", "Menu Name", "Automation") # type: ignore
menus.refresh_all_widgets()


MENUS = {
'ContentBrowser.AssetContextMenu.MirrorDataTable',
'SourceControl.ChangelistContextMenu',
'LevelEditor.ElementContextMenu',
'MainFrame.MainMenu.Tools',
'ContentBrowser.AssetViewOptions.PathViewFilters',
'ContentBrowser.FolderContextMenu',
'ContentBrowser.AssetContextMenu.MaterialFunction',
'NiagaraEditorModule.ContentBrowserNiagaraTags',
'MainFrame.MainMenu.Edit',
'LevelEditor.InViewportPanel',
'LevelEditor.ActorContextMenu',
'ContentBrowser.AssetViewOptions',
'LevelEditor.LevelEditorSceneOutliner.ContextMenu',
'MainFrame.NomadMainMenu',
'ContentBrowser.AssetContextMenu.AnimBlueprint',
'LevelEditor.LevelEditorToolBar.SettingsToolbar',
'ControlRigEditor.RigHierarchy.ContextMenu.New',
'ContentBrowser.AssetContextMenu.NiagaraScript.ManageTags',
'StatusBar.ToolBar.SourceControl',
'LevelEditor.MainMenu.Build.LightingInfo.LightingDensity',
'LevelEditor.StatusBar.ToolBar',
'ContentBrowser.AssetContextMenu.WidgetBlueprint.AssetActionsSubMenu',
'LevelEditor.MainMenu.Build',
'LevelEditor.MainMenu.Edit',
'LevelEditor.LevelEditorToolBar.AssetsToolBar',
'AssetEditor.AnimationBlueprintEditor.MainMenu.Tools',
'ContentBrowser.AssetContextMenu.LevelSequence',
'ContentBrowser.AssetContextMenu.MediaSource',
'LevelEditor.LevelViewportToolBar.Options',
'LevelEditor.MainMenu.Tools',
'ContentBrowser.AssetContextMenu.NiagaraSystem',
'ContentBrowser.AssetContextMenu.MaterialFunctionInstance',
'LevelEditor.ActorContextMenu.AssetToolsSubMenu',
'ContentBrowser.AssetContextMenu.NiagaraEmitter',
'AssetEditor.SkeletonEditor.ToolBar',
'MainFrame.MainMenu.Asset',
'ContentBrowser.AddNewContextMenu',
'ContentBrowser.AssetContextMenu.Class',
'LevelEditor.SceneOutlinerContextMenu',
'ControlRigEditor.RigHierarchy.DragDropMenu.Align.Translation',
'ControlRigEditor.ModularRigModel.ContextMenu',
'MediaPlayer.AssetPickerAssetContextMenu',
'LevelEditor.MenuBarEmptyContextMenu',
'LevelEditor.MainMenu.File',
'ContentBrowser.AssetContextMenu.BlendSpace',
'ContentBrowser.AssetContextMenu.Texture2D',
'ContentBrowser.AssetContextMenu.TextureRenderTarget',
'NiagaraEditorModule.ManageAssetTags',
'ContentBrowser.AssetContextMenu.StaticMesh',
'LevelEditor.MainMenu.Build.LightingInfo.LightingResolution',
'ContentBrowser.AssetContextMenu.DataTable',
'ContentBrowser.AssetContextMenu.NiagaraSystem.ManageTags',
'ContentBrowser.AssetContextMenu.AnimSequence',
'ContentBrowser.AssetContextMenu.NiagaraParameterCollection',
'MainFrame.MainMenu',
'ContentBrowser.AssetContextMenu.World',
'PropertyEditor.RowContextMenu',
'ContentBrowser.AssetContextMenu.BlueprintGeneratedClass',
'LevelEditor.EmptySelectionContextMenu',
'ContentBrowser.AssetContextMenu.SkeletalMesh',
'LevelEditor.LevelEditorToolBar.LevelToolbarQuickSettings',
'VrEditor.ToggleVrOptions',
'LevelEditor.MainMenu.Help',
'MainFrame.MainMenu.Window',
'ContentBrowser.AssetContextMenu.PoseAsset',
'ContentBrowser.AssetContextMenu.DataAsset',
'ContentBrowser.AssetContextMenu.ControlRigPoseAsset',
'ContentBrowser.AssetContextMenu.Blueprint',
'ContentBrowser.AssetContextMenu.CurveBase',
'LevelEditor.ActorContextMenu.LevelSubMenu',
'LevelEditor.MainMenu.Window',
'ContentBrowser.AssetContextMenu.FontFace',
'ContentBrowser.AssetContextMenu.MetaSoundPatch',
'ContentBrowser.AssetContextMenu.EditorUtilityBlueprint',
'EditorSettingsViewer.LevelEditorPlaySettings',
'AssetEditor.SkeletalMeshEditor.ToolBar',
'ContentBrowser.AssetContextMenu.MaterialInstanceConstant',
'LevelEditor.MainMenu.Build.LightingInfo',
'AssetEditor.WidgetBlueprintEditor.ToolBar.DesignerName',
'LevelEditor.LevelEditorToolBar.AddQuickMenu',
'LevelEditor.MainMenu.Build.LightingQuality',
'OutputLog.SettingsMenu',
'ContentBrowser.AssetContextMenu.AnimationAsset',
'LevelEditor.MainMenu',
'ContentBrowser.AssetContextMenu.DatasmithScene',
'LevelEditor.LevelEditorToolBar.ModesToolBar',
'ContentBrowser.AssetContextMenu.ImgMediaSource',
'LevelEditor.LevelEditorToolBar.OpenBlueprint',
'ContentBrowser.AssetContextMenu.NiagaraEmitter.ManageTags',
'ControlRigEditor.RigHierarchy.DragDropMenu.Align',
'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayerBlendInstance',
'ContentBrowser.DragDropContextMenu',
'LevelEditor.LevelEditorToolBar.User',
'ContentBrowser.AssetContextMenu.Texture',
'ContentBrowser.AssetContextMenu',
'ContentBrowser.AssetContextMenu.Skeleton',
'ContentBrowser.AssetContextMenu.NiagaraScript',
'ControlRigEditor.RigHierarchy.ContextMenu.Naming',
'ContentBrowser.AssetContextMenu.SoundWave',
'LevelEditor.LevelEditorSceneOutliner.ContextMenu.LevelSubMenu',
'ContentBrowser.AssetContextMenu.InterchangeSceneImportAsset',
'ContentBrowser.AssetContextMenu.LevelVariantSets',
'ContentBrowser.AssetContextMenu.AssetActionsSubMenu',
'LevelEditor.MainMenu.Select',
'AssetEditor.AnimationEditor.ToolBar',
'ContentBrowser.ToolBar',
'ContentBrowser.AssetContextMenu.MaterialInterface',
'AssetEditor.WidgetBlueprintEditor.ToolBar.GraphName',
'LevelEditor.ComponentContextMenu',
'ContentBrowser.AssetContextMenu.EditorUtilityWidgetBlueprint',
'MainFrame.MainMenu.Help',
'ContentBrowser.AssetContextMenu.CurveTable',
'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayerBlend',
'ContentBrowser.AssetContextMenu.MetaSoundSource',
'ContentBrowser.AssetContextMenu.AnimMontage',
'ControlRigEditor.RigHierarchy.DragDropMenu',
'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayer',
'ControlRigEditor.RigHierarchy.ContextMenu',
'ContentBrowser.AssetContextMenu.SoundCue',
'ContentBrowser.AssetContextMenu.NiagaraDataChannelAsset',
'LevelEditor.LevelEditorToolBar.Cinematics',
'ContentBrowser.AssetContextMenu.Font',
'LevelEditor.LevelEditorToolBar.PlayToolBar',
'MainFrame.MainMenu.File',
'ContentBrowser.AssetContextMenu.ObjectRedirector',
'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayerInstance',
'LevelEditor.SecondaryToolbar',
'ContentBrowser.AssetContextMenu.SkeletalMesh.CreateSkeletalMeshSubmenu',
'ContentBrowser.AssetContextMenu.IKRigDefinition',
'ContentBrowser.AssetContextMenu.Skeleton.CreateSkeletalMeshSubmenu',
'ContentBrowser.AssetContextMenu.TextureCube',
'MainFrame.MainTabMenu.File'}