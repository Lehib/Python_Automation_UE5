import unreal


# Registering the menu and entry
tool_menus = unreal.ToolMenus.get()
main_menu = tool_menus.find_menu(unreal.Name("LevelEditor.MainMenu"))

# Add the "Automation" sub-menu
automation_menu = main_menu.add_sub_menu(
    owner=unreal.Name("PythonAutomation"),
    section_name=unreal.Name(""),
    name=unreal.Name("PythonAutomation"),
    label=unreal.Text("Automation"), 
    tool_tip=unreal.Text("Python automation scripts")
    )

# sections
general_section_name = unreal.Name("GeneralAutomation")
automation_menu.add_section(general_section_name, unreal.Text("General"))

# next steps: adding GUI to give users option of adding or removing EXISTING_PREFIXES and EXCLUSIONS
# gather a larger list for PREFIX_MAPPING, and maybe see if it's possible to give users access to change the values

# Define the Set Prefix ToolMenu entry class
@unreal.uclass()
class SetPrefix(unreal.ToolMenuEntryScript):
    # Define constants and initialize EditorAssetLib
    EditorAssetLib = unreal.EditorAssetLibrary()

    PREFIX_MAPPING = {
        unreal.Texture2D: "T_",
        unreal.Material: "M_",
        unreal.MaterialInstanceConstant: "MI_",
        unreal.Blueprint: "BP_"
    }
    EXISTING_PREFIXES = {"T_", "M_", "MI_", "BP_", "Blueprint", "blueprint", "PPM_", "PPMI_"}
    EXCLUSIONS = {"MM_"}
    SUFFIXES = {"_Inst"}

    # Define the fix_prefix method as part of the class
    def fix_prefix(self, directory: str, apply_fix: bool = True):
        asset_path_list = self.EditorAssetLib.list_assets(directory, recursive=True)
        steps = len(asset_path_list)

        with unreal.ScopedSlowTask(steps, "Fixing prefixes for assets...") as slow_task:
            slow_task.make_dialog_delayed(1.5, can_cancel=True)

            for asset_path in asset_path_list:
                if slow_task.should_cancel():
                    unreal.log("Task was canceled by the user.")
                    break

                asset = self.EditorAssetLib.load_asset(asset_path)
                asset_name = asset.get_name()

                if any(asset_name.startswith(exclusion) for exclusion in self.EXCLUSIONS):
                    print(f"Skipping {asset_name} due to exclusion prefix.")
                    slow_task.enter_progress_frame(1)
                    continue

                correct_prefix = None
                for asset_type, prefix in self.PREFIX_MAPPING.items():
                    if isinstance(asset, asset_type):
                        correct_prefix = prefix

                        for existing_prefix in self.EXISTING_PREFIXES:
                            if asset_name.startswith(existing_prefix):
                                asset_name = asset_name[len(existing_prefix):]
                                break

                        if isinstance(asset, unreal.Material):
                            material_domain = asset.get_editor_property("material_domain")
                            is_postprocess = material_domain == unreal.MaterialDomain.MD_POST_PROCESS

                            if is_postprocess:
                                ppm_directory = "/Game/PostProcessMaterials"
                                if not self.EditorAssetLib.does_directory_exist(ppm_directory):
                                    self.EditorAssetLib.make_directory(ppm_directory)

                                for suffix in self.SUFFIXES:
                                    if asset_name.endswith(suffix):
                                        asset_name = asset_name[:-len(suffix)]
                                        break
                                
                                new_name = "PPM_" + asset_name
                                new_path = f"{ppm_directory}/{new_name}"

                                if apply_fix:
                                    success = self.EditorAssetLib.rename_asset(asset_path, new_path)
                                    if success:
                                        print(f"Renamed {asset_name} to {new_name} in PostProcessMaterials directory.")
                                    else:
                                        print(f"Failed to rename {asset_name}")
                                else:
                                    print(f"Suggested rename for post-process material: {asset_name} to {new_name}")

                                slow_task.enter_progress_frame(1)
                                continue

                        for suffix in self.SUFFIXES:
                            if asset_name.endswith(suffix):
                                asset_name = asset_name[:-len(suffix)]
                                break
                        new_name = correct_prefix + asset_name
                        new_path = "/".join(asset_path.split("/")[:-1]) + "/" + new_name

                        if apply_fix:
                            success = self.EditorAssetLib.rename_asset(asset_path, new_path)
                            if success:
                                print(f"Renamed {asset.get_name()} to {new_name}")
                            else:
                                print(f"Failed to rename {asset_name}")
                        else:
                            print(f"Suggested rename: {asset_name} to {new_name}")
                        break
                slow_task.enter_progress_frame(1)

    # Override execute to call fix_prefix
    @unreal.ufunction(override=True)
    def execute(self, context): # type: ignore
        # Calls fix_prefix when menu item is selected
        self.fix_prefix("/Game", apply_fix=True)

# Create an instance of SetPrefix
prefix_script_object = SetPrefix()

# Initialize the entry in the custom menu
prefix_script_object.init_entry(
    owner_name=unreal.Name("PythonAutomation"),
    menu=unreal.Name("LevelEditor.MainMenu.PythonAutomation"),
    section=general_section_name,
    name=unreal.Name("SetPrefix"),
    label=unreal.Text("Set Prefixes"),
    tool_tip=unreal.Text("Set the prefixes for assets in the Content Browser")
)

