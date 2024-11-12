import unreal


@unreal.uclass()
class FixTextureCompression(unreal.ToolMenuEntryScript):
    EditorAssetLib = unreal.EditorAssetLibrary()

    # suffixes based on https://gist.github.com/excalith/366e15b13c1c99539aa2600ff3d5e647#textures
    COMPRESSION_MAPPING = {
        "_D": unreal.TextureCompressionSettings.TC_DEFAULT,  # diffuse/colour map
        "_N": unreal.TextureCompressionSettings.TC_NORMALMAP,  # normal map
        "_E": unreal.TextureCompressionSettings.TC_DEFAULT,  # emissive map
        "_M": unreal.TextureCompressionSettings.TC_MASKS,  # mask map
        "_R": unreal.TextureCompressionSettings.TC_GRAYSCALE,  # roughness map
        "_MT": unreal.TextureCompressionSettings.TC_GRAYSCALE,  # metallic map
        "_S": unreal.TextureCompressionSettings.TC_MASKS,  # specular
        "_DP": unreal.TextureCompressionSettings.TC_DISPLACEMENTMAP,  # displacement
        "_AO": unreal.TextureCompressionSettings.TC_MASKS,  # ambient occlusion
        "_H": unreal.TextureCompressionSettings.TC_DISPLACEMENTMAP,  # height map
        "_F": unreal.TextureCompressionSettings.TC_NORMALMAP,  # flow map
        "_ORD": unreal.TextureCompressionSettings.TC_MASKS,  # occlusion, roughness and displacement map
        "_NMR": unreal.TextureCompressionSettings,  # normal, metallic, roughness, math on normals directly on texture
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
                    continue  # if the above is true, and it's NOT the specified class, continue with the next loop iteration

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
                current_compression = texture.get_editor_property(
                    "compression_settings"
                )

                if current_compression != correct_compression:
                    print(f"WRONG COMPRESSION SETTINGS ON: {asset_path}")
                    if apply_fix:
                        texture.set_editor_property(
                            "compression_settings", correct_compression
                        )
                        slow_task.enter_progress_frame(1)
                        print(
                            f"{asset_path} compression was set to {str(correct_compression)}"
                        )

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
    def execute(self, context):  # type: ignore
        with unreal.ScopedEditorTransaction("Fix Texture Compression"):
            self.validate_compression_settings("/Game", True)