prefix_script_object.register_menu_entry()

# icon
prefix_script_data = prefix_script_object.data
prefix_script_icon = unreal.ScriptSlateIcon(
    style_name=unreal.Name("Palette.Icon"),
    small_style_name=unreal.Name("Palette.Icon.Small"),
    style_set_name=unreal.Name("UMGStyle")
)
prefix_script_data.icon = prefix_script_icon

@unreal.uclass()
class FixTextureCompression(unreal.ToolMenuEntryScript):
    EditorAssetLib = unreal.EditorAssetLibrary()

    # suffixes based on https://gist.github.com/excalith/366e15b13c1c99539aa2600ff3d5e647#textures
    COMPRESSION_MAPPING = {
    "_D": unreal.TextureCompressionSettings.TC_DEFAULT, # diffuse/colour map
    "_N": unreal.TextureCompressionSettings.TC_NORMALMAP, # normal map
    "_E": unreal.TextureCompressionSettings.TC_DEFAULT, # emissive map
    "_M": unreal.TextureCompressionSettings.TC_MASKS, # mask map
    "_R": unreal.TextureCompressionSettings.TC_GRAYSCALE, # roughness map
    "_MT": unreal.TextureCompressionSettings.TC_GRAYSCALE, #metallic map
    "_S": unreal.TextureCompressionSettings.TC_MASKS, # specular
    "_DP": unreal.TextureCompressionSettings.TC_DISPLACEMENTMAP, #displacement
    "_AO": unreal.TextureCompressionSettings.TC_MASKS, # ambient occlusion
    "_H": unreal.TextureCompressionSettings.TC_DISPLACEMENTMAP, # height map
    "_F": unreal.TextureCompressionSettings.TC_NORMALMAP, # flow map
    "_ORD": unreal.TextureCompressionSettings.TC_MASKS, # occlusion, roughness and displacement map
    "_NMR": unreal.TextureCompressionSettings # normal, metallic, roughness, math on normals directly on texture
    }

    # add in that if height or displacement are below a certain size like they're 256x256, consider Grayscale R8
    # compression settings need to be matched in connected texture samplers too where it may not have changed

    # we are stating we'll take a directory argument and an apply fix argument which will be true or false
    def validate_compression_settings(self, directory: str, apply_fix: bool = True):
        asset_path_list = self.EditorAssetLib.list_assets(directory)
        steps = len(asset_path_list)
        
        with unreal.ScopedSlowTask(steps, "Fixing prefixes for assets...") as slow_task:
            slow_task.make_dialog_delayed(1.5, can_cancel=True)
                
            for asset_path in asset_path_list:
                # load asset into texture so we can act on it
                texture = self.EditorAssetLib.load_asset(asset_path)

                if not isinstance(texture, unreal.Texture2D):
                    slow_task.enter_progress_frame(1)
                    continue # if the above is true, and it's NOT the specified class, continue with the next loop iteration

                name = str(texture.get_fname())
                name_match = False
                correct_compression = None

                for suffix in self.COMPRESSION_MAPPING.keys():
                    if name.endswith(suffix):
                        name_match = True
                        correct_compression = self.COMPRESSION_MAPPING[suffix]
                        break

                if not name_match:
                    slow_task.enter_progress_frame(1)
                    continue

                # we will now have the editor property we want as an object
                current_compression = texture.get_editor_property("compression_settings")

                if current_compression != correct_compression:
                    print(f"WRONG COMPRESSION SETTINGS ON: {asset_path}")
                    if apply_fix:
                        texture.set_editor_property("compression_settings", correct_compression)
                        slow_task.enter_progress_frame(1)
                        print(f"{asset_path} compression was set to {str(correct_compression)}")

                # Set sRGB based on suffix type
                if name.endswith("_D"):
                    if not texture.get_editor_property("sRGB"):
                        texture.set_editor_property("sRGB", True)
                        slow_task.enter_progress_frame(1)
                        print(f"enabled sRGB on {name}")
                else:
                    if texture.get_editor_property("sRGB"):
                        texture.set_editor_property("sRGB", False)
                        slow_task.enter_progress_frame(1)
                        print(f"disabled sRGB on {name}")

    @unreal.ufunction(override=True)
    def execute(self, context): # type: ignore
        with unreal.ScopedEditorTransaction("Fix Texture Compression"):
            self.validate_compression_settings("/Game", True)

compression_script_object = FixTextureCompression()

compression_script_object.init_entry(
    owner_name=unreal.Name("PythonAutomation"),
    menu=unreal.Name("LevelEditor.MainMenu.PythonAutomation"),
    section=general_section_name,
    name=unreal.Name("FixCompression"),
    label=unreal.Text("Fix Texture Compression"),
    tool_tip=unreal.Text("Set the texture compression settings for textures in the Content Browser")
)

compression_script_object.register_menu_entry()

# icon
compression_script_data = compression_script_object.data
compression_script_icon = unreal.ScriptSlateIcon(
    style_name=unreal.Name("Palette.Icon"),
    small_style_name=unreal.Name("Palette.Icon.Small"),
    style_set_name=unreal.Name("UMGStyle")
)
compression_script_data.icon = compression_script_icon

# Refresh menu to update changes
tool_menus.refresh_all_widgets()
